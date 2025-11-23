import streamlit as st
from utils.io import get_license_text

def show_intro():
    """显示介绍部分"""
    st.header("📱 TikTok Video Data Analyzer")
    st.caption("Explore TikTok video performance with interactive visualizations and insights")
    
    # 添加使用指南
    st.markdown("""
    ### 🎯 How to Use This Dashboard
    
    This interactive dashboard is designed to help you explore and analyze TikTok video data through four main sections:
    
    1. **📊 Overview**: Get high-level insights with key metrics and data quality assessment
    2. **📈 Video Analysis**: Dive deep into performance metrics, user behavior, and content analysis
    3. **💡 Key Insights**: Discover actionable recommendations and strategic implications
    4. **📋 Raw Data**: Access and export the filtered dataset
    
    **Navigation Tips:**
    - Use the filters in the main interface to focus on specific data subsets
    - Switch between tabs in the Video Analysis section for different perspectives
    - Click on expandable sections to reveal detailed information
    - Download insights and filtered data using the provided buttons
    """)

    with st.expander("🔍 About this App"):
        st.markdown("""
        ### TikTok Video Data Analyzer

        This interactive dashboard explores TikTok video data, including:

        - **Performance Metrics**: View counts, like counts, share counts, and engagement rates
        - **User Analysis**: Verified status, ban status, and their impact on performance
        - **Content Analysis**: Content categorization, sentiment analysis, and word clouds
        - **Engagement Analysis**: Engagement rates and high-performing video characteristics
        - **Advanced Analytics**: Statistical summaries and comparative analysis

        **Features:**
        - Interactive filters for user status, content category, and performance metrics
        - Multiple visualization types: histograms, scatter plots, bar charts, pie charts
        - Sentiment analysis of video transcriptions
        - Word cloud generation from transcription content
        - Comprehensive dashboard view
        - Data export functionality

        **Data Source**: TikTok video dataset containing video information, performance metrics, and user status.

        **Note**: This app uses sample TikTok video data for demonstration purposes.
        """)

        st.markdown(get_license_text())


def show_data_caveats():
    """显示数据注意事项"""
    with st.expander("⚠️ Data Caveats and Limitations"):
        st.markdown("""
        ### 📊 Data Quality Notes

        **Missing Values:**
        - Some metrics may contain missing values that are automatically handled
        - Engagement rates are calculated only when view count data is available
        - Videos with incomplete data are excluded from relevant analyses

        **Data Processing:**
        - Content categorization uses keyword matching and may not capture all nuances
        - Sentiment analysis is performed on transcription text and may not reflect video content
        - Extreme values are filtered to improve visualization clarity

        ### 🔍 Interpretation Guidelines

        **Sample Size Considerations:**
        - Results are more reliable with larger filtered datasets
        - Be cautious when drawing conclusions from small sample sizes
        - Consider statistical significance when comparing groups

        **Filter Impact:**
        - Applying multiple filters may significantly reduce dataset size
        - Filter settings can influence observed patterns and trends
        - Reset filters to see the complete dataset when needed
        """)


def show_navigation_guide():
    """显示导航指南"""
    with st.expander("🧭 Navigation Guide"):
        st.markdown("""
        ### Section Overview
        
        **1. Overview Section**
        - **Key Metrics**: Real-time performance indicators
        - **Data Quality Report**: Assess dataset completeness and reliability
        - **Interactive Filters**: Refine your analysis scope
        
        **2. Video Analysis Section** (Multiple Tabs)
        - **Performance Metrics**: View distributions and correlations
        - **User Analysis**: Verified status and ban status impacts
        - **Content Analysis**: Categories, word clouds, and sentiment
        - **Engagement Analysis**: Interaction rates and high-performing content
        - **Dashboard**: Comprehensive overview visualization
        
        **3. Key Insights Section**
        - **Performance Drivers**: Top metrics and optimization opportunities
        - **Business Implications**: Strategic recommendations
        - **Actionable Next Steps**: Practical implementation guidance
        
        **4. Raw Data Section**
        - **Filtered Data Preview**: First 1000 rows of current selection
        - **Export Options**: Save to data directory or download as CSV
        - **Data Summary**: Basic statistics about the filtered dataset
        """)