import streamlit as st
import pandas as pd
from utils.io import generate_csv_data, save_data_to_directory  # 导入新函数


def show_conclusions(filtered_df):
    """显示结论和洞察"""
    st.header("💡 Key Insights & Recommendations")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Top Performance Drivers")

        # 计算关键指标
        insights_data = []

        if 'video_view_count_clean' in filtered_df.columns:
            avg_views = filtered_df['video_view_count_clean'].mean()
            max_views = filtered_df['video_view_count_clean'].max()

            st.metric("Average Views", f"{avg_views:,.0f}")
            st.metric("Peak Views", f"{max_views:,.0f}")

            insights_data.append({
                'Metric': 'Average Views',
                'Value': avg_views
            })
            insights_data.append({
                'Metric': 'Peak Views',
                'Value': max_views
            })

        if 'like_rate' in filtered_df.columns:
            avg_like_rate = filtered_df['like_rate'].mean() * 100
            st.metric("Average Like Rate", f"{avg_like_rate:.2f}%")

            insights_data.append({
                'Metric': 'Average Like Rate (%)',
                'Value': avg_like_rate
            })

    with col2:
        st.subheader("🎯 Optimization Opportunities")

        insights = []

        # 基于数据分析生成洞察
        if 'verified_status' in filtered_df.columns:
            verified_views = filtered_df.groupby('verified_status')['video_view_count_clean'].mean()
            if len(verified_views) > 1:
                max_status = verified_views.idxmax()
                insights.append(f"**{max_status}** accounts show highest average views")

        if 'content_category' in filtered_df.columns:
            top_category = filtered_df['content_category'].value_counts().index[0]
            insights.append(f"**{top_category}** is the most common content type")

        for insight in insights:
            st.write(f"• {insight}")

    # 添加关键指标下载按钮
    if insights_data:
        insights_df = pd.DataFrame(insights_data)

        col1, col2 = st.columns(2)

        with col1:
            # 保存到data目录的按钮
            if st.button("💾 Save Insights to Data Directory"):
                filepath = save_data_to_directory(insights_df, filename_prefix="tiktok_insights")
                st.success(f"Insights saved to: {filepath}")

        with col2:
            # 下载按钮 - 只在点击时生成数据
            csv_data = generate_csv_data(insights_df)
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tiktok_insights_{timestamp}.csv"

            st.download_button(
                label="📥 Download Key Insights as CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv"
            )

    st.subheader("🚀 Next Steps")
    st.markdown("""
    1. **Content Strategy**: Focus on high-performing content categories
    2. **Audience Engagement**: Analyze engagement patterns by user segments  
    3. **Performance Tracking**: Monitor key metrics over time
    4. **A/B Testing**: Experiment with different content formats
    5. **Quality Improvement**: Address data quality issues identified
    """)


def show_implications():
    """显示业务影响"""
    with st.expander("Business Implications"):
        st.markdown("""
        ### Strategic Impact

        **Content Strategy**
        - Identify top-performing content categories for resource allocation
        - Understand audience preferences and engagement patterns
        - Optimize video length and format based on performance data

        **User Engagement**  
        - Develop targeted engagement strategies for different user segments
        - Identify factors driving high engagement rates
        - Improve content recommendations based on sentiment analysis

        **Platform Growth**
        - Leverage insights for user acquisition and retention
        - Optimize platform features based on usage patterns
        - Enhance content discovery and recommendation algorithms
        """)