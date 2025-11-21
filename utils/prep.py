import pandas as pd
import numpy as np
from textblob import TextBlob
import streamlit as st  # 添加这行导入

def clean_numeric_data(value):
    """清洗数值数据"""
    if pd.isna(value):
        return np.nan
    try:
        return float(value)
    except:
        return np.nan

def categorize_text(text):
    """内容分类函数"""
    text = str(text).lower()
    categories = {
        'Technology': ['drone', 'mobile', 'internet', 'data', 'computer', 'phone', 'web', 'tech', 'software'],
        'Animals': ['dog', 'cat', 'animal', 'elephant', 'panda', 'snail', 'whale', 'bird', 'pet'],
        'History': ['history', 'ancient', 'century', 'year ago', 'discovered', 'historical'],
        'Sports': ['sport', 'basketball', 'olympics', 'game', 'player', 'match', 'football'],
        'Science': ['science', 'research', 'discover', 'study', 'scientist', 'experiment'],
        'Geography': ['earth', 'world', 'country', 'city', 'island', 'mountain', 'travel']
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    return 'Other'

def analyze_sentiment(text):
    """情感分析"""
    if pd.isna(text) or text == '':
        return 0
    analysis = TextBlob(str(text))
    return analysis.sentiment.polarity

@st.cache_data
def preprocess_data(df):
    """数据预处理"""
    df_processed = df.copy()

    # 清洗数值列
    numeric_columns = ['video_view_count', 'video_like_count', 'video_share_count',
                       'video_download_count', 'video_comment_count', 'video_duration_sec']

    for col in numeric_columns:
        if col in df_processed.columns:
            df_processed[f'{col}_clean'] = df_processed[col].apply(clean_numeric_data)

    # 内容分类
    if 'video_transcription_text' in df_processed.columns:
        df_processed['content_category'] = df_processed['video_transcription_text'].apply(categorize_text)

    # 计算互动率
    if 'video_view_count_clean' in df_processed.columns:
        view_col = 'video_view_count_clean'
        df_processed['like_rate'] = df_processed['video_like_count_clean'] / df_processed[view_col]
        df_processed['share_rate'] = df_processed['video_share_count_clean'] / df_processed[view_col]
        df_processed['comment_rate'] = df_processed['video_comment_count_clean'] / df_processed[view_col]

        # 处理无穷大和NaN值
        df_processed = df_processed.replace([np.inf, -np.inf], np.nan)
        df_processed = df_processed.fillna(0)

    return df_processed