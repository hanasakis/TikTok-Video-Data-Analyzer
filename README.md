# TikTok Video Data Analyzer

A comprehensive Streamlit-based web application for analyzing TikTok video performance metrics, user engagement patterns, and content insights through interactive visualizations and advanced analytics.

## 📋 Project Overview

This interactive dashboard provides deep insights into TikTok video data, enabling users to explore performance metrics, user behavior, content categorization, and engagement patterns through an intuitive web interface.

## 🚀 Features

- **📊 Performance Metrics**: View counts, like counts, share counts, and engagement rates analysis
- **👥 User Analysis**: Verified status, ban status, and their impact on video performance
- **📝 Content Analysis**: Automatic content categorization, sentiment analysis, and word clouds
- **💡 Engagement Analysis**: Engagement rates and high-performing video characteristics
- **🔍 Advanced Analytics**: Statistical summaries and comparative analysis
- **📱 Interactive Dashboard**: Comprehensive view with multiple visualization types
- **📥 Data Export**: Filter and download processed data as CSV files

## 🛠 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone or download the project**
   ```bash
   # If using git
   git clone https://github.com/hanasakis/TikTok-Video-Data-Analyzer
   cd tiktok-video-analyzer
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your data**
   - Place your TikTok dataset CSV file named `tiktok_dataset.csv` in the project root directory
   - Ensure the CSV file contains the required columns (video metrics, user status, transcription text)

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   - Open your web browser and go to `http://localhost:8501`
   - The application should load with the TikTok data analyzer interface

## 📁 Project Structure

```
tiktok-video-analyzer/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── tiktok_dataset.csv     # Input data file (not included in repo)
├── sections/              # Application content sections
│   ├── intro.py          # Context, objectives, data caveats
│   ├── overview.py       # KPIs, high-level trends
│   ├── deep_dives.py     # Comparisons, distributions, drilldowns
│   └── conclusions.py    # Insights, implications, next steps
├── utils/                 # Utility functions
│   ├── io.py            # Data loading, caching, file operations
│   ├── prep.py          # Data cleaning, normalization, preprocessing
│   └── viz.py           # Visualization functions with consistent styling
├── assets/               # Static resources
│   ├── aim.ico          # Icons for various UI elements
│   ├── bar_chart.ico
│   ├── document.ico
│   ├── line_chart.ico
│   ├── phone.ico
│   ├── rocket.ico
│   └── search.ico
│   ├── eFrei.png
│   └── WUT.png
└── data/                 # Processed and exported data files
    └── (auto-generated CSV files)
```

## 📊 Data Requirements

The application expects a CSV file with the following columns (or similar):

- `video_view_count` - Number of views
- `video_like_count` - Number of likes
- `video_share_count` - Number of shares
- `video_download_count` - Number of downloads
- `video_comment_count` - Number of comments
- `video_duration_sec` - Video duration in seconds
- `video_transcription_text` - Video description/transcription text
- `verified_status` - Account verification status
- `author_ban_status` - Author ban status
- `claim_status` - Content claim status

## 🎯 Usage Guide

### Data Exploration
1. **Apply Filters**: Use the sidebar filters to narrow down data by verified status, ban status, content category, duration, and view counts
2. **View KPIs**: Check the key metrics section for high-level performance indicators
3. **Explore Tabs**: Navigate through different analysis tabs for detailed insights

### Analysis Tabs
- **Performance Metrics**: Distribution of views, duration, and metric correlations
- **User Analysis**: Status distributions and their impact on performance
- **Content Analysis**: Category distribution, word clouds, and sentiment analysis
- **Engagement Analysis**: Engagement rates and high-performing content analysis
- **Dashboard**: Comprehensive view with multiple visualizations

### Data Export
- Filter data as needed and use the "Download Filtered Data as CSV" button
- Exported files are automatically saved to the `data/` directory with timestamps
- Download files to your local machine for further analysis

## 🔧 Configuration

### Customizing Content Categories
Modify the `categorize_text()` function in `utils/prep.py` to add or change content categories based on your specific keywords.

### Adjusting Visualization Styles
Update the visualization functions in `utils/viz.py` to customize chart colors, layouts, and styles.

### Adding New Analysis Sections
Create new modules in the `sections/` directory and integrate them into `app.py` following the existing pattern.

## 🐛 Troubleshooting

### Common Issues

1. **Data Loading Errors**
   - Ensure `tiktok_dataset.csv` exists in the project root
   - Check CSV file format and encoding
   - Verify required columns are present

2. **Missing Dependencies**
   - Run `pip install -r requirements.txt` to install all required packages
   - Ensure you're using a supported Python version (3.7+)

3. **Visualization Issues**
   - Clear browser cache if charts don't display properly
   - Check browser console for JavaScript errors

4. **Performance Issues**
   - For large datasets, consider sampling or aggregating data
   - Use the built-in filters to limit data volume

## 📄 License

This project is intended for educational and analytical purposes. Please ensure compliance with TikTok's terms of service and data usage policies when using actual TikTok data.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📞 Support

For questions or support regarding this application, please check the documentation or create an issue in the project repository.

---

**Note**: This application uses sample TikTok video data for demonstration purposes. Ensure you have appropriate permissions and comply with relevant terms of service when using actual TikTok data.

---

# requirements.txt

```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.13.0
matplotlib>=3.5.0
seaborn>=0.12.0
wordcloud>=1.9.0
textblob>=0.17.0
```

## Package Descriptions

- **streamlit**: Web application framework for creating interactive data apps
- **pandas**: Data manipulation and analysis library
- **numpy**: Numerical computing and array operations
- **plotly**: Interactive graphing and visualization library
- **matplotlib**: Comprehensive plotting and visualization library
- **seaborn**: Statistical data visualization based on matplotlib
- **wordcloud**: Word cloud generation from text data
- **textblob**: Simplified text processing and sentiment analysis

## Installation Notes

The requirements.txt file includes all necessary dependencies for running the TikTok Video Data Analyzer application. Install using:

```bash
pip install -r requirements.txt
```

For development or additional functionality, you might also consider:

```txt
jupyter>=1.0.0        # For notebook-based development
black>=22.0.0         # Code formatting
pytest>=7.0.0         # Testing framework
```

## Version Compatibility

The specified versions are minimum requirements. The application should work with newer versions of these packages, but if you encounter compatibility issues, try installing the exact versions listed above.