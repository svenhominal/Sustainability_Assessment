import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data import get_city_data

def show_ranking_section():
    """Display comprehensive city rankings for sustainability assessment"""
    
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
    .rank-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #D4E7D4 100%);
        border-left: 4px solid #2D5A3D;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .top-performer {
        background: linear-gradient(135deg, #1B4332 0%, #2D5A3D 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="section-title">🏆 City Sustainability Rankings</h1>', unsafe_allow_html=True)
    
    # Get data from session state
    if 'city_data' not in st.session_state or not st.session_state.city_data:
        st.warning("⚠️ No data available. Please add city data first in the Data section above.")
        return
    
    df = pd.DataFrame(st.session_state.city_data)
    
    # Calculate comprehensive rankings
    df_with_rankings = calculate_comprehensive_rankings(df)
    
    # Ranking type selection
    ranking_type = st.selectbox(
        "Select Ranking Type:",
        ["Overall Sustainability", "Environmental Performance", "Social Performance", 
         "Economic Performance", "Custom Weighted Ranking", "Performance Trends"]
    )
    
    if ranking_type == "Overall Sustainability":
        show_overall_ranking(df_with_rankings)
    elif ranking_type == "Environmental Performance":
        show_environmental_ranking(df_with_rankings)
    elif ranking_type == "Social Performance":
        show_social_ranking(df_with_rankings)
    elif ranking_type == "Economic Performance":
        show_economic_ranking(df_with_rankings)
    elif ranking_type == "Custom Weighted Ranking":
        show_custom_weighted_ranking(df_with_rankings)
    else:
        show_performance_trends(df_with_rankings)

def calculate_comprehensive_rankings(df):
    """Calculate comprehensive sustainability rankings"""
    df = df.copy()
    
    # Normalize all metrics to 0-1 scale
    # Environmental metrics (higher is better)
    df['Air_Quality_norm'] = df['Air_Quality'] / 100
    df['Green_Space_norm'] = df['Green_Space'] / 100
    df['Renewable_Energy_norm'] = df['Renewable_Energy'] / 100
    
    # Social metrics
    df['Education_norm'] = df['Education_Index']  # Already 0-1
    df['Healthcare_norm'] = df['Healthcare_Access'] / 100
    df['Safety_norm'] = df['Safety_Index'] / 10
    
    # Economic metrics
    df['GDP_norm'] = (df['GDP_per_Capita'] - df['GDP_per_Capita'].min()) / (df['GDP_per_Capita'].max() - df['GDP_per_Capita'].min())
    df['Employment_norm'] = (50 - df['Unemployment_Rate']) / 50  # Invert unemployment
    df['Innovation_norm'] = df['Innovation_Index'] / 100
    
    # Calculate dimension scores
    df['Environmental_Score'] = (df['Air_Quality_norm'] + df['Green_Space_norm'] + df['Renewable_Energy_norm']) / 3
    df['Social_Score'] = (df['Education_norm'] + df['Healthcare_norm'] + df['Safety_norm']) / 3
    df['Economic_Score'] = (df['GDP_norm'] + df['Employment_norm'] + df['Innovation_norm']) / 3
    
    # Overall sustainability score (equal weights)
    df['Overall_Score'] = (df['Environmental_Score'] + df['Social_Score'] + df['Economic_Score']) / 3
    
    # Calculate rankings
    df['Overall_Rank'] = df['Overall_Score'].rank(ascending=False, method='min')
    df['Environmental_Rank'] = df['Environmental_Score'].rank(ascending=False, method='min')
    df['Social_Rank'] = df['Social_Score'].rank(ascending=False, method='min')
    df['Economic_Rank'] = df['Economic_Score'].rank(ascending=False, method='min')
    
    return df

def show_overall_ranking(df):
    """Show overall sustainability ranking"""
    st.markdown('<h2 class="subsection-title">🌟 Overall Sustainability Ranking</h2>', unsafe_allow_html=True)
    
    # Sort by overall score
    df_sorted = df.sort_values('Overall_Score', ascending=False).reset_index(drop=True)
    
    # Top 3 performers highlight
    st.markdown('<h3 class="metric-category">🥇 Top Performers</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    for i, (idx, city) in enumerate(df_sorted.head(3).iterrows()):
        medals = ["🥇", "🥈", "🥉"]
        colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
        
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="top-performer">
                <h2>{medals[i]} #{i+1}</h2>
                <h3>{city['City']}</h3>
                <p><strong>{city['Country']}</strong></p>
                <p>Score: {city['Overall_Score']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Complete ranking table
    st.markdown('<h3 class="metric-category">📊 Complete Rankings</h3>', unsafe_allow_html=True)
    
    ranking_display = df_sorted[['City', 'Country', 'Overall_Score', 'Environmental_Score', 
                                'Social_Score', 'Economic_Score', 'Overall_Rank']].copy()
    
    ranking_display.columns = ['City', 'Country', 'Overall Score', 'Environmental', 
                              'Social', 'Economic', 'Rank']
    
    # Format scores
    for col in ['Overall Score', 'Environmental', 'Social', 'Economic']:
        ranking_display[col] = ranking_display[col].round(3)
    
    ranking_display['Rank'] = ranking_display['Rank'].astype(int)
    
    st.dataframe(ranking_display, use_container_width=True, hide_index=True)
    
    # Ranking visualization
    st.markdown('<h3 class="metric-category">📈 Score Distribution</h3>', unsafe_allow_html=True)
    
    fig = px.bar(
        df_sorted.head(10),
        x='City',
        y='Overall_Score',
        title="Top 10 Cities - Overall Sustainability Scores",
        color='Overall_Score',
        color_continuous_scale='Greens',
        text='Overall_Score'
    )
    
    fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_color='#1B4332',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance breakdown
    show_performance_breakdown(df_sorted.head(10))

def show_environmental_ranking(df):
    """Show environmental performance ranking"""
    st.markdown('<h2 class="subsection-title">🌱 Environmental Performance Ranking</h2>', unsafe_allow_html=True)
    
    df_sorted = df.sort_values('Environmental_Score', ascending=False)
    
    # Environmental leaders
    st.markdown('<h3 class="metric-category">🌿 Environmental Champions</h3>', unsafe_allow_html=True)
    
    top_env = df_sorted.head(5)
    
    for idx, city in top_env.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(f"**#{int(city['Environmental_Rank'])} {city['City']}**")
            st.write(f"Score: {city['Environmental_Score']:.3f}")
        
        with col2:
            st.metric("Air Quality", f"{city['Air_Quality']}/100")
        
        with col3:
            st.metric("Green Space", f"{city['Green_Space']}%")
        
        with col4:
            st.metric("Renewable Energy", f"{city['Renewable_Energy']}%")
        
        st.markdown("---")
    
    # Environmental metrics comparison
    fig = go.Figure()
    
    metrics = ['Air_Quality', 'Green_Space', 'Renewable_Energy']
    colors = ['#1B4332', '#2D5A3D', '#40736A']
    
    for i, metric in enumerate(metrics):
        fig.add_trace(go.Bar(
            name=metric.replace('_', ' '),
            x=top_env['City'],
            y=top_env[metric],
            marker_color=colors[i]
        ))
    
    fig.update_layout(
        title="Environmental Metrics - Top 5 Cities",
        title_font_color='#1B4332',
        barmode='group',
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_social_ranking(df):
    """Show social performance ranking"""
    st.markdown('<h2 class="subsection-title">👥 Social Performance Ranking</h2>', unsafe_allow_html=True)
    
    df_sorted = df.sort_values('Social_Score', ascending=False)
    
    # Social performance table
    social_display = df_sorted[['City', 'Country', 'Social_Score', 'Education_Index', 
                               'Healthcare_Access', 'Safety_Index', 'Social_Rank']].head(10)
    
    social_display.columns = ['City', 'Country', 'Social Score', 'Education', 
                             'Healthcare', 'Safety', 'Rank']
    
    st.dataframe(social_display.round(3), use_container_width=True, hide_index=True)
    
    # Social metrics radar chart for top 5
    st.markdown('<h3 class="metric-category">📊 Social Metrics Comparison - Top 5</h3>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    top_5_social = df_sorted.head(5)
    
    for idx, city in top_5_social.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[city['Education_Index']*100, city['Healthcare_Access'], city['Safety_Index']*10],
            theta=['Education', 'Healthcare', 'Safety'],
            fill='toself',
            name=city['City'],
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Social Performance - Top 5 Cities",
        title_font_color='#1B4332'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_economic_ranking(df):
    """Show economic performance ranking"""
    st.markdown('<h2 class="subsection-title">💰 Economic Performance Ranking</h2>', unsafe_allow_html=True)
    
    df_sorted = df.sort_values('Economic_Score', ascending=False)
    
    # Economic performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # GDP vs Innovation scatter
        fig = px.scatter(
            df,
            x='GDP_per_Capita',
            y='Innovation_Index',
            size='Economic_Score',
            hover_data=['City', 'Unemployment_Rate'],
            title="Economic Performance: GDP vs Innovation",
            color='Economic_Score',
            color_continuous_scale='Greens'
        )
        fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Employment rates
        fig = px.bar(
            df_sorted.head(10),
            x='City',
            y='Employment_norm',
            title="Employment Performance (Top 10)",
            color='Employment_norm',
            color_continuous_scale='Greens'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Economic ranking table
    economic_display = df_sorted[['City', 'Country', 'Economic_Score', 'GDP_per_Capita', 
                                 'Unemployment_Rate', 'Innovation_Index', 'Economic_Rank']].head(10)
    
    economic_display.columns = ['City', 'Country', 'Economic Score', 'GDP per Capita', 
                               'Unemployment %', 'Innovation', 'Rank']
    
    st.dataframe(economic_display.round(2), use_container_width=True, hide_index=True)

def show_custom_weighted_ranking(df):
    """Show custom weighted ranking with user-defined weights"""
    st.markdown('<h2 class="subsection-title">⚖️ Custom Weighted Ranking</h2>', unsafe_allow_html=True)
    
    st.write("Adjust the weights for different sustainability dimensions to create your custom ranking:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        env_weight = st.slider("Environmental Weight", 0.0, 1.0, 0.33, 0.01)
    with col2:
        social_weight = st.slider("Social Weight", 0.0, 1.0, 0.33, 0.01)
    with col3:
        economic_weight = st.slider("Economic Weight", 0.0, 1.0, 0.34, 0.01)
    
    # Normalize weights
    total_weight = env_weight + social_weight + economic_weight
    if total_weight > 0:
        env_weight_norm = env_weight / total_weight
        social_weight_norm = social_weight / total_weight
        economic_weight_norm = economic_weight / total_weight
        
        # Calculate custom scores
        df['Custom_Score'] = (
            df['Environmental_Score'] * env_weight_norm +
            df['Social_Score'] * social_weight_norm +
            df['Economic_Score'] * economic_weight_norm
        )
        
        df['Custom_Rank'] = df['Custom_Score'].rank(ascending=False, method='min')
        
        # Display custom ranking
        df_custom = df.sort_values('Custom_Score', ascending=False)
        
        st.markdown('<h3 class="metric-category">🎯 Your Custom Ranking</h3>', unsafe_allow_html=True)
        
        # Weight distribution display
        st.info(f"Weight Distribution: Environmental {env_weight_norm:.1%}, Social {social_weight_norm:.1%}, Economic {economic_weight_norm:.1%}")
        
        # Custom ranking table
        custom_display = df_custom[['City', 'Country', 'Custom_Score', 'Environmental_Score', 
                                  'Social_Score', 'Economic_Score', 'Custom_Rank']].head(10)
        
        custom_display.columns = ['City', 'Country', 'Custom Score', 'Environmental', 
                                'Social', 'Economic', 'Rank']
        
        st.dataframe(custom_display.round(3), use_container_width=True, hide_index=True)
        
        # Comparison with overall ranking
        comparison_fig = px.scatter(
            df,
            x='Overall_Score',
            y='Custom_Score',
            hover_data=['City'],
            title="Custom vs Overall Ranking Comparison",
            color='Custom_Score',
            color_continuous_scale='Greens'
        )
        comparison_fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(comparison_fig, use_container_width=True)

def show_performance_trends(df):
    """Show performance trends and insights"""
    st.markdown('<h2 class="subsection-title">📈 Performance Trends & Insights</h2>', unsafe_allow_html=True)
    
    # Performance distribution analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution histogram
        fig = px.histogram(
            df,
            x='Overall_Score',
            nbins=10,
            title="Distribution of Overall Sustainability Scores",
            color_discrete_sequence=['#2D5A3D']
        )
        fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Dimension correlation
        correlation_data = df[['Environmental_Score', 'Social_Score', 'Economic_Score']].corr()
        
        fig = px.imshow(
            correlation_data,
            title="Correlation Between Sustainability Dimensions",
            color_continuous_scale='Greens'
        )
        fig.update_layout(title_font_color='#1B4332')
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance insights
    st.markdown('<h3 class="metric-category">💡 Key Insights</h3>', unsafe_allow_html=True)
    
    # Calculate insights
    best_overall = df.loc[df['Overall_Score'].idxmax()]
    worst_overall = df.loc[df['Overall_Score'].idxmin()]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success(f"""
        **🏆 Best Performer**
        
        {best_overall['City']}, {best_overall['Country']}
        
        Overall Score: {best_overall['Overall_Score']:.3f}
        """)
    
    with col2:
        # Most balanced city (smallest std deviation across dimensions)
        df['Score_Std'] = df[['Environmental_Score', 'Social_Score', 'Economic_Score']].std(axis=1)
        most_balanced = df.loc[df['Score_Std'].idxmin()]
        
        st.info(f"""
        **⚖️ Most Balanced**
        
        {most_balanced['City']}, {most_balanced['Country']}
        
        Consistency Score: {1/most_balanced['Score_Std']:.2f}
        """)
    
    with col3:
        # Biggest improver potential (city with highest single dimension score but lower overall)
        df['Improvement_Potential'] = df[['Environmental_Score', 'Social_Score', 'Economic_Score']].max(axis=1) - df['Overall_Score']
        highest_potential = df.loc[df['Improvement_Potential'].idxmax()]
        
        st.warning(f"""
        **📈 Highest Potential**
        
        {highest_potential['City']}, {highest_potential['Country']}
        
        Improvement Gap: {highest_potential['Improvement_Potential']:.3f}
        """)
    
    # Regional/country analysis if multiple countries
    if df['Country'].nunique() > 1:
        st.markdown('<h3 class="metric-category">🌍 Country Performance</h3>', unsafe_allow_html=True)
        
        country_stats = df.groupby('Country').agg({
            'Overall_Score': ['mean', 'count'],
            'Environmental_Score': 'mean',
            'Social_Score': 'mean',
            'Economic_Score': 'mean'
        }).round(3)
        
        country_stats.columns = ['Avg Overall Score', 'Number of Cities', 'Avg Environmental', 'Avg Social', 'Avg Economic']
        st.dataframe(country_stats, use_container_width=True)

def show_performance_breakdown(df):
    """Show detailed performance breakdown for top cities"""
    st.markdown('<h3 class="metric-category">🔍 Performance Breakdown - Top 10</h3>', unsafe_allow_html=True)
    
    # Stacked bar chart showing dimension contributions
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Environmental',
        x=df['City'],
        y=df['Environmental_Score'],
        marker_color='#1B4332'
    ))
    
    fig.add_trace(go.Bar(
        name='Social',
        x=df['City'],
        y=df['Social_Score'],
        marker_color='#2D5A3D'
    ))
    
    fig.add_trace(go.Bar(
        name='Economic',
        x=df['City'],
        y=df['Economic_Score'],
        marker_color='#40736A'
    ))
    
    fig.update_layout(
        barmode='stack',
        title='Sustainability Score Breakdown by Dimension',
        title_font_color='#1B4332',
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
