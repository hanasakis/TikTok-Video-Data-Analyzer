import streamlit as st
import pandas as pd
from utils.viz import *
from utils.prep import analyze_sentiment
from utils.io import generate_csv_data, save_data_to_directory  # 导入新函数
# ... 其余代码保持不变


def show_performance_metrics_tab(filtered_df):
    """显示性能指标标签页"""
    st.subheader("Video Performance Metrics")

    performance_metrics = ['video_view_count_clean', 'video_like_count_clean', 'video_share_count_clean',
                           'video_download_count_clean', 'video_comment_count_clean']

    col1, col2 = st.columns(2)

    with col1:
        # Views distribution
        fig_views = create_histogram(
            filtered_df,
            'video_view_count_clean',
            'Distribution of Video Views',
            'View Count'
        )
        if fig_views:
            st.plotly_chart(fig_views, use_container_width=True)

    with col2:
        # Duration distribution
        fig_duration = create_histogram(
            filtered_df,
            'video_duration_sec_clean',
            'Distribution of Video Duration',
            'Duration (seconds)'
        )
        if fig_duration:
            st.plotly_chart(fig_duration, use_container_width=True)

    # Metrics correlation
    st.subheader("Metrics Correlation")

    available_metrics = [metric for metric in performance_metrics if
                         metric in filtered_df.columns and not filtered_df[metric].isna().all()]

    if len(available_metrics) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            metric1 = st.selectbox("Select first metric:", available_metrics)
        with col2:
            other_metrics = [m for m in available_metrics if m != metric1]
            metric2 = st.selectbox("Select second metric:", other_metrics, index=min(1, len(other_metrics) - 1))

        if metric1 and metric2:
            fig_scatter = create_scatter_plot(
                filtered_df,
                metric1,
                metric2,
                f'{metric1.replace("_clean", "")} vs {metric2.replace("_clean", "")}'
            )
            if fig_scatter:
                st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Need at least 2 valid metrics for correlation analysis")


