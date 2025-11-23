import streamlit as st
import pandas as pd
from utils.viz import *
from utils.prep import analyze_sentiment
from utils.io import generate_csv_data, save_data_to_directory

def show_performance_metrics_tab(filtered_df):
    """显示性能指标标签页"""
    st.markdown("""
    ### 🎬 Video Performance Analysis
    
    This section helps you understand how videos perform across different metrics:
    - **Distribution patterns**: How views, likes, and other metrics are spread
    - **Duration analysis**: Optimal video length insights
    - **Metric relationships**: How different performance indicators correlate
    
    **Key Questions Answered:**
    - What is the typical view count distribution?
    - Is there an optimal video duration for engagement?
    - How do different performance metrics relate to each other?
    """)
    
    st.subheader("📊 Performance Distributions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 👀 View Count Distribution
        - Shows how views are distributed across videos
        - Right-skewed distribution is typical (few viral videos)
        - Helps identify what constitutes 'high performance'
        """)
        if 'video_view_count_clean' in filtered_df.columns:
            fig_views = create_histogram(
                filtered_df,
                'video_view_count_clean',
                'Distribution of Video Views',
                'View Count'
            )
            if fig_views:
                st.plotly_chart(fig_views, use_container_width=True)
                st.caption("Most videos get modest views, with a few high-performing outliers")
        else:
            st.info("View count data not available for analysis")

    with col2:
        st.markdown("""
        #### ⏱️ Video Duration Distribution
        - Analyzes typical video lengths
        - Helps identify preferred duration ranges
        - Longer doesn't always mean better performance
        """)
        if 'video_duration_sec_clean' in filtered_df.columns:
            fig_duration = create_histogram(
                filtered_df,
                'video_duration_sec_clean',
                'Distribution of Video Duration',
                'Duration (seconds)'
            )
            if fig_duration:
                st.plotly_chart(fig_duration, use_container_width=True)
                st.caption("Typical TikTok video durations range from 15-60 seconds")
        else:
            st.info("Video duration data not available")

    # Metrics correlation
    st.subheader("🔗 Metrics Correlation Analysis")
    st.markdown("""
    Explore relationships between different performance indicators:
    - **Positive correlation**: Metrics that move together
    - **No correlation**: Independent metrics
    - **Outlier identification**: Exceptional performers
    
    **Practical Applications:**
    - Identify which metrics best predict overall success
    - Understand engagement patterns across different content types
    - Spot unusual performance patterns worth investigating
    """)
    
    available_metrics = [metric for metric in
                         ['video_view_count_clean', 'video_like_count_clean', 'video_share_count_clean',
                          'video_download_count_clean', 'video_comment_count_clean']
                         if metric in filtered_df.columns and not filtered_df[metric].isna().all()]

    if len(available_metrics) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            metric1 = st.selectbox("Select first metric:", available_metrics, 
                                 help="Choose the primary metric for comparison")
        with col2:
            other_metrics = [m for m in available_metrics if m != metric1]
            metric2 = st.selectbox("Select second metric:", other_metrics, 
                                 index=min(1, len(other_metrics) - 1),
                                 help="Choose the secondary metric to compare against")
        
        st.markdown(f"### 📈 {metric1.replace('_clean', '').replace('_', ' ').title()} vs {metric2.replace('_clean', '').replace('_', ' ').title()}")

        if metric1 and metric2:
            fig_scatter = create_scatter_plot(
                filtered_df,
                metric1,
                metric2,
                f'{metric1.replace("_clean", "").replace("_", " ").title()} vs {metric2.replace("_clean", "").replace("_", " ").title()}'
            )
            if fig_scatter:
                st.plotly_chart(fig_scatter, use_container_width=True)
                st.caption("Each point represents a video. Clustered points indicate strong correlation")
                
                # 添加简单的相关性分析
                correlation = filtered_df[metric1].corr(filtered_df[metric2])
                st.metric("Correlation Coefficient", f"{correlation:.3f}")
                if correlation > 0.7:
                    st.success("Strong positive correlation: These metrics tend to increase together")
                elif correlation > 0.3:
                    st.info("Moderate positive correlation")
                elif correlation > -0.3:
                    st.warning("Weak correlation: Metrics are largely independent")
                else:
                    st.error("Negative correlation: Metrics move in opposite directions")
    else:
        st.info("Need at least 2 valid metrics for correlation analysis. Check your data filters.")


def show_user_analysis_tab(filtered_df):
    """显示用户分析标签页"""
    st.markdown("""
    ### 👥 User Account Analysis
    
    Understand how account characteristics influence video performance:
    - **Verified vs Non-verified**: Impact of account verification
    - **Ban status analysis**: Performance differences by account standing
    - **Status-performance relationships**: How account attributes affect engagement
    
    **Business Applications:**
    - Inform verification strategy decisions
    - Understand trust signals that drive performance
    - Identify healthy account behavior patterns
    """)
    
    st.subheader("📊 Account Status Distribution")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### ✅ Verified Status Distribution
        - Percentage of verified creator accounts
        - Verified accounts often have different performance patterns
        - Helps understand platform influencer composition
        """)
        if 'verified_status' in filtered_df.columns:
            verified_counts = filtered_df['verified_status'].value_counts()
            fig_verified = create_pie_chart(
                verified_counts.values,
                verified_counts.index,
                'Verified Status Distribution'
            )
            st.plotly_chart(fig_verified, use_container_width=True)
            st.caption(f"Verified accounts: {verified_counts.get('verified', 0)} | Non-verified: {verified_counts.get('not verified', 0)}")
        else:
            st.info("Verified status data not available in current dataset")

    with col2:
        st.markdown("""
        #### 🚫 Ban Status Distribution
        - Distribution of account standing status
        - Banned vs active account performance comparisons
        - Platform health and content moderation insights
        """)
        if 'author_ban_status' in filtered_df.columns:
            ban_counts = filtered_df['author_ban_status'].value_counts()
            fig_ban = create_pie_chart(
                ban_counts.values,
                ban_counts.index,
                'Author Ban Status Distribution'
            )
            st.plotly_chart(fig_ban, use_container_width=True)
            st.caption("Monitor ban rates as a platform health indicator")
        else:
            st.info("Ban status data not available in current dataset")

    # Status impact on performance
    st.subheader("📈 Status Impact on Video Performance")
    st.markdown("""
    Compare performance metrics across different account statuses:
    - **Box plots** show distribution patterns and outliers
    - **Median lines** indicate typical performance levels
    - **Whiskers** show variability within each group
    
    **Interpretation Tips:**
    - Higher median = better typical performance
    - Larger boxes = more performance variability
    - Outliers = exceptional performing videos
    """)
    
    available_performance_metrics = [metric for metric in
                                     ['video_view_count_clean', 'video_like_count_clean', 'video_share_count_clean']
                                     if metric in filtered_df.columns and not filtered_df[metric].isna().all()]

    if available_performance_metrics:
        status_metric = st.selectbox("Select performance metric:", available_performance_metrics,
                                    help="Choose which performance metric to analyze by account status")
        
        metric_name = status_metric.replace('_clean', '').replace('_', ' ').title()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"#### 📊 {metric_name} by Verified Status")
            if 'verified_status' in filtered_df.columns:
                fig_status = create_box_plot(
                    filtered_df,
                    'verified_status',
                    status_metric,
                    f'{metric_name} by Verified Status'
                )
                if fig_status:
                    st.plotly_chart(fig_status, use_container_width=True)
                    st.caption("Compare performance between verified and non-verified accounts")
            else:
                st.info("Verified status data not available")

        with col2:
            st.markdown(f"#### 📊 {metric_name} by Ban Status")
            if 'author_ban_status' in filtered_df.columns:
                fig_ban_impact = create_box_plot(
                    filtered_df,
                    'author_ban_status',
                    status_metric,
                    f'{metric_name} by Ban Status'
                )
                if fig_ban_impact:
                    st.plotly_chart(fig_ban_impact, use_container_width=True)
                    st.caption("Analyze performance differences by account standing")
            else:
                st.info("Ban status data not available")
    else:
        st.info("No performance metrics available for status impact analysis. Check your data filters.")


