import pandas as pd
import streamlit as st
import datetime

def display_monthly_list(df, category, num_months):
    """
    指定カテゴリのデータを月ごとに集計して表示

    Parameters:
    - df: pandas DataFrame
    - category: str, 表示したいカテゴリ名
    - num_months: int, 表示する月数
    """
    # 日付をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
    # カテゴリでフィルタ
    filtered_df = df[df['カテゴリ'] == category].copy()
    filtered_df = filtered_df.dropna(subset=['日付'])

    # 月ごとに集計
    filtered_df['月'] = filtered_df['日付'].dt.to_period('M')
    monthly_summary = filtered_df.groupby('月').agg(
        購入回数=('金額', 'size'),
        合計金額=('金額', 'sum')
    ).reset_index()

    # 平均金額を計算
    monthly_summary['平均金額'] = monthly_summary['合計金額'] / monthly_summary['購入回数']

    # 金額の表示フォーマット
    monthly_summary['平均金額'] = monthly_summary['平均金額'].apply(lambda x: f"¥{x:,.0f}")
    monthly_summary['合計金額'] = monthly_summary['合計金額'].apply(lambda x: f"¥{x:,.0f}")

    # 「平均金額 × 購入回数 = 合計金額」形式の列を作成
    monthly_summary['詳細'] = monthly_summary.apply(
        lambda row: f"{row['平均金額']} × {row['購入回数']} = {row['合計金額']}", axis=1
    )

    # 月を「YYYY年M月」形式に変換する前に、今月から直近num_month分だけ抽出
    import datetime

    # 今日の年月
    today = pd.Timestamp.today()
    this_month = today.to_period('M')

    # 直近num_month分のPeriodをリストで作成（新しい順）
    recent_months = [(this_month - i) for i in range(num_months)]
    # 古い順に並べ替え
    recent_months = sorted(recent_months)

    # recent_monthsに含まれる月だけ抽出
    monthly_summary = monthly_summary[monthly_summary['月'].isin(recent_months)]

    # 月を「YYYY年M月」形式に変換
    monthly_summary['月'] = monthly_summary['月'].apply(lambda x: f"{x.year}年{x.month}月")

    # 月が若い順にソート
    monthly_summary = monthly_summary.sort_values('月').reset_index(drop=True)

    # 列の順番を指定（「月」と「詳細」だけ表示）
    monthly_summary = monthly_summary[['月', '詳細']]

    # スタイリングを適用
    styled = monthly_summary.style.set_properties(**{
        'text-align': 'right',
        'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace",
        'font-size': '14px',
        'padding': '10px'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#F7F8FA'),
            ('font-weight', '600'),
            ('text-align', 'right'),
            ('padding', '12px'),
            ('border-bottom', '2px solid #E8EAED'),
            ('font-size', '14px')
        ]},
        {'selector': 'td', 'props': [
            ('border-bottom', '1px solid #F0F2F4')
        ]},
        {'selector': 'tr:hover', 'props': [
            ('background-color', '#F7F8FA')
        ]}
    ])

    # 表を表示（st.dataframeでStylerを使う）
    st.dataframe(styled, use_container_width=True, hide_index=True)
