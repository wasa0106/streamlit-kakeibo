import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv
import os

from components.list import display_filtered_data
from components.Interval import display_interval_card
from components.timeline import display_timeline
from components.monthly_list import display_monthly_list
from components.stacked_bar import display_stacked_bar

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

# データを表示する
if df is not None:

    # 食料
    st.subheader("食料")
    display_interval_card(df, '食料', 3)
    display_timeline(df, '食料', 1, 25000)
    display_monthly_list(df, '食料', 3)

    # カフェ
    st.subheader("カフェ")
    display_interval_card(df, 'カフェ', 3)
    display_timeline(df, 'カフェ', 1, 6000)
    display_filtered_data(df, 'カフェ', 3)
    display_monthly_list(df, 'カフェ', 3)

    # 外食
    st.subheader("外食")
    display_interval_card(df, '外食', 8)
    display_timeline(df, '外食', 1, 6000)
    display_filtered_data(df, '外食', 3)
    display_monthly_list(df, '外食', 3)

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
