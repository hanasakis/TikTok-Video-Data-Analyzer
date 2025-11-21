import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st  # 确保这行存在


def create_histogram(df, column, title, xaxis_title, nbins=30):
    """创建直方图"""
    if column not in df.columns or df[column].isna().all():
        st.info(f"{title} data not available")
        return None

    fig = px.histogram(
        df,
        x=column,
        title=title,
        nbins=nbins
    )
    fig.update_layout(xaxis_title=xaxis_title, yaxis_title='Count')
    return fig


def create_pie_chart(values, names, title):
    """创建饼图"""
    fig = px.pie(
        values=values,
        names=names,
        title=title
    )
    return fig


def create_bar_chart(x, y, title, xaxis_title="Category", yaxis_title="Count"):
    """创建柱状图"""
    fig = px.bar(
        x=x,
        y=y,
        title=title,
        labels={'x': xaxis_title, 'y': yaxis_title}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def create_scatter_plot(df, x, y, title, opacity=0.6):
    """创建散点图"""
    scatter_data = df.dropna(subset=[x, y])
    if scatter_data.empty:
        st.info("No valid data available for scatter plot")
        return None

    # 对大数据集进行采样
    scatter_sample = scatter_data.sample(min(1000, len(scatter_data)))
    fig = px.scatter(
        scatter_sample,
        x=x,
        y=y,
        title=title,
        opacity=opacity
    )
    return fig


def create_box_plot(df, x, y, title):
    """创建箱线图"""
    data = df.dropna(subset=[y, x])
    if data.empty:
        st.info("No data available for box plot")
        return None

    # 去除极端值以便更好显示箱线图
    q95 = data[y].quantile(0.95)
    data_filtered = data[data[y] <= q95]

    if data_filtered.empty:
        st.info("No data available after filtering extremes")
        return None

    fig = px.box(
        data_filtered,
        x=x,
        y=y,
        title=title
    )
    return fig


def create_wordcloud(text):
    """创建词云"""
    if not text.strip():
        st.info("No text available for word cloud generation")
        return None

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=100
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Video Transcription Word Cloud')
    return fig


def create_comprehensive_dashboard(filtered_df):
    """创建综合仪表板"""
    required_columns = ['video_view_count_clean', 'video_duration_sec_clean']
    available_columns = [col for col in required_columns if
                         col in filtered_df.columns and not filtered_df[col].isna().all()]

    if len(available_columns) < 2:
        st.info("Insufficient data for comprehensive dashboard. Need view count and duration data.")
        return None

    dashboard_data = filtered_df.dropna(subset=available_columns)
    if dashboard_data.empty:
        st.info("No valid data available for dashboard")
        return None

    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('View Count Distribution', 'Duration Distribution',
                        'Views vs Duration', 'Top Categories by Average Views'),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )

    # View count distribution
    fig.add_trace(
        go.Histogram(x=dashboard_data['video_view_count_clean'], name='View Distribution'),
        row=1, col=1
    )

    # Duration distribution
    fig.add_trace(
        go.Histogram(x=dashboard_data['video_duration_sec_clean'], name='Duration Distribution'),
        row=1, col=2
    )

    # Views vs Duration scatter
    scatter_sample = dashboard_data.sample(min(500, len(dashboard_data)))
    if not scatter_sample.empty:
        fig.add_trace(
            go.Scatter(
                x=scatter_sample['video_duration_sec_clean'],
                y=scatter_sample['video_view_count_clean'],
                mode='markers',
                name='Views vs Duration',
                marker=dict(size=8, opacity=0.6)
            ),
            row=2, col=1
        )

    # Top categories by average views
    if 'content_category' in dashboard_data.columns:
        category_avg_views = dashboard_data.groupby('content_category')[
            'video_view_count_clean'].mean().sort_values(ascending=False).head(10)
        if not category_avg_views.empty:
            fig.add_trace(
                go.Bar(x=category_avg_views.index, y=category_avg_views.values, name='Category Avg Views'),
                row=2, col=2
            )

    fig.update_layout(height=800, title_text="TikTok Video Data Comprehensive Dashboard", showlegend=False)
    return fig