def show_content_analysis_tab(filtered_df):
    """显示内容分析标签页"""
    st.markdown("""
    ### 📝 Content Analysis
    
    Dive deep into what types of content perform best:
    - **Content categorization**: Distribution across topics/themes
    - **Transcription insights**: Word frequency and sentiment analysis
    - **Performance by category**: Which content types resonate most
    
    **Content Strategy Applications:**
    - Identify high-performing content categories
    - Understand audience preferences and interests
    - Optimize content creation and curation strategies
    """)
    
    st.subheader("📂 Content Category Analysis")

    # Content category analysis
    if 'content_category' in filtered_df.columns:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 🥧 Content Category Distribution
            - Pie chart shows proportional representation
            - Helps understand content mix in your dataset
            - Identify over/under-represented categories
            """)
            category_counts = filtered_df['content_category'].value_counts()
            fig_category = create_pie_chart(
                category_counts.values,
                category_counts.index,
                'Content Category Distribution'
            )
            st.plotly_chart(fig_category, use_container_width=True)
            st.caption(f"Total categories: {len(category_counts)} | Most common: {category_counts.index[0]}")

        with col2:
            st.markdown("""
            #### 📊 Content Categories by Video Count
            - Bar chart for precise quantity comparisons
            - Easier to compare similar-sized categories
            - Identifies volume leaders clearly
            """)
            fig_category_bar = create_bar_chart(
                category_counts.index,
                category_counts.values,
                'Content Categories by Video Count'
            )
            st.plotly_chart(fig_category_bar, use_container_width=True)
            st.caption("Bar charts provide clearer comparison of similar values")
    else:
        st.info("Content category data not available. Categories are generated from transcription text.")

    # Word cloud
    st.subheader("☁️ Video Transcription Word Cloud")
    st.markdown("""
    Visualize the most frequent words in video transcriptions:
    - **Larger words** appear more frequently
    - **Common words** (the, and, etc.) are filtered out
    - **Theme identification** through prominent keywords
    
    **Usage Tips:**
    - Identify common topics and themes
    - Spot trending terminology and phrases
    - Understand content focus areas
    """)
    
    if 'video_transcription_text' in filtered_df.columns:
        if st.button("🔄 Generate Word Cloud", help="Click to generate/refresh the word cloud visualization"):
            with st.spinner('Generating word cloud from transcription text...'):
                all_text = ' '.join(filtered_df['video_transcription_text'].dropna().astype(str))
                if all_text.strip():
                    fig_wordcloud = create_wordcloud(all_text)
                    if fig_wordcloud:
                        st.pyplot(fig_wordcloud)
                        st.caption("Word size indicates frequency. Common stop words are filtered out.")
                else:
                    st.warning("No transcription text available for word cloud generation")
        else:
            st.info("Click the button above to generate a word cloud from video transcriptions")
    else:
        st.info("Transcription text data not available for word cloud analysis")

    # Sentiment analysis
    st.subheader("😊 Content Sentiment Analysis")
    st.markdown("""
    Analyze the emotional tone of video transcriptions:
    - **Sentiment scores**: Range from -1 (negative) to +1 (positive)
    - **Distribution analysis**: Overall sentiment patterns
    - **Categorization**: Positive, negative, neutral classification
    
    **Interpretation Guide:**
    - **Positive (>0.1)**: Upbeat, encouraging, happy content
    - **Neutral (-0.1 to 0.1)**: Factual, instructional, balanced content  
    - **Negative (<-0.1)**: Critical, concerning, negative content
    """)
    
    if 'video_transcription_text' in filtered_df.columns:
        if st.button("🔍 Analyze Sentiment", help="Perform sentiment analysis on transcription text"):
            with st.spinner('Analyzing sentiment in video transcriptions...'):
                sentiment_df = filtered_df.copy()
                sentiment_df['transcription_sentiment'] = sentiment_df['video_transcription_text'].apply(analyze_sentiment)

            st.success(f"Sentiment analysis complete! Analyzed {len(sentiment_df.dropna(subset=['transcription_sentiment']))} transcriptions")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Sentiment Score Distribution")
                if not sentiment_df['transcription_sentiment'].isna().all():
                    fig_sentiment = create_histogram(
                        sentiment_df,
                        'transcription_sentiment',
                        'Distribution of Transcription Sentiment',
                        'Sentiment Score'
                    )
                    if fig_sentiment:
                        st.plotly_chart(fig_sentiment, use_container_width=True)
                        st.caption("Distribution of sentiment scores across all analyzed transcriptions")
                else:
                    st.info("No sentiment data available after analysis")

            with col2:
                st.markdown("#### 🥧 Sentiment Category Distribution")
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
                        
                        # 显示情感统计
                        total = len(sentiment_labels)
                        positive_pct = (sentiment_counts.get('Positive', 0) / total) * 100
                        neutral_pct = (sentiment_counts.get('Neutral', 0) / total) * 100
                        negative_pct = (sentiment_counts.get('Negative', 0) / total) * 100
                        
                        st.metric("Positive Content", f"{positive_pct:.1f}%")
                        st.caption(f"Neutral: {neutral_pct:.1f}% | Negative: {negative_pct:.1f}%")
                else:
                    st.info("No sentiment categorization available")
        else:
            st.info("Click the button above to perform sentiment analysis on transcription text")
    else:
        st.info("Transcription text data not available for sentiment analysis")


def show_engagement_analysis_tab(filtered_df):
    """显示互动分析标签页"""
    st.markdown("""
    ### 💬 Engagement Analysis
    
    Understand how audiences interact with content:
    - **Engagement rates**: Like, share, and comment rates relative to views
    - **High-performance analysis**: Characteristics of top-performing content
    - **Audience behavior**: How viewers engage with different content types
    
    **Strategic Applications:**
    - Identify content that drives meaningful engagement
    - Understand what makes videos shareable and interactive
    - Optimize for engagement metrics that matter most
    """)
    
    st.subheader("📈 Engagement Rate Analysis")

    engagement_metrics = ['like_rate', 'share_rate', 'comment_rate']
    available_engagement_metrics = [metric for metric in engagement_metrics if
                                    metric in filtered_df.columns and not filtered_df[metric].isna().all()]

    if available_engagement_metrics:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 👍 Like Rate Distribution
            - Percentage of viewers who like videos
            - Measures content appreciation and enjoyment
            - High like rates indicate resonant content
            """)
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
                        avg_like_rate = like_data['like_rate'].mean()
                        st.metric("Average Like Rate", f"{avg_like_rate:.4f}")
                else:
                    st.info("No like rate data available after filtering extremes")
            else:
                st.info("Like rate data not available")

        with col2:
            st.markdown("""
            #### 🔄 Share Rate Distribution  
            - Percentage of viewers who share videos
            - Measures viral potential and shareability
            - High share rates indicate valuable/entertaining content
            """)
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
                        avg_share_rate = share_data['share_rate'].mean()
                        st.metric("Average Share Rate", f"{avg_share_rate:.4f}")
                else:
                    st.info("No share rate data available after filtering extremes")
            else:
                st.info("Share rate data not available")
    else:
        st.info("Engagement rate data not available. Rates require both engagement metrics and view counts.")

    # High engagement videos analysis
    st.subheader("🏆 High Engagement Videos Analysis")
    st.markdown("""
    Identify characteristics of top-performing videos:
    - **Threshold setting**: Define what constitutes 'high engagement'
    - **Comparative analysis**: How top videos differ from average
    - **Success patterns**: Common traits of high performers
    
    **Analysis Benefits:**
    - Learn from your most successful content
    - Identify replicable success patterns
    - Inform content strategy and creation decisions
    """)
    
    if 'video_view_count_clean' in filtered_df.columns and not filtered_df['video_view_count_clean'].isna().all():
        st.markdown("""
        **Adjust the slider to define high engagement threshold:**
        - Higher percentiles = more selective (only top performers)
        - Lower percentiles = broader high-performance category
        - 80th percentile is a common benchmark for 'high performing'
        """)
        
        engagement_threshold = st.slider("Engagement Threshold (Percentile)", 50, 95, 80,
                                       help="Set the percentile threshold for high engagement classification")

        high_engagement_threshold = filtered_df['video_view_count_clean'].quantile(engagement_threshold / 100)
        high_engagement_videos = filtered_df[filtered_df['video_view_count_clean'] >= high_engagement_threshold]

        st.success(f"**High engagement threshold**: {high_engagement_threshold:,.0f} views")
        st.metric("High Engagement Videos", 
                 f"{len(high_engagement_videos)} ({len(high_engagement_videos) / len(filtered_df) * 100:.1f}%)",
                 help=f"Videos in the top {100-engagement_threshold}% by view count")

        if len(high_engagement_videos) > 0:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### ✅ Verified Status in Top Performers")
                if 'verified_status' in high_engagement_videos.columns:
                    high_engagement_verified = high_engagement_videos['verified_status'].value_counts()
                    if not high_engagement_verified.empty:
                        fig_high_verified = create_pie_chart(
                            high_engagement_verified.values,
                            high_engagement_verified.index,
                            'Verified Status in High Engagement Videos'
                        )
                        st.plotly_chart(fig_high_verified, use_container_width=True)
                        
                        # 比较验证状态比例
                        overall_verified_pct = (filtered_df['verified_status'] == 'verified').mean() * 100
                        high_engagement_verified_pct = (high_engagement_videos['verified_status'] == 'verified').mean() * 100
                        
                        st.metric("Verified in Top Performers", f"{high_engagement_verified_pct:.1f}%", 
                                 delta=f"{high_engagement_verified_pct - overall_verified_pct:.1f}% vs overall")
                else:
                    st.info("Verified status data not available for high engagement videos")

            with col2:
                st.markdown("#### 📂 Top Categories in High Performers")
                if 'content_category' in high_engagement_videos.columns:
                    high_engagement_category = high_engagement_videos['content_category'].value_counts().head(10)
                    if not high_engagement_category.empty:
                        fig_high_category = create_bar_chart(
                            high_engagement_category.index,
                            high_engagement_category.values,
                            'Top Categories in High Engagement Videos'
                        )
                        st.plotly_chart(fig_high_category, use_container_width=True)
                        st.caption(f"Most common category: {high_engagement_category.index[0]}")
                else:
                    st.info("Content category data not available for high engagement videos")
        else:
            st.warning("No videos meet the current high engagement threshold. Try lowering the percentile.")
    else:
        st.info("View count data not available for engagement analysis. Check your data filters.")