def show_user_analysis_tab(filtered_df):
    """显示用户分析标签页"""
    st.subheader("User Status Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Verified status distribution
        if 'verified_status' in filtered_df.columns:
            verified_counts = filtered_df['verified_status'].value_counts()
            fig_verified = create_pie_chart(
                verified_counts.values,
                verified_counts.index,
                'Verified Status Distribution'
            )
            st.plotly_chart(fig_verified, use_container_width=True)
        else:
            st.info("Verified status data not available")

    with col2:
        # Ban status distribution
        if 'author_ban_status' in filtered_df.columns:
            ban_counts = filtered_df['author_ban_status'].value_counts()
            fig_ban = create_pie_chart(
                ban_counts.values,
                ban_counts.index,
                'Author Ban Status Distribution'
            )
            st.plotly_chart(fig_ban, use_container_width=True)
        else:
            st.info("Ban status data not available")

    # Status impact on performance
    st.subheader("Status Impact on Video Performance")

    available_performance_metrics = [metric for metric in
                                     ['video_view_count_clean', 'video_like_count_clean', 'video_share_count_clean']
                                     if metric in filtered_df.columns and not filtered_df[metric].isna().all()]

    if available_performance_metrics:
        status_metric = st.selectbox("Select performance metric:", available_performance_metrics)

        col1, col2 = st.columns(2)

        with col1:
            if 'verified_status' in filtered_df.columns:
                fig_status = create_box_plot(
                    filtered_df,
                    'verified_status',
                    status_metric,
                    f'{status_metric.replace("_clean", "")} by Verified Status'
                )
                if fig_status:
                    st.plotly_chart(fig_status, use_container_width=True)

        with col2:
            if 'author_ban_status' in filtered_df.columns:
                fig_ban_impact = create_box_plot(
                    filtered_df,
                    'author_ban_status',
                    status_metric,
                    f'{status_metric.replace("_clean", "")} by Ban Status'
                )
                if fig_ban_impact:
                    st.plotly_chart(fig_ban_impact, use_container_width=True)
    else:
        st.info("No performance metrics available for status impact analysis")


def show_content_analysis_tab(filtered_df):
    """显示内容分析标签页"""
    st.subheader("Content Analysis")

    # Content category analysis
    if 'content_category' in filtered_df.columns:
        col1, col2 = st.columns(2)

        with col1:
            category_counts = filtered_df['content_category'].value_counts()
            fig_category = create_pie_chart(
                category_counts.values,
                category_counts.index,
                'Content Category Distribution'
            )
            st.plotly_chart(fig_category, use_container_width=True)

        with col2:
            fig_category_bar = create_bar_chart(
                category_counts.index,
                category_counts.values,
                'Content Categories by Video Count'
            )
            st.plotly_chart(fig_category_bar, use_container_width=True)
    else:
        st.info("Content category data not available")

    # Word cloud
    st.subheader("Video Transcription Word Cloud")

    if 'video_transcription_text' in filtered_df.columns:
        if st.button("Generate Word Cloud"):
            all_text = ' '.join(filtered_df['video_transcription_text'].dropna().astype(str))
            fig_wordcloud = create_wordcloud(all_text)
            if fig_wordcloud:
                st.pyplot(fig_wordcloud)
    else:
        st.info("Transcription text data not available")

    # Sentiment analysis
    st.subheader("Content Sentiment Analysis")

    if 'video_transcription_text' in filtered_df.columns:
        if st.button("Analyze Sentiment"):
            with st.spinner('Performing sentiment analysis...'):
                sentiment_df = filtered_df.copy()
                sentiment_df['transcription_sentiment'] = sentiment_df['video_transcription_text'].apply(
                    analyze_sentiment)

            col1, col2 = st.columns(2)

            with col1:
                if not sentiment_df['transcription_sentiment'].isna().all():
                    fig_sentiment = create_histogram(
                        sentiment_df,
                        'transcription_sentiment',
                        'Distribution of Transcription Sentiment',
                        'Sentiment Score'
                    )
                    if fig_sentiment:
                        st.plotly_chart(fig_sentiment, use_container_width=True)
                else:
                    st.info("No sentiment data available")

            with col2:
                if not sentiment_df['transcription_sentiment'].isna().all():
                    # Classify sentiments
                    sentiment_labels = []
                    for sentiment in sentiment_df['transcription_sentiment'].dropna():
                        if sentiment > 0.1:
                            sentiment_labels.append('Positive')
                        elif sentiment < -0.1:
                            sentiment_labels.append('Negative')
                        else:
                            sentiment_labels.append('Neutral')

                    if sentiment_labels:
                        sentiment_counts = pd.Series(sentiment_labels).value_counts()
                        fig_sentiment_pie = create_pie_chart(
                            sentiment_counts.values,
                            sentiment_counts.index,
                            'Sentiment Distribution'
                        )
                        st.plotly_chart(fig_sentiment_pie, use_container_width=True)
                else:
                    st.info("No sentiment data available")
    else:
        st.info("Transcription text data not available for sentiment analysis")


def show_engagement_analysis_tab(filtered_df):
    """显示互动分析标签页"""
    st.subheader("Engagement Analysis")

    engagement_metrics = ['like_rate', 'share_rate', 'comment_rate']
    available_engagement_metrics = [metric for metric in engagement_metrics if
                                    metric in filtered_df.columns and not filtered_df[metric].isna().all()]

    if available_engagement_metrics:
        col1, col2 = st.columns(2)

        with col1:
            # Engagement rates distribution
            if 'like_rate' in filtered_df.columns and not filtered_df['like_rate'].isna().all():
                like_data = filtered_df[filtered_df['like_rate'] < filtered_df['like_rate'].quantile(0.95)]
                if not like_data.empty:
                    fig_like_rate = create_histogram(
                        like_data,
                        'like_rate',
                        'Distribution of Like Rates',
                        'Like Rate'
                    )
                    if fig_like_rate:
                        st.plotly_chart(fig_like_rate, use_container_width=True)

        with col2:
            if 'share_rate' in filtered_df.columns and not filtered_df['share_rate'].isna().all():
                share_data = filtered_df[filtered_df['share_rate'] < filtered_df['share_rate'].quantile(0.95)]
                if not share_data.empty:
                    fig_share_rate = create_histogram(
                        share_data,
                        'share_rate',
                        'Distribution of Share Rates',
                        'Share Rate'
                    )
                    if fig_share_rate:
                        st.plotly_chart(fig_share_rate, use_container_width=True)
    else:
        st.info("Engagement rate data not available")

    # High engagement videos analysis
    st.subheader("High Engagement Videos Analysis")

    if 'video_view_count_clean' in filtered_df.columns and not filtered_df['video_view_count_clean'].isna().all():
        engagement_threshold = st.slider("Engagement Threshold (Percentile)", 50, 95, 80)

        high_engagement_threshold = filtered_df['video_view_count_clean'].quantile(engagement_threshold / 100)
        high_engagement_videos = filtered_df[filtered_df['video_view_count_clean'] >= high_engagement_threshold]

        st.write(
            f"High engagement videos: {len(high_engagement_videos)} ({len(high_engagement_videos) / len(filtered_df) * 100:.1f}%)")

        col1, col2 = st.columns(2)

        with col1:
            if 'verified_status' in high_engagement_videos.columns:
                high_engagement_verified = high_engagement_videos['verified_status'].value_counts()
                if not high_engagement_verified.empty:
                    fig_high_verified = create_pie_chart(
                        high_engagement_verified.values,
                        high_engagement_verified.index,
                        'Verified Status in High Engagement Videos'
                    )
                    st.plotly_chart(fig_high_verified, use_container_width=True)

        with col2:
            if 'content_category' in high_engagement_videos.columns:
                high_engagement_category = high_engagement_videos['content_category'].value_counts().head(10)
                if not high_engagement_category.empty:
                    fig_high_category = create_bar_chart(
                        high_engagement_category.index,
                        high_engagement_category.values,
                        'Top Categories in High Engagement Videos'
                    )
                    st.plotly_chart(fig_high_category, use_container_width=True)
    else:
        st.info("View count data not available for engagement analysis")


def show_dashboard_tab(filtered_df):
    """显示仪表板标签页"""
    st.subheader("Comprehensive Dashboard")

    fig_dashboard = create_comprehensive_dashboard(filtered_df)
    if fig_dashboard:
        st.plotly_chart(fig_dashboard, use_container_width=True)


def show_advanced_analytics(filtered_df):
    """显示高级分析"""
    st.header("🔍 Advanced Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Performance statistics by category
        st.subheader("Performance Statistics by Category")

        if ('content_category' in filtered_df.columns and
                'video_view_count_clean' in filtered_df.columns and
                not filtered_df['video_view_count_clean'].isna().all()):

            performance_data = filtered_df.dropna(subset=['video_view_count_clean'])
            performance_stats = performance_data.groupby('content_category')['video_view_count_clean'].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(2).sort_values('count', ascending=False).head(10)

            st.dataframe(performance_stats)
        else:
            st.info("Performance or category data not available")

    with col2:
        # Engagement statistics by verified status
        st.subheader("Engagement Statistics by Verified Status")

        if ('verified_status' in filtered_df.columns and
                'like_rate' in filtered_df.columns and
                not filtered_df['like_rate'].isna().all()):

            engagement_data = filtered_df.dropna(subset=['like_rate'])
            engagement_stats = engagement_data.groupby('verified_status')['like_rate'].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(4).sort_values('count', ascending=False)

            st.dataframe(engagement_stats)
        else:
            st.info("Engagement or verified status data not available")


# ... 其他函数保持不变 ...

def show_raw_data_section(filtered_df):
    """显示原始数据部分"""
    st.header("📋 Raw Data")

    with st.expander("View Filtered Data"):
        if not filtered_df.empty:
            st.dataframe(filtered_df.head(1000))

            # Show basic statistics
            st.subheader("Data Summary")
            st.write(f"Total rows: {len(filtered_df)}")
            st.write(f"Total columns: {len(filtered_df.columns)}")

            # 添加保存和下载按钮
            col1, col2 = st.columns(2)

            with col1:
                # 保存到data目录的按钮
                if st.button("💾 Save Data to Data Directory", key="save_data_btn"):
                    filepath = save_data_to_directory(filtered_df, filename_prefix="tiktok_filtered_data")
                    st.success(f"Data saved to: {filepath}")

            with col2:
                # 下载按钮 - 只在点击时生成数据
                csv_data = generate_csv_data(filtered_df)
                timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tiktok_filtered_data_{timestamp}.csv"

                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    key="download_data_btn"
                )
        else:
            st.info("No data available to display")


# ... 其他函数保持不变 ...


def show_deep_dives(filtered_df):
    """显示深度分析部分"""
    st.header("📈 Video Analysis")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Performance Metrics", "User Analysis", "Content Analysis", "Engagement Analysis", "Dashboard"])

    with tab1:
        show_performance_metrics_tab(filtered_df)

    with tab2:
        show_user_analysis_tab(filtered_df)

    with tab3:
        show_content_analysis_tab(filtered_df)

    with tab4:
        show_engagement_analysis_tab(filtered_df)

    with tab5:
        show_dashboard_tab(filtered_df)

    # 高级分析和原始数据
    show_advanced_analytics(filtered_df)
    show_raw_data_section(filtered_df)