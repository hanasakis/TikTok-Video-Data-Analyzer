import pandas as pd
import streamlit as st


def show_kpi_metrics(filtered_df):
    """显示KPI指标"""
    # 移除这里的st.header("📊 Key Metrics")，因为在app.py中已经添加了

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_videos = len(filtered_df)
        st.metric("Total Videos", f"{total_videos:,}")

    with col2:
        if 'video_view_count_clean' in filtered_df.columns and not filtered_df['video_view_count_clean'].isna().all():
            avg_views = filtered_df['video_view_count_clean'].mean()
            st.metric("Average Views", f"{avg_views:,.0f}")
        else:
            st.metric("Average Views", "N/A")

    with col3:
        if 'video_duration_sec_clean' in filtered_df.columns and not filtered_df[
            'video_duration_sec_clean'].isna().all():
            avg_duration = filtered_df['video_duration_sec_clean'].mean()
            st.metric("Average Duration", f"{avg_duration:.1f}s")
        else:
            st.metric("Average Duration", "N/A")

    with col4:
        if 'verified_status' in filtered_df.columns:
            verified_count = len(filtered_df[filtered_df['verified_status'] == 'verified'])
            verified_percentage = (verified_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
            st.metric("Verified Accounts", f"{verified_percentage:.1f}%")
        else:
            st.metric("Verified Accounts", "N/A")


def show_data_quality_report(df):
    """显示数据质量报告"""
    with st.expander("Data Quality Report"):
        st.subheader("Data Quality Summary")

        quality_data = []
        numeric_columns = ['video_view_count_clean', 'video_like_count_clean', 'video_share_count_clean',
                           'video_download_count_clean', 'video_comment_count_clean', 'video_duration_sec_clean']

        for col in numeric_columns:
            if col in df.columns:
                total_count = len(df)
                non_null_count = df[col].count()
                null_percentage = (total_count - non_null_count) / total_count * 100
                quality_data.append({
                    'Column': col.replace('_clean', ''),
                    'Total': total_count,
                    'Non-Null': non_null_count,
                    'Null %': f"{null_percentage:.2f}%"
                })

        if quality_data:
            st.dataframe(pd.DataFrame(quality_data))

        # 显示数据样本
        st.subheader("Data Sample (First 10 Rows)")
        st.dataframe(df.head(10))