def show_dashboard_tab(filtered_df):
    """显示仪表板标签页"""
    st.markdown("""
    ### 📊 Comprehensive Dashboard
    
    Get a complete overview of your TikTok video data in one integrated view:
    - **Multiple visualizations**: Key charts combined for quick insights
    - **Cross-metric analysis**: See relationships between different aspects
    - **Quick assessment**: Identify patterns and outliers at a glance
    
    **Dashboard Components:**
    1. View count distribution
    2. Video duration patterns  
    3. Views vs duration relationship
    4. Category performance comparison
    """)
    
    st.subheader("📈 Integrated Data Overview")

    fig_dashboard = create_comprehensive_dashboard(filtered_df)
    if fig_dashboard:
        st.plotly_chart(fig_dashboard, use_container_width=True)
        st.caption("Interactive dashboard: Hover over elements for detailed information")
    else:
        st.info("Dashboard requires view count and duration data. Check your data filters.")


def show_advanced_analytics(filtered_df):
    """显示高级分析"""
    st.markdown("---")
    st.header("🔬 Advanced Analytics")
    st.markdown("""
    Statistical summaries and detailed comparative analysis:
    - **Group performance**: Metrics broken down by categories and status
    - **Statistical measures**: Mean, standard deviation, min/max values
    - **Sample size awareness**: Understand data reliability by group size
    
    **Usage Tips:**
    - Compare performance across different segments
    - Identify variability within groups (standard deviation)
    - Consider sample size when interpreting differences
    """)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Performance Statistics by Category")
        st.markdown("""
        Compare video performance across content categories:
        - **Count**: Number of videos in each category
        - **Mean**: Average view count per category
        - **Std**: Variability in performance within category
        """)
        
        if ('content_category' in filtered_df.columns and
                'video_view_count_clean' in filtered_df.columns and
                not filtered_df['video_view_count_clean'].isna().all()):

            performance_data = filtered_df.dropna(subset=['video_view_count_clean'])
            performance_stats = performance_data.groupby('content_category')['video_view_count_clean'].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(2).sort_values('count', ascending=False).head(10)

            st.dataframe(performance_stats, use_container_width=True)
            st.caption("Top 10 categories by video count. Sort by any column for different insights.")
        else:
            st.info("Performance or category data not available for analysis")

    with col2:
        st.subheader("📊 Engagement Statistics by Verified Status")
        st.markdown("""
        Analyze engagement patterns by account verification:
        - **Like rate comparisons**: Verified vs non-verified performance
        - **Statistical significance**: Consider sample sizes and variability
        - **Strategic insights**: Inform verification value assessment
        """)
        
        if ('verified_status' in filtered_df.columns and
                'like_rate' in filtered_df.columns and
                not filtered_df['like_rate'].isna().all()):

            engagement_data = filtered_df.dropna(subset=['like_rate'])
            engagement_stats = engagement_data.groupby('verified_status')['like_rate'].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(4).sort_values('count', ascending=False)

            st.dataframe(engagement_stats, use_container_width=True)
            st.caption("Engagement rate statistics by verification status")
        else:
            st.info("Engagement or verified status data not available")


