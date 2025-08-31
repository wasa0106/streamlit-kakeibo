import pandas as pd
import streamlit as st
from datetime import datetime
import calendar
from .styles import get_metric_card_style, get_number_style

def display_daily_budget(df, category, monthly_budget):
    """
    指定カテゴリの今月の1日あたりの残予算をカード形式で表示する
    
    Parameters:
    - df: pandas DataFrame, データフレーム
    - category: str, 表示したいカテゴリ名
    - monthly_budget: int, 月間予算（円）
    """
    # 今日の日付情報を取得
    today = datetime.now()
    current_year = today.year
    current_month = today.month
    current_day = today.day
    
    # 今月のデータをフィルタリング
    df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
    df_this_month = df[
        (df['日付'].dt.year == current_year) &
        (df['日付'].dt.month == current_month) &
        (df['カテゴリ'] == category)
    ]
    
    # 累計金額を計算
    total_spent = df_this_month['金額'].sum()
    
    # 残予算を計算
    remaining_budget = monthly_budget - total_spent
    
    # 今月の最終日を取得
    last_day_of_month = calendar.monthrange(current_year, current_month)[1]
    
    # 今月の残日数を計算（今日を含む）
    remaining_days = last_day_of_month - current_day + 1
    
    # 1日あたりの残予算を計算
    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
    else:
        # 月末の場合
        daily_budget = remaining_budget
        remaining_days = 1
    
    # 色の設定（残予算がマイナスの場合は赤、プラスの場合は青）
    if remaining_budget < 0:
        status_color = "#EA4335"
        card_color = "#EA4335"
    else:
        status_color = "#769CDF"
        card_color = "#769CDF"
    
    # カード形式で表示
    st.markdown(
        f"""
        <div style="{get_metric_card_style(card_color)}">
            <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 2.5rem; font-weight: 600; color: {status_color}; {get_number_style()}">
                    ¥{int(daily_budget):,}
                </span>
                <span style="font-size: 1.25rem; color: #5F6368;">/ 日</span>
            </div>
            <div style="color: #5F6368; font-size: 0.875rem;">
                <span style="margin-right: 12px;">残予算: ¥{int(remaining_budget):,}</span>
                <span>残り{remaining_days}日</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )