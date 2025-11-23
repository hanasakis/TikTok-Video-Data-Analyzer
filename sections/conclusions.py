import streamlit as st
import pandas as pd
from utils.io import generate_csv_data, save_data_to_directory

def show_conclusions(filtered_df):
    """显示结论和洞察"""
    st.header("💡 Key Insights & Actionable Recommendations")
    st.markdown("""
    ### Transform Data into Strategic Decisions
    
    This section synthesizes your analysis into actionable insights and recommendations. 
    Use these findings to inform your content strategy, platform decisions, and performance optimization.
    """)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Top Performance Drivers")
        st.markdown("""
        **Key metrics that indicate successful content:**
        - **Average performance benchmarks** for your current selection
        - **Peak performance levels** to aspire toward
        - **Engagement rates** that measure audience connection
        """)
        
        # 计算关键指标
        insights_data = []

        if 'video_view_count_clean' in filtered_df.columns:
            avg_views = filtered_df['video_view_count_clean'].mean()
            max_views = filtered_df['video_view_count_clean'].max()

            st.metric("Average Views", f"{avg_views:,.0f}", 
                     help="Typical view count for videos in current selection")
            st.metric("Peak Views", f"{max_views:,.0f}", 
                     help="Highest view count achieved in current selection")

            insights_data.append({
                'Metric': 'Average Views',
                'Value': avg_views,
                'Insight': 'Benchmark performance level'
            })
            insights_data.append({
                'Metric': 'Peak Views', 
                'Value': max_views,
                'Insight': 'Maximum achievable performance'
            })

        if 'like_rate' in filtered_df.columns:
            avg_like_rate = filtered_df['like_rate'].mean() * 100
            st.metric("Average Like Rate", f"{avg_like_rate:.2f}%",
                     help="Percentage of viewers who like videos")

            insights_data.append({
                'Metric': 'Average Like Rate (%)',
                'Value': avg_like_rate,
                'Insight': 'Audience appreciation level'
            })

    with col2:
        st.subheader("🎯 Optimization Opportunities")
        st.markdown("""
        **Areas for improvement and strategic focus:**
        - **High-performing segments** to emulate and scale
        - **Content gaps** and underserved categories
        - **Engagement drivers** to prioritize
        """)
        
        insights = []

        # 基于数据分析生成洞察
        if 'verified_status' in filtered_df.columns:
            verified_views = filtered_df.groupby('verified_status')['video_view_count_clean'].mean()
            if len(verified_views) > 1:
                max_status = verified_views.idxmax()
                max_views = verified_views.max()
                min_status = verified_views.idxmin()
                min_views = verified_views.min()
                performance_gap = ((max_views - min_views) / min_views) * 100
                
                insights.append(f"**{max_status} accounts** show {performance_gap:.0f}% higher average views than {min_status} accounts")
                st.metric(f"{max_status} vs {min_status}", f"+{performance_gap:.0f}%", 
                         help="Performance difference between best and worst performing status")

        if 'content_category' in filtered_df.columns:
            top_category = filtered_df['content_category'].value_counts().index[0]
            top_count = filtered_df['content_category'].value_counts().iloc[0]
            total_videos = len(filtered_df)
            category_percentage = (top_count / total_videos) * 100
            
            insights.append(f"**{top_category}** is the most common content type ({category_percentage:.1f}% of videos)")
            st.metric("Top Category", top_category, 
                     help="Most frequently occurring content category")

        # 显示生成的洞察
        st.markdown("#### 🔍 Key Findings:")
        for insight in insights:
            st.success(f"• {insight}")

    # 添加关键指标下载按钮
    if insights_data:
        insights_df = pd.DataFrame(insights_data)

        st.subheader("💾 Export Insights")
        st.markdown("""
        Save your key insights for future reference or sharing with stakeholders:
        - **CSV format** for easy import into other tools
        - **Local storage** for ongoing project work
        - **Timestamped** for version control
        """)
        
        col1, col2 = st.columns(2)

        with col1:
            # 保存到data目录的按钮
            if st.button("💾 Save Insights to Data Directory", 
                       help="Save insights as a CSV file in the local data directory"):
                filepath = save_data_to_directory(insights_df, filename_prefix="tiktok_insights")
                st.success(f"✅ Insights saved to: `{filepath}`")
                st.balloons()

        with col2:
            # 下载按钮 - 只在点击时生成数据
            csv_data = generate_csv_data(insights_df)
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tiktok_insights_{timestamp}.csv"

            st.download_button(
                label="📥 Download Key Insights as CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                help="Download insights as a CSV file for immediate use"
            )

    st.subheader("🚀 Actionable Next Steps")
    st.markdown("""
    ### Implement Your Findings with This Strategic Roadmap
    
    Based on your analysis, consider these implementation priorities:
    """)
    
    steps_col1, steps_col2 = st.columns(2)
    
    with steps_col1:
        st.markdown("""
        **1. 📊 Content Strategy Development**
        - Focus resources on high-performing content categories identified
        - Experiment with formats that show above-average engagement
        - Balance content mix based on category performance insights
        
        **2. 👥 Audience Engagement Optimization**  
        - Analyze engagement patterns by different user segments
        - Develop targeted strategies for verified vs non-verified creators
        - Optimize posting schedules based on performance patterns
        
        **3. ⚡ Performance Tracking System**
        - Establish regular monitoring of key metrics identified
        - Set benchmarks based on current average performance
        - Create alerts for significant performance changes
        """)
    
    with steps_col2:
        st.markdown("""
        **4. 🔬 A/B Testing Framework**
        - Experiment with different content formats and lengths
        - Test hypotheses generated from correlation analyses
        - Measure impact of changes on key performance indicators
        
        **5. 🛠️ Quality Improvement Initiatives**
        - Address data quality issues identified in the report
        - Improve data collection for under-represented metrics
        - Enhance categorization accuracy for better insights
        
        **6. 📈 Continuous Learning Cycle**
        - Schedule regular analysis sessions to track progress
        - Update strategies based on new performance data
        - Share insights across relevant teams and stakeholders
        """)
    
    st.info("""
    **💡 Pro Tip**: Revisit this analysis monthly to track progress against these recommendations 
    and adjust your strategy based on new performance data.
    """)