def show_raw_data_section(filtered_df):
    """显示原始数据部分"""
    st.markdown("---")
    st.header("📋 Raw Data Explorer")
    st.markdown("""
    ### 🔍 Direct Data Access and Export
    
    Access the filtered dataset directly for:
    - **Data verification**: Check specific records and values
    - **Custom analysis**: Export for further analysis in other tools
    - **Data quality**: Review actual data structure and values
    
    **Export Options:**
    - **Save to data directory**: Store filtered dataset locally
    - **Download as CSV**: Get immediate file download
    - **Preview limited**: First 1,000 rows shown for performance
    """)
    
    with st.expander("📊 View Filtered Data", expanded=False):
        if not filtered_df.empty:
            st.markdown(f"**Displaying first 1,000 rows of {len(filtered_df):,} total records**")
            st.dataframe(filtered_df.head(1000), use_container_width=True)

            # Show basic statistics
            st.subheader("📈 Data Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Rows", f"{len(filtered_df):,}")
                st.metric("Total Columns", f"{len(filtered_df.columns)}")
                
            with col2:
                numeric_cols = len([col for col in filtered_df.columns if filtered_df[col].dtype in ['int64', 'float64']])
                categorical_cols = len([col for col in filtered_df.columns if filtered_df[col].dtype == 'object'])
                st.metric("Numeric Columns", numeric_cols)
                st.metric("Categorical Columns", categorical_cols)
                
            with col3:
                total_cells = len(filtered_df) * len(filtered_df.columns)
                non_null_cells = filtered_df.count().sum()
                completeness = (non_null_cells / total_cells) * 100
                st.metric("Data Completeness", f"{completeness:.1f}%")

            # 添加保存和下载按钮
            st.subheader("💾 Export Options")
            st.markdown("Choose how you want to export the current filtered dataset:")
            
            col1, col2 = st.columns(2)

            with col1:
                # 保存到data目录的按钮
                if st.button("💾 Save to Data Directory", key="save_data_btn", 
                           help="Save the filtered dataset to the local data directory"):
                    filepath = save_data_to_directory(filtered_df, filename_prefix="tiktok_filtered_data")
                    st.success(f"✅ Data saved to: `{filepath}`")
                    st.caption("File saved locally for future access")

            with col2:
                # 下载按钮 - 只在点击时生成数据
                csv_data = generate_csv_data(filtered_df)
                timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tiktok_filtered_data_{timestamp}.csv"

                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    key="download_data_btn",
                    help="Download the filtered dataset as a CSV file"
                )
                st.caption("Immediate download for external analysis")
        else:
            st.warning("⚠️ No data available to display. Try adjusting your filters.")


def show_deep_dives(filtered_df):
    """显示深度分析部分"""
    st.header("📈 Video Analysis Center")
    st.markdown("""
    ### Dive deep into your TikTok video data with interactive analysis tools
    
    Explore different aspects of video performance through specialized tabs:
    """)
    
    # 创建标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎬 Performance Metrics", 
        "👥 User Analysis", 
        "📝 Content Analysis", 
        "💬 Engagement Analysis", 
        "📊 Dashboard"
    ])

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