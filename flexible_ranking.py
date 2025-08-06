"""
Flexible Ranking Module
This module creates rankings that adapt to any custom indicators or default template data.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from custom_indicators import load_custom_indicators_data, get_indicators_summary

def show_ranking_section():
    """Display ranking analysis - adapts to available data"""
    
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
    .ranking-card {
        background-color: #F0F8F0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #40736A;
        margin: 0.5rem 0;
    }
    .rank-1 {
        background: linear-gradient(90deg, #FFD700 0%, #FFF8DC 100%);
        border-left-color: #FFD700;
        font-weight: bold;
    }
    .rank-2 {
        background: linear-gradient(90deg, #C0C0C0 0%, #F5F5F5 100%);
        border-left-color: #C0C0C0;
        font-weight: bold;
    }
    .rank-3 {
        background: linear-gradient(90deg, #CD7F32 0%, #F4E4BC 100%);
        border-left-color: #CD7F32;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="section-title">🏆 City Rankings</h1>', unsafe_allow_html=True)
    
    # Get data from session state
    if 'city_data' not in st.session_state or not st.session_state.city_data:
        st.warning("⚠️ No data available. Please add city data first in the Data section above.")
        return
    
    # Determine data type and adapt ranking
    use_custom = st.session_state.get('use_custom_indicators', False)
    
    if use_custom:
        show_custom_indicators_ranking()
    else:
        show_default_template_ranking()

def show_custom_indicators_ranking():
    """Show rankings for custom indicators data"""
    
    # Load custom indicators data
    indicators_data = load_custom_indicators_data()
    
    if indicators_data.empty:
        st.warning("⚠️ No custom indicators data found.")
        return
    
    summary = get_indicators_summary()
    
    st.info(f"🎯 **Custom Indicators Ranking** - Based on {summary['total_indicators']} indicators across {summary['unique_cities']} cities")
    
    # Ranking type selection
    ranking_type = st.selectbox(
        "Select Ranking Type:",
        [
            "Overall Performance Ranking",
            "Indicator-Specific Ranking",
            "Category-Based Ranking",
            "Custom Weighted Ranking"
        ]
    )
    
    if ranking_type == "Overall Performance Ranking":
        show_custom_overall_ranking(indicators_data)
    elif ranking_type == "Indicator-Specific Ranking":
        show_custom_indicator_ranking(indicators_data)
    elif ranking_type == "Category-Based Ranking":
        show_custom_category_ranking(indicators_data)
    else:
        show_custom_weighted_ranking(indicators_data)

def show_custom_overall_ranking(indicators_data):
    """Show overall performance ranking based on all indicators"""
    
    st.markdown('<h2 class="subsection-title">🌟 Overall Performance Ranking</h2>', unsafe_allow_html=True)
    
    st.info("📊 Cities ranked by their average performance across all indicators (normalized to 0-100 scale).")
    
    # Calculate overall scores
    city_scores = calculate_overall_scores(indicators_data)
    
    if city_scores.empty:
        st.warning("⚠️ Unable to calculate overall scores.")
        return
    
    # Display ranking
    display_ranking_cards(city_scores, "Overall Score")
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig = px.bar(
            x=city_scores.index,
            y=city_scores.values,
            title="Overall Performance Scores",
            color=city_scores.values,
            color_continuous_scale='Greens',
            labels={'x': 'City', 'y': 'Score'}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332',
            font_color='#2D5A3D'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Detailed breakdown
        st.markdown('<h3 class="metric-category">📈 Score Breakdown</h3>', unsafe_allow_html=True)
        
        # Show indicator count per city
        indicator_counts = indicators_data.groupby('City').size()
        
        for city in city_scores.index:
            indicator_count = indicator_counts.get(city, 0)
            score = city_scores[city]
            
            with st.container():
                st.write(f"**{city}**")
                st.write(f"Score: {score:.1f}/100")
                st.write(f"Indicators: {indicator_count}")
                st.progress(score / 100)
                st.write("---")

def show_custom_indicator_ranking(indicators_data):
    """Show ranking for a specific indicator"""
    
    st.markdown('<h2 class="subsection-title">📊 Indicator-Specific Ranking</h2>', unsafe_allow_html=True)
    
    # Select indicator
    available_indicators = indicators_data['Indicator_Name'].unique()
    selected_indicator = st.selectbox("Select indicator to rank by:", available_indicators)
    
    if not selected_indicator:
        return
    
    # Filter data for selected indicator
    indicator_data = indicators_data[indicators_data['Indicator_Name'] == selected_indicator]
    
    if indicator_data.empty:
        st.warning("⚠️ No data found for this indicator.")
        return
    
    # Show indicator details
    sample = indicator_data.iloc[0]
    
    st.markdown(f"""
    <div class="ranking-card">
    <strong>📈 {selected_indicator}</strong><br>
    <strong>Description:</strong> {sample['Description']}<br>
    <strong>Unit:</strong> {sample['Unit']}<br>
    <strong>Category:</strong> {sample.get('Category', 'Not specified')}
    </div>
    """, unsafe_allow_html=True)
    
    # Create ranking
    city_ranking = indicator_data.set_index('City')['Value'].sort_values(ascending=False)
    
    # Display ranking
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="metric-category">🏆 City Ranking</h3>', unsafe_allow_html=True)
        
        for rank, (city, value) in enumerate(city_ranking.items(), 1):
            rank_class = ""
            medal = ""
            
            if rank == 1:
                rank_class = "rank-1"
                medal = "🥇"
            elif rank == 2:
                rank_class = "rank-2"
                medal = "🥈"
            elif rank == 3:
                rank_class = "rank-3"
                medal = "🥉"
            else:
                medal = f"**{rank}.**"
            
            st.markdown(f"""
            <div class="ranking-card {rank_class}">
            {medal} <strong>{city}</strong><br>
            Value: {value} {sample['Unit']}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Bar chart
        fig = px.bar(
            x=city_ranking.index,
            y=city_ranking.values,
            title=f"{selected_indicator} by City",
            color=city_ranking.values,
            color_continuous_scale='Greens',
            labels={'x': 'City', 'y': sample['Unit']}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332',
            font_color='#2D5A3D'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.markdown('<h3 class="metric-category">📊 Statistics</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Best", f"{city_ranking.iloc[0]:.2f}")
    with col2:
        st.metric("Average", f"{city_ranking.mean():.2f}")
    with col3:
        st.metric("Worst", f"{city_ranking.iloc[-1]:.2f}")
    with col4:
        st.metric("Range", f"{city_ranking.iloc[0] - city_ranking.iloc[-1]:.2f}")

def show_custom_category_ranking(indicators_data):
    """Show ranking by indicator categories"""
    
    st.markdown('<h2 class="subsection-title">🏷️ Category-Based Ranking</h2>', unsafe_allow_html=True)
    
    if 'Category' not in indicators_data.columns:
        st.warning("⚠️ No category information available.")
        return
    
    # Select category
    available_categories = indicators_data['Category'].unique()
    selected_category = st.selectbox("Select category to rank by:", available_categories)
    
    if not selected_category:
        return
    
    # Filter data for selected category
    category_data = indicators_data[indicators_data['Category'] == selected_category]
    
    if category_data.empty:
        st.warning(f"⚠️ No data found for category: {selected_category}")
        return
    
    st.info(f"📊 Ranking cities based on their average performance in **{selected_category}** indicators.")
    
    # Calculate category scores for each city
    category_scores = calculate_category_scores(category_data)
    
    if category_scores.empty:
        st.warning("⚠️ Unable to calculate category scores.")
        return
    
    # Display ranking
    display_ranking_cards(category_scores, f"{selected_category} Score")
    
    # Show detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig = px.bar(
            x=category_scores.index,
            y=category_scores.values,
            title=f"{selected_category} Category Performance",
            color=category_scores.values,
            color_continuous_scale='Greens',
            labels={'x': 'City', 'y': 'Score'}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332',
            font_color='#2D5A3D'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # List indicators in this category
        st.markdown('<h3 class="metric-category">📋 Indicators in Category</h3>', unsafe_allow_html=True)
        indicators_in_category = category_data['Indicator_Name'].unique()
        
        for indicator in indicators_in_category:
            st.write(f"• {indicator}")
        
        # Show how many indicators each city has in this category
        city_indicator_counts = category_data.groupby('City').size()
        
        st.markdown('<h3 class="metric-category">📊 Indicator Coverage</h3>', unsafe_allow_html=True)
        for city, count in city_indicator_counts.items():
            st.write(f"**{city}:** {count} indicators")

def show_custom_weighted_ranking(indicators_data):
    """Show custom weighted ranking where users can assign weights to indicators"""
    
    st.markdown('<h2 class="subsection-title">⚖️ Custom Weighted Ranking</h2>', unsafe_allow_html=True)
    
    st.info("💡 Assign custom weights to indicators based on their importance to your research question.")
    
    # Get available indicators
    available_indicators = indicators_data['Indicator_Name'].unique()
    
    if len(available_indicators) == 0:
        st.warning("⚠️ No indicators available.")
        return
    
    # Weight assignment interface
    st.markdown('<h3 class="metric-category">🎛️ Assign Weights</h3>', unsafe_allow_html=True)
    
    weights = {}
    
    # Create sliders for each indicator
    for indicator in available_indicators:
        sample = indicators_data[indicators_data['Indicator_Name'] == indicator].iloc[0]
        
        with st.expander(f"⚖️ {indicator}", expanded=False):
            st.write(f"**Description:** {sample['Description']}")
            st.write(f"**Unit:** {sample['Unit']}")
            st.write(f"**Category:** {sample.get('Category', 'Not specified')}")
            
            weight = st.slider(
                f"Weight for {indicator}",
                min_value=0.0,
                max_value=10.0,
                value=5.0,
                step=0.1,
                key=f"weight_{indicator}",
                help="Higher weight = more important in final ranking"
            )
            weights[indicator] = weight
    
    # Calculate weighted scores
    if st.button("🏆 Calculate Weighted Ranking"):
        weighted_scores = calculate_weighted_scores(indicators_data, weights)
        
        if not weighted_scores.empty:
            # Display ranking
            display_ranking_cards(weighted_scores, "Weighted Score")
            
            # Visualization
            fig = px.bar(
                x=weighted_scores.index,
                y=weighted_scores.values,
                title="Custom Weighted Performance Ranking",
                color=weighted_scores.values,
                color_continuous_scale='Greens',
                labels={'x': 'City', 'y': 'Weighted Score'}
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                title_font_color='#1B4332',
                font_color='#2D5A3D'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show weight distribution
            with st.expander("⚖️ Weight Distribution", expanded=False):
                weight_df = pd.DataFrame(list(weights.items()), columns=['Indicator', 'Weight'])
                weight_df = weight_df[weight_df['Weight'] > 0].sort_values('Weight', ascending=False)
                
                if not weight_df.empty:
                    fig_weights = px.bar(
                        weight_df,
                        x='Indicator',
                        y='Weight',
                        title="Assigned Weights by Indicator"
                    )
                    fig_weights.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_weights, use_container_width=True)
        else:
            st.warning("⚠️ Unable to calculate weighted scores.")

def calculate_overall_scores(indicators_data):
    """Calculate overall performance scores for each city"""
    
    # Normalize all indicators to 0-100 scale
    normalized_data = []
    
    for indicator in indicators_data['Indicator_Name'].unique():
        indicator_subset = indicators_data[indicators_data['Indicator_Name'] == indicator].copy()
        
        # Min-max normalization
        min_val = indicator_subset['Value'].min()
        max_val = indicator_subset['Value'].max()
        
        if max_val > min_val:
            indicator_subset['Normalized_Value'] = ((indicator_subset['Value'] - min_val) / (max_val - min_val)) * 100
        else:
            indicator_subset['Normalized_Value'] = 50  # If all values are the same
        
        normalized_data.append(indicator_subset)
    
    if not normalized_data:
        return pd.Series()
    
    # Combine all normalized data
    all_normalized = pd.concat(normalized_data, ignore_index=True)
    
    # Calculate average score per city
    city_scores = all_normalized.groupby('City')['Normalized_Value'].mean().sort_values(ascending=False)
    
    return city_scores

def calculate_category_scores(category_data):
    """Calculate scores for a specific category"""
    
    # Normalize indicators within the category
    normalized_data = []
    
    for indicator in category_data['Indicator_Name'].unique():
        indicator_subset = category_data[category_data['Indicator_Name'] == indicator].copy()
        
        # Min-max normalization
        min_val = indicator_subset['Value'].min()
        max_val = indicator_subset['Value'].max()
        
        if max_val > min_val:
            indicator_subset['Normalized_Value'] = ((indicator_subset['Value'] - min_val) / (max_val - min_val)) * 100
        else:
            indicator_subset['Normalized_Value'] = 50
        
        normalized_data.append(indicator_subset)
    
    if not normalized_data:
        return pd.Series()
    
    # Combine and calculate average
    all_normalized = pd.concat(normalized_data, ignore_index=True)
    category_scores = all_normalized.groupby('City')['Normalized_Value'].mean().sort_values(ascending=False)
    
    return category_scores

def calculate_weighted_scores(indicators_data, weights):
    """Calculate weighted scores based on user-defined weights"""
    
    city_scores = {}
    
    # Get all cities
    cities = indicators_data['City'].unique()
    
    for city in cities:
        city_data = indicators_data[indicators_data['City'] == city]
        total_weighted_score = 0
        total_weight = 0
        
        for _, row in city_data.iterrows():
            indicator = row['Indicator_Name']
            value = row['Value']
            weight = weights.get(indicator, 0)
            
            if weight > 0:
                # Normalize value (simple approach)
                # In a more sophisticated approach, you'd normalize across all cities for this indicator
                all_values_for_indicator = indicators_data[indicators_data['Indicator_Name'] == indicator]['Value']
                min_val = all_values_for_indicator.min()
                max_val = all_values_for_indicator.max()
                
                if max_val > min_val:
                    normalized_value = ((value - min_val) / (max_val - min_val)) * 100
                else:
                    normalized_value = 50
                
                total_weighted_score += normalized_value * weight
                total_weight += weight
        
        if total_weight > 0:
            city_scores[city] = total_weighted_score / total_weight
    
    # Convert to Series and sort
    weighted_scores = pd.Series(city_scores).sort_values(ascending=False)
    
    return weighted_scores

def display_ranking_cards(scores, score_label):
    """Display ranking cards for cities"""
    
    st.markdown('<h3 class="metric-category">🏆 Final Ranking</h3>', unsafe_allow_html=True)
    
    for rank, (city, score) in enumerate(scores.items(), 1):
        rank_class = ""
        medal = ""
        
        if rank == 1:
            rank_class = "rank-1"
            medal = "🥇"
        elif rank == 2:
            rank_class = "rank-2"
            medal = "🥈"
        elif rank == 3:
            rank_class = "rank-3"
            medal = "🥉"
        else:
            medal = f"**{rank}.**"
        
        st.markdown(f"""
        <div class="ranking-card {rank_class}">
        {medal} <strong>{city}</strong><br>
        {score_label}: {score:.1f}
        </div>
        """, unsafe_allow_html=True)

def show_default_template_ranking():
    """Show rankings for default template data"""
    
    df = pd.DataFrame(st.session_state.city_data)
    
    st.info("📊 **Default Template Ranking** - Using predefined sustainability indicators")
    
    # Calculate scores if not already done
    if 'Overall_Score' not in df.columns:
        df = calculate_default_sustainability_scores(df)
    
    # Ranking type selection
    ranking_type = st.selectbox(
        "Select Ranking Type:",
        ["Overall Sustainability", "Environmental", "Social", "Economic"]
    )
    
    if ranking_type == "Overall Sustainability":
        show_default_overall_ranking(df)
    elif ranking_type == "Environmental":
        show_default_dimension_ranking(df, "Environmental")
    elif ranking_type == "Social":
        show_default_dimension_ranking(df, "Social")
    else:
        show_default_dimension_ranking(df, "Economic")

def calculate_default_sustainability_scores(df):
    """Calculate sustainability scores for default template data"""
    df = df.copy()
    
    # Environmental score
    env_cols = ['Air_Quality', 'Green_Space', 'Renewable_Energy']
    if all(col in df.columns for col in env_cols):
        df['Environmental_Score'] = df[env_cols].mean(axis=1) / 100
    else:
        df['Environmental_Score'] = 0
    
    # Social score
    social_cols = ['Education_Index', 'Healthcare_Access', 'Safety_Index']
    if all(col in df.columns for col in social_cols):
        df['Social_Score'] = (
            df['Education_Index'] +
            df['Healthcare_Access'] / 100 +
            df['Safety_Index'] / 10
        ) / 3
    else:
        df['Social_Score'] = 0
    
    # Economic score
    econ_cols = ['GDP_per_Capita', 'Innovation_Index', 'Unemployment_Rate']
    if all(col in df.columns for col in econ_cols):
        max_gdp = df['GDP_per_Capita'].max()
        df['Economic_Score'] = (
            df['GDP_per_Capita'] / max_gdp +
            df['Innovation_Index'] / 100 +
            (50 - df['Unemployment_Rate']) / 50
        ) / 3
    else:
        df['Economic_Score'] = 0
    
    # Overall score
    df['Overall_Score'] = (
        df['Environmental_Score'] +
        df['Social_Score'] +
        df['Economic_Score']
    ) / 3
    
    return df

def show_default_overall_ranking(df):
    """Show overall ranking for default template"""
    
    st.markdown('<h2 class="subsection-title">🌟 Overall Sustainability Ranking</h2>', unsafe_allow_html=True)
    
    # Sort by overall score
    ranked_df = df.sort_values('Overall_Score', ascending=False)
    
    # Display ranking
    for rank, (idx, row) in enumerate(ranked_df.iterrows(), 1):
        score_percent = row['Overall_Score'] * 100
        
        rank_class = ""
        medal = ""
        
        if rank == 1:
            rank_class = "rank-1"
            medal = "🥇"
        elif rank == 2:
            rank_class = "rank-2"
            medal = "🥈"
        elif rank == 3:
            rank_class = "rank-3"
            medal = "🥉"
        else:
            medal = f"**{rank}.**"
        
        st.markdown(f"""
        <div class="ranking-card {rank_class}">
        {medal} <strong>{row['City']}</strong><br>
        Overall Score: {score_percent:.1f}%<br>
        Environmental: {row['Environmental_Score']*100:.1f}% | 
        Social: {row['Social_Score']*100:.1f}% | 
        Economic: {row['Economic_Score']*100:.1f}%
        </div>
        """, unsafe_allow_html=True)
    
    # Visualization
    fig = px.bar(
        ranked_df,
        x='City',
        y='Overall_Score',
        title="Overall Sustainability Ranking",
        color='Overall_Score',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_color='#1B4332'
    )
    st.plotly_chart(fig, use_container_width=True)

def show_default_dimension_ranking(df, dimension):
    """Show ranking for a specific sustainability dimension"""
    
    st.markdown(f'<h2 class="subsection-title">📊 {dimension} Ranking</h2>', unsafe_allow_html=True)
    
    score_col = f"{dimension}_Score"
    
    if score_col not in df.columns:
        st.warning(f"⚠️ {dimension} scores not available.")
        return
    
    # Sort by dimension score
    ranked_df = df.sort_values(score_col, ascending=False)
    
    # Display ranking
    for rank, (idx, row) in enumerate(ranked_df.iterrows(), 1):
        score_percent = row[score_col] * 100
        
        rank_class = ""
        medal = ""
        
        if rank == 1:
            rank_class = "rank-1"
            medal = "🥇"
        elif rank == 2:
            rank_class = "rank-2"
            medal = "🥈"
        elif rank == 3:
            rank_class = "rank-3"
            medal = "🥉"
        else:
            medal = f"**{rank}.**"
        
        st.markdown(f"""
        <div class="ranking-card {rank_class}">
        {medal} <strong>{row['City']}</strong><br>
        {dimension} Score: {score_percent:.1f}%
        </div>
        """, unsafe_allow_html=True)
    
    # Visualization
    fig = px.bar(
        ranked_df,
        x='City',
        y=score_col,
        title=f"{dimension} Performance Ranking",
        color=score_col,
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_color='#1B4332'
    )
    st.plotly_chart(fig, use_container_width=True)
