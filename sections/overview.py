import pandas as pd
import streamlit as st

def show_kpi_metrics(filtered_df):
    """显示KPI指标"""
    st.markdown("""
    ### 📊 Real-time Performance Indicators
    
    These metrics update automatically based on your current filters. Use them to quickly assess:
    - **Overall dataset size** and representativeness
    - **Average performance levels** for benchmarking
    - **Content characteristics** like average duration
    - **Account verification status** distribution
    """)
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_videos = len(filtered_df)
        st.metric("Total Videos", f"{total_videos:,}")
        st.caption("Number of videos in current selection")

    with col2:
        if 'video_view_count_clean' in filtered_df.columns and not filtered_df['video_view_count_clean'].isna().all():
            avg_views = filtered_df['video_view_count_clean'].mean()
            st.metric("Average Views", f"{avg_views:,.0f}")
            st.caption("Mean view count across selected videos")
        else:
            st.metric("Average Views", "N/A")
            st.caption("View count data not available")

    with col3:
        if 'video_duration_sec_clean' in filtered_df.columns and not filtered_df['video_duration_sec_clean'].isna().all():
            avg_duration = filtered_df['video_duration_sec_clean'].mean()
            st.metric("Average Duration", f"{avg_duration:.1f}s")
            st.caption("Mean video length in seconds")
        else:
            st.metric("Average Duration", "N/A")
            st.caption("Duration data not available")

    with col4:
        if 'verified_status' in filtered_df.columns:
            verified_count = len(filtered_df[filtered_df['verified_status'] == 'verified'])
            verified_percentage = (verified_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
            st.metric("Verified Accounts", f"{verified_percentage:.1f}%")
            st.caption("Percentage of verified creator accounts")
        else:
            st.metric("Verified Accounts", "N/A")
            st.caption("Verification status data not available")


def show_data_quality_report(df):
    """显示数据质量报告"""
    with st.expander("🔍 Data Quality Report"):
        st.markdown("""
        ### 📈 Data Quality Assessment
        
        This report helps you understand the completeness and reliability of your dataset:
        - **Column-wise completeness**: Percentage of non-null values for key metrics
        - **Data sample**: Preview of actual data structure
        - **Quality indicators**: Identify potential data issues
        
        **Interpretation Guide:**
        - **Null % < 5%**: Excellent data quality
        - **Null % 5-20%**: Good, consider impact on analysis
        - **Null % > 20%**: May require careful interpretation
        """)
        
        st.subheader("📋 Data Quality Summary")

        quality_data = []
        numeric_columns = ['video_view_count_clean', 'video_like_count_clean', 'video_share_count_clean',
                           'video_download_count_clean', 'video_comment_count_clean', 'video_duration_sec_clean']

        for col in numeric_columns:
            if col in df.columns:
                total_count = len(df)
                non_null_count = df[col].count()
                null_percentage = (total_count - non_null_count) / total_count * 100
                quality_data.append({
                    'Column': col.replace('_clean', '').replace('_', ' ').title(),
                    'Total Records': total_count,
                    'Non-Null Records': non_null_count,
                    'Null Percentage': f"{null_percentage:.2f}%",
                    'Data Quality': "✅ Good" if null_percentage < 5 else "⚠️ Moderate" if null_percentage < 20 else "❌ Poor"
                })

        if quality_data:
            quality_df = pd.DataFrame(quality_data)
            st.dataframe(quality_df, use_container_width=True)
            
            # 添加数据质量建议
            poor_quality_cols = [row['Column'] for row in quality_data if row['Null Percentage'].endswith('%') and float(row['Null Percentage'].replace('%', '')) >= 20]
            if poor_quality_cols:
                st.warning(f"**Note**: The following columns have significant missing data: {', '.join(poor_quality_cols)}. Results involving these metrics should be interpreted with caution.")

        # 显示数据样本
        st.subheader("👀 Data Sample Preview")
        st.markdown("First 10 rows of the dataset (showing key columns only):")
        
        # 选择关键列显示
        key_columns = [col for col in ['video_id', 'verified_status', 'author_ban_status', 'video_view_count_clean', 
                                      'video_duration_sec_clean', 'content_category'] if col in df.columns]
        if key_columns:
            st.dataframe(df[key_columns].head(10), use_container_width=True)
        else:
            st.dataframe(df.head(10), use_container_width=True)
            
        st.caption("This preview helps you understand the data structure and verify filter applications")