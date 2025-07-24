import streamlit as st
import pandas as pd
import altair as alt

def display_stacked_bar(df, categories, months=6, color_map=None):
    """
    指定カテゴリ群のデータを月ごとに積み上げ棒グラフで表示する

    Parameters
    ----------
    df : pd.DataFrame
        データフレーム（'カテゴリ', '日付', '金額' などのカラムが必要）
    categories : list[str]
        表示するカテゴリのリスト
    months : int
        遡って表示する月数
    color_map : dict
        カテゴリごとの色指定（例: {'カフェ': '#ff7f0e', 'ランチ': '#1f77b4'}）
    """
    df = df.copy()
    df['日付'] = pd.to_datetime(df['日付'])

    # 指定カテゴリ群のみ抽出
    df = df[df['カテゴリ'].isin(categories)]

    # 最新月を取得し、months分だけ遡る
    latest_month = df['日付'].max().to_period('M')
    month_list = [(latest_month - i).strftime('%Y-%m') for i in reversed(range(months))]

    # 月カラムを追加
    df['月'] = df['日付'].dt.strftime('%Y-%m')

    # 月リストに含まれるデータのみ
    df = df[df['月'].isin(month_list)]

    # 積み上げ棒グラフ用にカテゴリごとに集計
    grouped = df.groupby(['月', 'カテゴリ'])['金額'].sum().reset_index()

    # 月の順序を左が古いように設定
    grouped['月'] = pd.Categorical(grouped['月'], categories=month_list, ordered=True)

    # 色指定を新しいカラーパレットに更新
    updated_color_map = {
        '医療費': '#769CDF',      # メインカラー
        '日用品': '#5E88D1',      # メインカラーの濃い版
        '交通費': '#34A853',      # グリーン
        '交際費': '#EA4335',      # レッド
        '本・教材': '#9C27B0',    # パープル
        '美容': '#E91E63',        # ピンク
        'イベント': '#795548',    # ブラウン
    }
    
    # 既存のcolor_mapがある場合は、updated_color_mapで更新
    if color_map:
        updated_color_map.update(color_map)
    
    color = alt.Color('カテゴリ:N', 
                     scale=alt.Scale(domain=list(updated_color_map.keys()), 
                                   range=list(updated_color_map.values())),
                     legend=alt.Legend(orient='bottom', 
                                     titleFontSize=12,
                                     labelFontSize=11))

    # Altairで積み上げ棒グラフ作成
    chart = alt.Chart(grouped).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4
    ).encode(
        x=alt.X('月:N', 
                sort=month_list, 
                title='月',
                axis=alt.Axis(
                    labelAngle=0,
                    labelFontSize=11,
                    titleFontSize=12,
                    grid=False
                )),
        y=alt.Y('金額:Q', 
                title='金額（円）',
                axis=alt.Axis(
                    labelFontSize=11,
                    titleFontSize=12,
                    grid=True,
                    gridColor='#F0F2F4',
                    gridDash=[2, 2],
                    format=',.0f'
                )),
        color=color,
        tooltip=[
            alt.Tooltip('月', title='月'),
            alt.Tooltip('カテゴリ', title='カテゴリ'),
            alt.Tooltip('金額:Q', title='金額', format=',.0f')
        ]
    ).properties(
        height=400
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelFont='sans-serif',
        titleFont='sans-serif'
    ).configure_legend(
        labelFont='sans-serif',
        titleFont='sans-serif'
    )

    st.altair_chart(chart, use_container_width=True)
