import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data import get_city_data

def show_analysis_section():
    """Display the analysis section with sustainability metrics"""
    
    # Custom CSS for dark green styling
    st.markdown("""
    <style>
    .section-title {
        color: #1B4332;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subsection-title {
        color: #2D5A3D;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    .metric-category {
        color: #40736A;
        font-size: 1.3rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="section-title">📈 Sustainability Analysis</h1>', unsafe_allow_html=True)
    
    # Get data from session state
    if 'city_data' not in st.session_state or not st.session_state.city_data:
        st.warning("⚠️ No data available. Please add city data first in the Data section above.")
        return
    
    df = pd.DataFrame(st.session_state.city_data)
    
    # Calculate sustainability scores
    df_with_scores = calculate_sustainability_scores(df)
    
    # Analysis options
    analysis_type = st.selectbox(
        "Select Analysis Type:",
        ["Overview Dashboard", "Environmental Analysis", "Social Analysis", "Economic Analysis", "Comparative Analysis"]
    )
    
    if analysis_type == "Overview Dashboard":
        show_overview_dashboard(df_with_scores)
    elif analysis_type == "Environmental Analysis":
        show_environmental_analysis(df_with_scores)
    elif analysis_type == "Social Analysis":
        show_social_analysis(df_with_scores)
    elif analysis_type == "Economic Analysis":
        show_economic_analysis(df_with_scores)
    else:
        show_comparative_analysis(df_with_scores)

def calculate_sustainability_scores(df):
    """Calculate sustainability scores for each dimension"""
    df = df.copy()
    
    # Normalize metrics to 0-1 scale
    environmental_metrics = ['Air_Quality', 'Green_Space', 'Renewable_Energy']
    social_metrics = ['Education_Index', 'Healthcare_Access', 'Safety_Index']
    economic_metrics = ['GDP_per_Capita', 'Innovation_Index']
    
    # Environmental score (higher is better)
    df['Environmental_Score'] = (
        df['Air_Quality'] / 100 +
        df['Green_Space'] / 100 +
        df['Renewable_Energy'] / 100
    ) / 3
    
    # Social score (higher is better, but normalize Safety_Index and Healthcare_Access)
    df['Social_Score'] = (
        df['Education_Index'] +
        df['Healthcare_Access'] / 100 +
        df['Safety_Index'] / 10
    ) / 3
    
    # Economic score (normalize and invert unemployment rate as it's negative)
    max_gdp = df['GDP_per_Capita'].max()
    df['Economic_Score'] = (
        df['GDP_per_Capita'] / max_gdp +
        df['Innovation_Index'] / 100 +
        (50 - df['Unemployment_Rate']) / 50  # Invert unemployment rate
    ) / 3
    
    # Overall sustainability score
    df['Overall_Score'] = (
        df['Environmental_Score'] +
        df['Social_Score'] +
        df['Economic_Score']
    ) / 3
    
    return df

def show_overview_dashboard(df):
    """Show overview dashboard with key metrics"""
    st.markdown('<h2 class="subsection-title">🎯 Sustainability Overview</h2>', unsafe_allow_html=True)
    
    # Top performing cities
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="metric-category">🏆 Top Performing Cities</h3>', unsafe_allow_html=True)
        top_cities = df.nlargest(5, 'Overall_Score')[['City', 'Overall_Score']]
        
        for idx, row in top_cities.iterrows():
            score_percent = row['Overall_Score'] * 100
            st.metric(
                label=row['City'],
                value=f"{score_percent:.1f}%",
                delta=f"Rank #{top_cities.index.get_loc(idx) + 1}"
            )
    
    with col2:
        st.markdown('<h3 class="metric-category">📊 Average Scores by Dimension</h3>', unsafe_allow_html=True)
        avg_env = df['Environmental_Score'].mean() * 100
        avg_social = df['Social_Score'].mean() * 100
        avg_economic = df['Economic_Score'].mean() * 100
        
        st.metric("Environmental", f"{avg_env:.1f}%")
        st.metric("Social", f"{avg_social:.1f}%")
        st.metric("Economic", f"{avg_economic:.1f}%")
    
    # Overall scores distribution
    st.markdown('<h3 class="metric-category">📈 Overall Sustainability Scores</h3>', unsafe_allow_html=True)
    
    fig = px.bar(
        df, 
        x='City', 
        y='Overall_Score',
        title="Overall Sustainability Scores by City",
        color='Overall_Score',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_color='#1B4332',
        font_color='#2D5A3D'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Scores breakdown heatmap
    st.markdown('<h3 class="metric-category">🔥 Scores Breakdown Heatmap</h3>', unsafe_allow_html=True)
    
    heatmap_data = df[['City', 'Environmental_Score', 'Social_Score', 'Economic_Score']].set_index('City')
    
    fig = px.imshow(
        heatmap_data.T,
        title="Sustainability Scores Heatmap",
        color_continuous_scale='Greens',
        aspect='auto'
    )
    fig.update_layout(title_font_color='#1B4332')
    st.plotly_chart(fig, use_container_width=True)

def show_environmental_analysis(df):
    """Show detailed environmental analysis"""
    st.markdown('<h2 class="subsection-title">🌱 Environmental Analysis</h2>', unsafe_allow_html=True)
    
    # Environmental metrics comparison
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df, 
            x='Air_Quality', 
            y='Green_Space',
            size='Renewable_Energy',
            hover_data=['City'],
            title="Air Quality vs Green Space (Size = Renewable Energy)",
            color='Environmental_Score',
            color_continuous_scale='Greens'
        )
        fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Environmental performance radar
        categories = ['Air Quality', 'Green Space', 'Renewable Energy']
        
        fig = go.Figure()
        
        for idx, row in df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row['Air_Quality'], row['Green_Space'], row['Renewable_Energy']],
                theta=categories,
                fill='toself',
                name=row['City'],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Environmental Performance Comparison",
            title_font_color='#1B4332'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top environmental performers
    st.markdown('<h3 class="metric-category">🏆 Environmental Leaders</h3>', unsafe_allow_html=True)
    env_leaders = df.nlargest(3, 'Environmental_Score')[['City', 'Air_Quality', 'Green_Space', 'Renewable_Energy', 'Environmental_Score']]
    st.dataframe(env_leaders, use_container_width=True)

def show_social_analysis(df):
    """Show detailed social analysis"""
    st.markdown('<h2 class="subsection-title">👥 Social Analysis</h2>', unsafe_allow_html=True)
    
    # Social metrics visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df,
            x='Education_Index',
            y='Healthcare_Access',
            size='Safety_Index',
            hover_data=['City'],
            title="Education vs Healthcare (Size = Safety)",
            color='Social_Score',
            color_continuous_scale='Greens'
        )
        fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Social metrics by city
        social_metrics = df[['City', 'Education_Index', 'Healthcare_Access', 'Safety_Index']].melt(
            id_vars=['City'], 
            var_name='Metric', 
            value_name='Score'
        )
        
        fig = px.box(
            social_metrics,
            x='Metric',
            y='Score',
            title="Distribution of Social Metrics"
        )
        fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(fig, use_container_width=True)
    
    # Social performance ranking
    st.markdown('<h3 class="metric-category">🏆 Social Performance Ranking</h3>', unsafe_allow_html=True)
    social_ranking = df.nlargest(5, 'Social_Score')[['City', 'Education_Index', 'Healthcare_Access', 'Safety_Index', 'Social_Score']]
    st.dataframe(social_ranking, use_container_width=True)

def show_economic_analysis(df):
    """Show detailed economic analysis"""
    st.markdown('<h2 class="subsection-title">💰 Economic Analysis</h2>', unsafe_allow_html=True)
    
    # Economic metrics visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df,
            x='GDP_per_Capita',
            y='Innovation_Index',
            size='Population',
            hover_data=['City', 'Unemployment_Rate'],
            title="GDP per Capita vs Innovation Index",
            color='Economic_Score',
            color_continuous_scale='Greens'
        )
        fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Unemployment rate comparison
        fig = px.bar(
            df.sort_values('Unemployment_Rate'),
            x='City',
            y='Unemployment_Rate',
            title="Unemployment Rate by City",
            color='Unemployment_Rate',
            color_continuous_scale='Greens_r'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Economic performance summary
    st.markdown('<h3 class="metric-category">💼 Economic Performance Summary</h3>', unsafe_allow_html=True)
    economic_summary = df[['City', 'GDP_per_Capita', 'Unemployment_Rate', 'Innovation_Index', 'Economic_Score']].round(2)
    st.dataframe(economic_summary, use_container_width=True)

def show_comparative_analysis(df):
    """Show comparative analysis between cities"""
    st.markdown('<h2 class="subsection-title">⚖️ Comparative Analysis</h2>', unsafe_allow_html=True)
    
    # City selection for comparison
    selected_cities = st.multiselect(
        "Select cities to compare:",
        df['City'].tolist(),
        default=df['City'].tolist()[:3] if len(df) >= 3 else df['City'].tolist()
    )
    
    if selected_cities:
        comparison_df = df[df['City'].isin(selected_cities)]
        
        # Radar chart comparison
        fig = go.Figure()
        
        metrics = ['Environmental_Score', 'Social_Score', 'Economic_Score']
        
        for idx, row in comparison_df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row['Environmental_Score']*100, row['Social_Score']*100, row['Economic_Score']*100],
                theta=['Environmental', 'Social', 'Economic'],
                fill='toself',
                name=row['City'],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="City Comparison - Sustainability Dimensions",
            title_font_color='#1B4332'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed comparison table
        st.markdown('<h3 class="metric-category">📋 Detailed Comparison</h3>', unsafe_allow_html=True)
        comparison_metrics = comparison_df[[
            'City', 'Overall_Score', 'Environmental_Score', 
            'Social_Score', 'Economic_Score'
        ]].round(3)
        st.dataframe(comparison_metrics, use_container_width=True)
        
        # Best performing city in each category
        st.markdown('<h3 class="metric-category">🥇 Category Leaders</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            env_leader = comparison_df.loc[comparison_df['Environmental_Score'].idxmax()]
            st.success(f"🌱 **Environmental Leader**\n\n{env_leader['City']}\nScore: {env_leader['Environmental_Score']:.2f}")
        
        with col2:
            social_leader = comparison_df.loc[comparison_df['Social_Score'].idxmax()]
            st.success(f"👥 **Social Leader**\n\n{social_leader['City']}\nScore: {social_leader['Social_Score']:.2f}")
        
        with col3:
            economic_leader = comparison_df.loc[comparison_df['Economic_Score'].idxmax()]
            st.success(f"💰 **Economic Leader**\n\n{economic_leader['City']}\nScore: {economic_leader['Economic_Score']:.2f}")
    else:
        st.info("Please select at least one city to compare.")
