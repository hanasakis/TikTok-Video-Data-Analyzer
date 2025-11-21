import pandas as pd
import streamlit as st
import os
from datetime import datetime
import base64


@st.cache_data
def load_data():
    """加载数据"""
    try:
        df = pd.read_csv('tiktok_dataset.csv')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


def get_license_text():
    """返回许可证文本"""
    return """
    ### Data License and Usage
    This application uses TikTok video data for analytical purposes only.
    All data is used in compliance with applicable terms and conditions.
    """


def generate_csv_data(df):
    """生成CSV数据但不保存到文件"""
    return df.to_csv(index=False).encode('utf-8')


def save_data_to_directory(df, filename_prefix="tiktok_data"):
    """保存数据到data目录，返回文件路径"""
    # 确保data目录存在
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 生成文件名，包含时间戳以避免覆盖
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    filepath = os.path.join(data_dir, filename)

    # 保存到data目录
    df.to_csv(filepath, index=False)
    return filepath


def save_and_download_data(df, filename_prefix="filtered_tiktok_data", save_to_directory=False):
    """
    生成下载数据，可选择是否保存到目录

    参数:
        df: 要保存的DataFrame
        filename_prefix: 文件名前缀
        save_to_directory: 是否保存到data目录
    """
    # 生成CSV数据
    csv_data = generate_csv_data(df)

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"

    filepath = None
    if save_to_directory:
        filepath = save_data_to_directory(df, filename_prefix)

    return csv_data, filename, filepath


def load_icon(icon_name, size=16):
    """加载图标并返回HTML格式"""
    icon_path = f"assets/{icon_name}"
    if os.path.exists(icon_path):
        with open(icon_path, "rb") as icon_file:
            icon_data = base64.b64encode(icon_file.read()).decode()
        return f'<img src="data:image/x-icon;base64,{icon_data}" width="{size}" height="{size}">'
    else:
        # 如果图标不存在，返回一个默认的emoji
        icon_mapping = {
            "aim.ico": "🎯",
            "bar_chart.ico": "📊",
            "document.ico": "📄",
            "line_chart.ico": "📈",
            "phone.ico": "📱",
            "rocket.ico": "🚀",
            "search.ico": "🔍"
        }
        emoji = icon_mapping.get(icon_name, "📄")
        # 去除可能的换行符和空白字符
        return emoji.strip().replace('\n', '').replace('\r', '')


def display_icon(icon_name, size=16):
    """显示图标（使用HTML）"""
    icon_html = load_icon(icon_name, size)
    st.markdown(icon_html, unsafe_allow_html=True)


def get_icon_html(icon_name, size=16):
    """获取图标的HTML代码"""
    return load_icon(icon_name, size)