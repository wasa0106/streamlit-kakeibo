import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime

def display_timeline(df, category, months, monthly_budget):
    """
    指定カテゴリ・掲載期間・月間予算で時系列折れ線グラフを表示

    Parameters:
    - df: pandas DataFrame
    - category: str, 表示したいカテゴリ名
    - months: int, 掲載期間（月単位、1なら今月のみ、2なら今月と先月をまとめて）
    - monthly_budget: int, 月間予算（円）
    """
    # 日付をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
    # カテゴリでフィルタ
    filtered_df = df[df['カテゴリ'] == category].copy()
    filtered_df = filtered_df.dropna(subset=['日付'])

    # 掲載期間（月単位）でフィルタ
    now = datetime.now()
    this_month = now.replace(day=1)
    start_month = (this_month - pd.DateOffset(months=months-1)).replace(day=1)
    end_month = (this_month + pd.DateOffset(months=1)) - pd.Timedelta(days=1)
    mask = (filtered_df['日付'] >= start_month) & (filtered_df['日付'] <= end_month)
    period_df = filtered_df[mask].copy()

    if period_df.empty:
        st.info("該当期間のデータがありません。")
        return

    # 日付でソート
    period_df = period_df.sort_values('日付')
    period_df['累積金額'] = period_df['金額'].cumsum()
    period_df['日付ラベル'] = period_df['日付'].dt.strftime('%Y-%m-%d')

    # 期間内の日付リスト
    last_date = period_df['日付'].max()
    # 今月の末日を取得
    end_of_this_month = (now.replace(day=1) + pd.DateOffset(months=1)) - pd.Timedelta(days=1)
    # 期間の終了日を「今月末日」とする
    all_dates = pd.date_range(start=period_df['日付'].min(), end=end_of_this_month)

    # 日ごと累積金額（データがない日は直前の累積値を維持）
    daily = period_df.groupby('日付').agg({'累積金額':'last'}).reindex(all_dates, method='ffill').fillna(0).reset_index()
    daily.columns = ['日付', '累積金額']
    daily['日付ラベル'] = daily['日付'].dt.strftime('%Y-%m-%d')

    # 予算線（全月分合計）
    total_days = (all_dates[-1] - all_dates[0]).days + 1
    total_budget = monthly_budget * months
    daily['予算'] = [(total_budget / total_days) * (i+1) for i in range(total_days)]

    # データが存在する日付までの累積支出だけをプロットする DataFrame
    spend_daily = daily[daily['日付'] <= last_date].copy()

    # 予算線の終了日を決定
    budget_line_end_date = last_date if last_date < end_of_this_month else end_of_this_month
    budget_daily = daily[daily['日付'] <= budget_line_end_date].copy()

    # 折れ線グラフ（記入されている日付までのみプロット）
    line_chart = alt.Chart(spend_daily).mark_line(point=True, color='blue').encode(
        x=alt.X('日付ラベル:O', title='日付', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('累積金額:Q', title='累積金額（円）'),
        tooltip=['日付ラベル', '累積金額']
    )

    # 予算線
    budget_line = alt.Chart(budget_daily).mark_line(strokeDash=[5,5], color='orange').encode(
        x='日付ラベル:O',
        y=alt.Y('予算:Q', title='累積金額（円）'),
        tooltip=['日付ラベル', '予算']
    )

    # 予算線と支出線をレイヤーして表示
    # チャートのタイトルも budget_line_end_date を使用して調整
    chart_title_end_date = budget_line_end_date
    chart = alt.layer(line_chart, budget_line).resolve_scale(y='shared').properties(
        title=f"{start_month.strftime('%Y-%m-%d')} 〜 {chart_title_end_date.strftime('%Y-%m-%d')} の累積支出"
    )

    st.altair_chart(chart, use_container_width=True)


    """
    # データテーブルも表示（任意）
    table_df = period_df.copy()
    table_df['日付'] = table_df['日付'].dt.strftime('%Y-%m-%d')
    st.dataframe(table_df[['日付', '金額', '累積金額', 'メモ']])
    """

