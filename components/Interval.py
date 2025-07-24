import pandas as pd
import streamlit as st
from datetime import datetime
from .styles import get_metric_card_style, get_number_style

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
        status_color = "#EA4335" if days_diff <= recommended_days else "#769CDF"
        card_color = "#EA4335" if days_diff <= recommended_days else "#769CDF"

        # カード形式で表示
        st.markdown(
            f"""
            <div style="{get_metric_card_style(card_color)}">
                <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 2.5rem; font-weight: 600; color: {status_color}; {get_number_style()}">{days_diff}</span>
                    <span style="font-size: 1.25rem; color: #5F6368;">/ {recommended_days} 日</span>
                </div>
                <div style="color: #5F6368; font-size: 0.875rem;">
                    <span style="margin-right: 8px;">{latest_date.strftime('%Y-%m-%d')}</span>
                    <span>{str(latest_memo)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info(f"カテゴリ「{category}」のデータがありません。")
