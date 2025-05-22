import pandas as pd
import streamlit as st
from datetime import datetime

def display_interval_card(df, category, recommended_days):
    """
    指定カテゴリの最新入力日と今日の日付の差（日数）をカード形式で表示する

    Parameters:
    - df: pandas DataFrame, データフレーム
    - category: str, 表示したいカテゴリ名
    - recommended_days: int, 推奨日数
    """
    # カテゴリでフィルタリング
    filtered_df = df[df['カテゴリ'] == category]

    # 日付でソート（新しい順）
    filtered_df = filtered_df.sort_values(by='日付', ascending=False)

    # 最新の日付を取得
    if not filtered_df.empty:
        latest_date = pd.to_datetime(filtered_df.iloc[0]['日付'])
        latest_memo = filtered_df.iloc[0]['メモ']
        today = pd.to_datetime(datetime.now().date())
        days_diff = (today - latest_date).days

        # days_diffの色分岐
        color = "#2CA02C" if days_diff > recommended_days else "#d32f2f"  # 緑 or 赤

        # カード形式で表示
        st.markdown(
            f"""
            <div style="border:1px solid #ccc; border-radius:5px; padding:10px; background:#f9f9f9; text-align:center;">
                <h2>
                    <span style="color:{color};">{days_diff}</span> / {recommended_days} 日
                </h2>
                <p>{latest_date.strftime('%Y-%m-%d')} ： {str(latest_memo)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info(f"カテゴリ「{category}」のデータがありません。")
