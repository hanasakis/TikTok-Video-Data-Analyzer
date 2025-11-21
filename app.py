import pandas as pd
import numpy as np
import streamlit as st
import warnings
import os

# 导入自定义模块
from utils.io import load_data
from utils.prep import preprocess_data
from sections.intro import show_intro, show_data_caveats
from sections.overview import show_kpi_metrics, show_data_quality_report
from sections.deep_dives import show_deep_dives
from sections.conclusions import show_conclusions, show_implications

warnings.filterwarnings('ignore')

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="TikTok Video Data Analyzer",
    page_icon="📱",
    layout="wide"
)


# -----------------------------
# Helper functions for images
# -----------------------------
def display_image_in_sidebar(image_path, width=150):
    """在侧边栏显示图片 - 使用st.image"""
    try:
        if os.path.exists(image_path):
            st.sidebar.image(image_path, width=width)
        else:
            st.sidebar.warning(f"图片文件不存在: {image_path}")
    except Exception as e:
        st.sidebar.error(f"加载图片时出错 {image_path}: {e}")


# -----------------------------
# Sidebar content
# -----------------------------
def setup_sidebar():
    """设置侧边栏内容"""
    st.sidebar.header("📋 Project Information")

    # 添加项目信息
    st.sidebar.markdown("""
    **Prof:** Mano Mathew  
    **Student:** Jianyu Li  
    **Student ID:** 20252230  
    **Email:** jianyu.li@efrei.net  
    **Github:** [hanasakis](https://github.com/hanasakis)  
    **GitHub Repository:** [TikTok-Video-Data-Analyzer](https://github.com/hanasakis/TikTok-Video-Data-Analyzer)  
    **Dataset:** [Dataset-From-Tiktok](https://www.kaggle.com/datasets/erikvdven/tiktok-dataset)
    """)

    st.sidebar.markdown("---")

    # 添加项目介绍
    st.sidebar.markdown("""
    **Introduction:**
    TikTok's dataset of user-reported claims enables predictive modeling to distinguish claims from opinions, 
    reducing backlog for educational data analysis.
    """)

    st.sidebar.markdown("---")

    # 添加图片
    st.sidebar.subheader("🏫 Partner Institutions")

    # 检查并显示图片 - 使用替代方案
    st.sidebar.markdown("**École d'Ingénieur Généraliste en Informatique et Technologies du Numérique:**")
    if os.path.exists("assets/eFrei.png"):
        display_image_in_sidebar("assets/eFrei.png", width=120)
    else:
        st.sidebar.error("❌ eFrei.png not found in assets directory")
        # 显示替代文本或占位符
        st.sidebar.info("请将eFrei.png文件放入assets目录")

    st.sidebar.markdown("")  # 添加空行作为间距

    st.sidebar.markdown("**Wuhan University of Technology:**")
    if os.path.exists("assets/WUT.png"):
        display_image_in_sidebar("assets/WUT.png", width=120)
    else:
        st.sidebar.error("❌ WUT.png not found in assets directory")
        # 显示替代文本或占位符
        st.sidebar.info("请将WUT.png文件放入assets目录")


