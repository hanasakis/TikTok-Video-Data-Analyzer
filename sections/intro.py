import streamlit as st
from utils.io import get_license_text

# ... 其余代码保持不变

def show_intro():
    """显示介绍部分"""
    st.header("📱 TikTok Video Data Analyzer")
    st.caption("Explore TikTok video performance with interactive visualizations and insights")

    with st.expander("About this App"):
        st.markdown("""
        ### TikTok Video Data Analyzer

        This interactive dashboard explores TikTok video data, including:

        - **Performance Metrics**: View counts, like counts, share counts, and engagement rates
        - **User Analysis**: Verified status, ban status, and their impact on performance
        - **Content Analysis**: Content categorization, sentiment analysis, and word clouds
        - **Engagement Analysis**: Engagement rates and high-performing video characteristics
        - **Advanced Analytics**: Statistical summaries and comparative analysis

        **Features**:
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
    with st.expander("Data Caveats and Limitations"):
        st.markdown("""
        ### Data Quality Notes

        - Some metrics may contain missing values
        - Engagement rates are calculated based on available view counts
        - Content categorization uses keyword matching and may not be exhaustive
        - Sentiment analysis is performed on transcription text only

        ### Usage Guidelines

        - Filter data carefully to avoid biased conclusions
        - Consider sample size when interpreting results
        - Be cautious when comparing across different content categories
        """)