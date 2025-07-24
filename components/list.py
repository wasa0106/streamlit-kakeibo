import pandas as pd
import streamlit as st

def display_filtered_data(df, categories, num_items):
    """
    指定されたカテゴリに一致するデータを新しい順で表示し、表示する個数を設定できる関数。

    Parameters:
    - df: pandas DataFrame, データフレーム
    - categories: list[str] or str, 表示したいカテゴリ名またはカテゴリ名のリスト
    - num_items: int, 表示するデータの個数
    """
    # カテゴリでフィルタリング
    if isinstance(categories, str):
        categories = [categories]
    filtered_df = df[df['カテゴリ'].isin(categories)]

    # 日付でソート（新しい順）
    filtered_df = filtered_df.sort_values(by='日付', ascending=False)

    # 必要なカラムだけ抽出
    filtered_df = filtered_df[['日付', 'メモ', '金額']]

    # 日付のフォーマット変換
    filtered_df['日付'] = pd.to_datetime(filtered_df['日付']).dt.strftime('%-m月%-d日')

    # 金額のフォーマット変換
    filtered_df['金額'] = filtered_df['金額'].apply(lambda x: f"¥{x:,}")

    # 指定された個数だけ取得
    display_df = filtered_df.head(num_items).copy()
    
    # スタイリングを適用
    styled = display_df.style.set_properties(**{
        'font-size': '14px',
        'padding': '8px'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#F7F8FA'),
            ('font-weight', '600'),
            ('text-align', 'left'),
            ('padding', '10px'),
            ('border-bottom', '2px solid #E8EAED'),
            ('font-size', '13px')
        ]},
        {'selector': 'td', 'props': [
            ('border-bottom', '1px solid #F0F2F4')
        ]},
        {'selector': 'tr:hover', 'props': [
            ('background-color', '#F7F8FA')
        ]},
        {'selector': 'td:last-child', 'props': [
            ('text-align', 'right'),
            ('font-family', "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace")
        ]}
    ])
    
    # 表示
    st.dataframe(styled, use_container_width=True, hide_index=True)

# 使用例
# df = load_data(google_sheet_csv_url)  # app.py でデータを読み込む
# display_filtered_data(df, 'カフェ', 5)  # カフェカテゴリの最新5件を表示
