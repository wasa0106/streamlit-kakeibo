import streamlit as st

def get_card_style():
    """統一されたカードスタイルを返す"""
    return """
        border: 1px solid #E8EAED;
        border-radius: 8px;
        padding: 20px;
        background-color: #FFFFFF;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    """

def get_metric_card_style(color="#769CDF"):
    """メトリクスカード用のスタイル"""
    return f"""
        border: 1px solid #E8EAED;
        border-radius: 8px;
        padding: 24px;
        background-color: #FFFFFF;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.06);
        margin-bottom: 16px;
        border-left: 4px solid {color};
    """

def get_number_style():
    """数値表示用のスタイル"""
    return """
        font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
        font-weight: 500;
    """

def apply_custom_css():
    """カスタムCSSを適用"""
    st.markdown("""
    <style>
    /* 見出しのスタイル */
    .main h1 {
        font-size: 2.0rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-bottom: 1.5rem;
    }
    
    .main h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
    }
    
    .main h3 {
        font-size: 1.25rem;
        font-weight: 500;
        color: #1A1A1A;
        margin-bottom: 1rem;
    }
    
    /* データフレームのスタイル */
    .dataframe {
        font-size: 0.9rem;
        border: none !important;
    }
    
    .dataframe th {
        background-color: #F7F8FA !important;
        font-weight: 600 !important;
        text-align: left !important;
        padding: 12px !important;
        border-bottom: 2px solid #E8EAED !important;
    }
    
    .dataframe td {
        padding: 10px !important;
        border-bottom: 1px solid #F0F2F4 !important;
    }
    
    /* 数値の等幅フォント */
    .number-display {
        font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
        font-weight: 500;
    }
    
    /* マルチセレクトのスタイル */
    .stMultiSelect > div {
        border-radius: 8px;
        border-color: #E8EAED;
    }
    
    /* カード内の余白調整 */
    .element-container {
        margin-bottom: 0.75rem;
    }
    
    /* Altairチャートの角丸 */
    .vega-embed {
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)