def show_implications():
    """显示业务影响"""
    with st.expander("🏢 Business Implications & Strategic Impact", expanded=False):
        st.markdown("""
        ### Strategic Implications for Your Organization
        
        Translate data insights into actionable business strategies:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🎯 Content Strategy Implications
            
            **Resource Allocation**
            - Direct content creation resources toward high-performing categories
            - Balance investment between proven formats and experimental content
            - Prioritize content types that show strong engagement signals
            
            **Audience Development**
            - Develop creator support programs for high-potential categories
            - Identify and nurture emerging content trends early
            - Create category-specific best practices and guidelines
            
            **Platform Optimization**
            - Optimize recommendation algorithms for high-engagement content patterns
            - Improve discovery features for underrepresented but high-quality categories
            - Enhance user experience based on successful content characteristics
            """)
            
        with col2:
            st.markdown("""
            #### 💼 User Engagement Strategy
            
            **Creator Relationships**
            - Develop targeted support for different creator segments
            - Create verification programs that align with performance benefits
            - Establish feedback loops with high-performing creators
            
            **Community Building**
            - Foster communities around high-engagement content categories
            - Develop features that enhance category-specific interactions
            - Create events and challenges that leverage successful content patterns
            
            **Monetization Opportunities**
            - Align advertising products with high-performing content characteristics
            - Develop sponsorship opportunities around successful categories
            - Create premium features that enhance top content performance
            """)
        
        st.markdown("""
        #### 📊 Platform Growth & Development
        
        **User Acquisition & Retention**
        - Leverage high-performing content insights for user acquisition campaigns
        - Develop retention strategies based on engagement pattern analysis
        - Create onboarding experiences that highlight successful content types
        
        **Feature Development**
        - Prioritize platform features that enhance high-engagement behaviors
        - Develop tools that help creators optimize based on performance insights
        - Create analytics features that provide actionable insights to creators
        
        **Competitive Positioning**
        - Differentiate based on unique performance advantages identified
        - Develop specialty areas around consistently high-performing categories
        - Create brand positioning that leverages performance strengths
        """)
        
        st.success("""
        **Strategic Recommendation**: Use these insights to create a prioritized roadmap 
        that focuses on the highest-impact opportunities identified through your analysis.
        """)