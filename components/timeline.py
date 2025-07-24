import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime

def display_timeline(df, categories, months, monthly_budget):
    """
    指定カテゴリ・掲載期間・月間予算で時系列折れ線グラフを表示

    Parameters:
    - df: pandas DataFrame
    - categories: list[str] or str, 表示したいカテゴリ名またはカテゴリ名のリスト
    - months: int, 掲載期間（月単位、1なら今月のみ、2なら今月と先月をまとめて）
    - monthly_budget: int, 月間予算（円）
    """
    # 日付をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
    # カテゴリでフィルタ
    if isinstance(categories, str):
        categories = [categories]
    filtered_df = df[df['カテゴリ'].isin(categories)].copy()
    filtered_df = filtered_df.dropna(subset=['日付'])

    # 掲載期間（月単位）でフィルタ
    now = datetime.now()
    this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_month = (this_month - pd.DateOffset(months=months-1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_month = ((this_month + pd.DateOffset(months=1)) - pd.Timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
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

    # months=1の場合は今月固定、それ以外は複数月対応
    if months == 1:
        # 今月初日から今月末日まで固定
        start_of_period = this_month
        end_of_period = end_month
    else:
        # 複数月の場合は期間フィルタと同じ範囲
        start_of_period = start_month
        end_of_period = end_month

    all_dates = pd.date_range(start=start_of_period, end=end_of_period)

    # 日ごと累積金額（データがない日は直前の累積値を維持）
    daily = period_df.groupby('日付').agg({'累積金額':'last'}).reindex(all_dates, method='ffill').reset_index()
    daily.columns = ['日付', '累積金額']
    
    # 最初の日付より前の0値を除去し、最後の入力日以降は最後の累積値を維持
    if not daily.empty and daily['累積金額'].notna().any():
        # 最初のデータがある日より前は0のまま
        first_data_idx = daily['累積金額'].first_valid_index()
        if first_data_idx is not None:
            daily.loc[:first_data_idx-1, '累積金額'] = 0
        
        # 最後のデータがある日以降は最後の累積値で埋める
        daily['累積金額'] = daily['累積金額'].fillna(method='ffill').fillna(0)
    else:
        daily['累積金額'] = daily['累積金額'].fillna(0)
    daily['日付ラベル'] = daily['日付'].dt.strftime('%Y-%m-%d')

    # 予算線（全月分合計）
    total_days = (all_dates[-1] - all_dates[0]).days + 1
    total_budget = monthly_budget * months
    daily['予算'] = [(total_budget / total_days) * (i+1) for i in range(total_days)]

    # 今日までの累積支出をプロットする DataFrame
    today = pd.Timestamp(datetime.now().date())
    spend_daily = daily[daily['日付'] <= today].copy()

    # 折れ線グラフ（今日までをプロット）
    line_chart = alt.Chart(spend_daily).mark_line(
        point=True, 
        color='#769CDF',
        strokeWidth=3,
        opacity=0.9
    ).encode(
        x=alt.X('日付ラベル:O', 
                title='日付', 
                axis=alt.Axis(
                    labelAngle=-45,
                    labelFontSize=11,
                    titleFontSize=12,
                    grid=False
                )),
        y=alt.Y('累積金額:Q', 
                title='累積金額（円）',
                axis=alt.Axis(
                    labelFontSize=11,
                    titleFontSize=12,
                    grid=True,
                    gridColor='#F0F2F4',
                    gridDash=[2, 2]
                )),
        tooltip=[
            alt.Tooltip('日付ラベル', title='日付'),
            alt.Tooltip('累積金額:Q', title='支出累計', format=',.0f')
        ]
    )

    # 予算線
    budget_line = alt.Chart(daily).mark_line(
        strokeDash=[8, 4], 
        color='#EA4335',
        strokeWidth=2,
        opacity=0.7
    ).encode(
        x='日付ラベル:O',
        y=alt.Y('予算:Q', title='累積金額（円）'),
        tooltip=[
            alt.Tooltip('日付ラベル', title='日付'),
            alt.Tooltip('予算:Q', title='予算累計', format=',.0f')
        ]
    )

    # 予算線と支出線をレイヤーして表示
    chart = alt.layer(line_chart, budget_line).resolve_scale(y='shared').properties(
        title=f"{start_of_period.strftime('%Y-%m-%d')} 〜 {end_of_period.strftime('%Y-%m-%d')} の累積支出",
        width=800,
        height=400
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelFont='sans-serif',
        titleFont='sans-serif'
    ).configure_title(
        fontSize=16,
        font='sans-serif',
        anchor='start',
        color='#1A1A1A'
    )

    st.altair_chart(chart, use_container_width=True)


    """
    # データテーブルも表示（任意）
    table_df = period_df.copy()
    table_df['日付'] = table_df['日付'].dt.strftime('%Y-%m-%d')
    st.dataframe(table_df[['日付', '金額', '累積金額', 'メモ']])
    """

