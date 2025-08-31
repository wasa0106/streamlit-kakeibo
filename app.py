import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv
import os
import datetime

from components.list import display_filtered_data
from components.Interval import display_interval_card
from components.timeline import display_timeline
from components.monthly_list import display_monthly_list
from components.stacked_bar import display_stacked_bar
from components.daily_budget import display_daily_budget
from components.styles import apply_custom_css
from dateutil.relativedelta import relativedelta

# --- 設定 ---
load_dotenv()
google_sheet_csv_url = os.getenv("GOOGLE_SHEET_CSV_URL")

# カラーマップ
color_map = {
    '医療費': '#17BECF',   # シアン系（清潔感・医療のイメージ）
    '日用品': '#1F77B4',   # 青系（定番）
    '交通費': '#2CA02C',   # 緑（移動のイメージ）
    '交際費': '#D62728',   # 赤（人とのつながり・感情）
    '本・教材': '#9467BD', # 紫（知的・教育系）
    '美容': '#E377C2',     # ピンク系（ビューティー系に合う）
    'イベント': '#8C564B', # ブラウン（落ち着いた雰囲気）
}


# データを読み込む関数
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"データの読み込み中にエラーが発生しました: {e}")
        return None

# データを読み込む
df = load_data(google_sheet_csv_url)
if df is not None:
    df = df.reset_index(drop=True)
    df['日付'] = pd.to_datetime(df['日付'], errors='coerce')

# ページ設定
st.set_page_config(
    page_title="家計簿",
    layout="wide"
)

# カスタムCSSを適用
apply_custom_css()

# データを表示する
if df is not None:

    # 全体
    st.subheader("全体（¥110,000）")
    display_timeline(df, ['食料', '日用品', '医療費', '交際費', '交通費', '本・教材', '設備', '趣味', '飲料・軽食', '外食', 'カフェ', '美容', 'イベント', 'その他'], 1, 110000)

    today = datetime.date.today()


    # 月別合計金額の表を作成
    months = [today - relativedelta(months=i) for i in range(4, -1, -1)]
    month_names = [month.strftime("%m月") for month in months]
    total_amounts = []

    for month in months:
        df_month = df[
            (df['日付'].dt.year == month.year) &
            (df['日付'].dt.month == month.month)
        ]
        total_amount = df_month['金額'].sum()
        total_amounts.append(f"¥{int(total_amount):,}")

    month_data = pd.DataFrame({
        '月': month_names,
        '合計金額': total_amounts
    })

    # テーブルのスタイリング
    styled_month_df = month_data.style.set_properties(**{
        'text-align': 'right',
        'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace",
        'font-size': '14px',
        'padding': '10px'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#F7F8FA'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('padding', '12px'),
            ('border-bottom', '2px solid #E8EAED'),
            ('font-size', '14px')
        ]},
        {'selector': 'td', 'props': [
            ('border-bottom', '1px solid #F0F2F4')
        ]},
        {'selector': 'tr:hover', 'props': [
            ('background-color', '#F7F8FA')
        ]},
        {'selector': 'td:first-child', 'props': [
            ('text-align', 'left'),
            ('font-weight', '500')
        ]}
    ])

    st.dataframe(styled_month_df, use_container_width=True, hide_index=True)


    # カテゴリと予算
    categories = [
        '食料', '日用品', '医療費', '交際費', '交通費', '本・教材', '設備', '趣味', '飲料・軽食', '晩酌・外食・カフェ', '美容', 'イベント', 'その他'
    ]
    budgets = {
        '食料': 30000,
        '日用品': 2000,
        '医療費': 12000,
        '交際費': 35000,
        '交通費': 6000,
        '本・教材': 3000,
        '設備': 2500,
        '趣味': 3000,
        '飲料・軽食': 2000,
        '晩酌・外食・カフェ': 6000,
        '美容': 11000
    }

    # ★カテゴリ選択ウィジェットを追加
    selected_categories = st.multiselect(
        "",
        categories,
        default=['飲料・軽食', '交際費', '本・教材','晩酌・外食・カフェ', '趣味', '美容']
    )


    # 実績計算
    this_month = today.month
    this_year = today.year
    df_this_month = df[
        (df['日付'].dt.year == this_year) &
        (df['日付'].dt.month == this_month)
    ]

    table_data = []
    for cat in selected_categories:  # ←ここをselected_categoriesに
        budget = budgets.get(cat, 0)
        actual = df_this_month[df_this_month['カテゴリ'] == cat]['金額'].sum()
        remain = budget - actual
        table_data.append({
            'カテゴリ': cat,
            '予算': f"¥{budget:,}",
            '実績': f"¥{int(actual):,}",
            '残予算': f"¥{int(remain):,}"
        })

    table_df = pd.DataFrame(table_data, columns=['カテゴリ', '予算', '実績', '残予算'])

    # テーブルのスタイリング
    def color_negative(val):
        """残予算がマイナスの場合は赤色にする"""
        if isinstance(val, str) and val.startswith('¥-'):
            return 'color: #EA4335; font-weight: 600;'
        return ''

    styled_df = table_df.style.applymap(
        color_negative, subset=['残予算']
    ).set_properties(**{
        'text-align': 'right',
        'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace",
        'font-size': '14px',
        'padding': '10px'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#F7F8FA'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('padding', '12px'),
            ('border-bottom', '2px solid #E8EAED'),
            ('font-size', '14px')
        ]},
        {'selector': 'td', 'props': [
            ('border-bottom', '1px solid #F0F2F4')
        ]},
        {'selector': 'tr:hover', 'props': [
            ('background-color', '#F7F8FA')
        ]},
        {'selector': 'td:first-child', 'props': [
            ('text-align', 'left'),
            ('font-weight', '500')
        ]}
    ])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # 食料
    st.subheader("食料")
    col1, col2 = st.columns(2)
    with col1:
        display_interval_card(df, '食料', 2)
    with col2:
        display_daily_budget(df, '食料', 30000)
    display_timeline(df, '食料', 1, 30000)
    display_monthly_list(df, '食料', 3)

    # 晩酌・外食・カフェ
    st.subheader("晩酌・外食・カフェ")
    col1, col2 = st.columns(2)
    with col1:
        display_interval_card(df, '晩酌・外食・カフェ', 7)
    with col2:
        display_daily_budget(df, '晩酌・外食・カフェ', 6000)
    display_timeline(df, '晩酌・外食・カフェ', 1, 6000)
    display_filtered_data(df, '晩酌・外食・カフェ', 3)
    display_monthly_list(df, '晩酌・外食・カフェ', 3)

    # 趣味
    st.subheader("趣味")
    display_interval_card(df, '趣味', 15)
    display_timeline(df, '趣味', 3, 9000)
    display_filtered_data(df, '趣味', 3)
    display_monthly_list(df, '趣味', 3)

    # その他
    st.subheader("その他")
    categories = ['医療費','日用品', '交通費', '交際費', '本・教材', '美容','イベント']

    display_stacked_bar(df, categories, months=5, color_map=color_map)

else:
    st.warning("データの読み込みに失敗しました。ウェブ公開設定とURLを確認してください。")
