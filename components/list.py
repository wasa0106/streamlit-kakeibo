import pandas as pd
import streamlit as st

def display_filtered_data(df, category, num_items):
    """
    指定されたカテゴリに一致するデータを新しい順で表示し、表示する個数を設定できる関数。

    Parameters:
    - df: pandas DataFrame, データフレーム
    - category: str, 表示したいカテゴリ名
    - num_items: int, 表示するデータの個数
    """
    # カテゴリでフィルタリング
    filtered_df = df[df['カテゴリ'] == category]

    # 日付でソート（新しい順）
    filtered_df = filtered_df.sort_values(by='日付', ascending=False)

    # 必要なカラムだけ抽出
    filtered_df = filtered_df[['日付', 'メモ', '金額']]

    # 日付のフォーマット変換
    filtered_df['日付'] = pd.to_datetime(filtered_df['日付']).dt.strftime('%-m月%-d日')

    # 金額のフォーマット変換
    filtered_df['金額'] = filtered_df['金額'].apply(lambda x: f"¥{x:,}")

    # 指定された個数だけ表示
    st.write(filtered_df.head(num_items))

# 使用例
# df = load_data(google_sheet_csv_url)  # app.py でデータを読み込む
# display_filtered_data(df, 'カフェ', 5)  # カフェカテゴリの最新5件を表示