# -----------------------------
# Main interface filters
# -----------------------------
def setup_main_filters(df):
    """在主界面设置过滤器"""
    st.header("🔍 Data Filters")

    with st.expander("Filter Options", expanded=True):
        col1, col2, col3 = st.columns(3)

        filters = {}

        with col1:
            # Status filters
            if 'verified_status' in df.columns:
                filters['verified_options'] = st.multiselect(
                    "✅ Verified Status",
                    options=df['verified_status'].unique(),
                    default=df['verified_status'].unique()
                )
            else:
                filters['verified_options'] = []

            if 'author_ban_status' in df.columns:
                filters['ban_options'] = st.multiselect(
                    "🚫 Author Ban Status",
                    options=df['author_ban_status'].unique(),
                    default=df['author_ban_status'].unique()
                )
            else:
                filters['ban_options'] = []

        with col2:
            if 'claim_status' in df.columns:
                filters['claim_options'] = st.multiselect(
                    "📋 Claim Status",
                    options=df['claim_status'].unique(),
                    default=df['claim_status'].unique()
                )
            else:
                filters['claim_options'] = []

            # Content category filter
            if 'content_category' in df.columns:
                filters['category_options'] = st.multiselect(
                    "📁 Content Category",
                    options=df['content_category'].unique(),
                    default=df['content_category'].unique()
                )
            else:
                filters['category_options'] = []

        with col3:
            # Video duration filter
            if 'video_duration_sec_clean' in df.columns:
                duration_data = df['video_duration_sec_clean'].dropna()
                if not duration_data.empty:
                    duration_min = float(duration_data.min())
                    duration_max = float(duration_data.max())
                    filters['min_duration'], filters['max_duration'] = st.slider(
                        "⏱️ Video Duration (seconds)",
                        min_value=duration_min,
                        max_value=duration_max,
                        value=(0.0, min(duration_max, 60.0)),
                        help="Filter videos by duration in seconds"
                    )
                else:
                    filters['min_duration'], filters['max_duration'] = (0, 60)
                    st.warning("No duration data available")
            else:
                filters['min_duration'], filters['max_duration'] = (0, 60)

            # View count filter
            if 'video_view_count_clean' in df.columns:
                view_data = df['video_view_count_clean'].dropna()
                if not view_data.empty:
                    view_min = float(view_data.min())
                    view_max = float(view_data.max())
                    filters['min_views'], filters['max_views'] = st.slider(
                        "👀 View Count Range",
                        min_value=view_min,
                        max_value=view_max,
                        value=(0.0, min(view_max, float(view_data.quantile(0.95)) if not view_data.empty else 1000000)),
                        help="Filter videos by view count range"
                    )
                else:
                    filters['min_views'], filters['max_views'] = (0, 1000000)
                    st.warning("No view count data available")
            else:
                filters['min_views'], filters['max_views'] = (0, 1000000)

    return filters


def apply_filters(df, filters):
    """应用过滤器"""
    filtered_df = df.copy()

    if filters['verified_options']:
        filtered_df = filtered_df[filtered_df['verified_status'].isin(filters['verified_options'])]

    if filters['ban_options']:
        filtered_df = filtered_df[filtered_df['author_ban_status'].isin(filters['ban_options'])]

    if filters['claim_options']:
        filtered_df = filtered_df[filtered_df['claim_status'].isin(filters['claim_options'])]

    if filters['category_options'] and 'content_category' in df.columns:
        filtered_df = filtered_df[filtered_df['content_category'].isin(filters['category_options'])]

    if 'video_duration_sec_clean' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['video_duration_sec_clean'] >= filters['min_duration']) &
            (filtered_df['video_duration_sec_clean'] <= filters['max_duration'])
            ]

    if 'video_view_count_clean' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['video_view_count_clean'] >= filters['min_views']) &
            (filtered_df['video_view_count_clean'] <= filters['max_views'])
            ]

    return filtered_df


# -----------------------------
# Main application flow
# -----------------------------
def main():
    # 设置侧边栏内容
    setup_sidebar()

    # 加载数据
    df_raw = load_data()

    if df_raw.empty:
        st.error("No data loaded. Please check if tiktok_dataset.csv exists in the same directory.")
        st.stop()

    # 预处理数据
    df = preprocess_data(df_raw)

    # 显示介绍部分
    show_intro()
    show_data_caveats()

    # 显示KPI指标（使用原始数据）
    st.header("📊 Key Metrics")
    show_kpi_metrics(df)

    # 显示数据质量报告
    show_data_quality_report(df)

    # 设置主界面过滤器
    st.markdown("---")  # 添加分隔线
    filters = setup_main_filters(df)

    # 应用过滤器
    filtered_df = apply_filters(df, filters)

    # 显示过滤结果统计
    st.success(f"✅ Filtered dataset: {len(filtered_df)} videos (from original {len(df)} videos)")

    # 显示深度分析和结论（使用过滤后的数据）
    show_deep_dives(filtered_df)
    show_conclusions(filtered_df)
    show_implications()

    # Footer
    st.markdown("---")
    st.caption("TikTok Video Data Analyzer | Built with Streamlit")
    st.caption("Project by Jianyu Li (20252230) | Supervised by Prof. Mano Mathew")


if __name__ == "__main__":
    main()