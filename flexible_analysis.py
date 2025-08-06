"""
Flexible Analysis Module
This module handles analysis for both custom indicators and default template data,
adapting dynamically to whatever indicators are available in the dataset.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from custom_indicators import get_indicators_summary, load_custom_indicators_data

def show_analysis_section():
    """Display the analysis section with sustainability metrics - adapts to available data"""
    
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
    .indicator-card {
        background-color: #F0F8F0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #40736A;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="section-title">📈 Sustainability Analysis</h1>', unsafe_allow_html=True)
    
    # Get data from session state
    if 'city_data' not in st.session_state or not st.session_state.city_data:
        st.warning("⚠️ No data available. Please add city data first in the Data section above.")
        return
    
    # Determine data type and adapt analysis
    use_custom = st.session_state.get('use_custom_indicators', False)
    
    if use_custom:
        show_custom_indicators_analysis()
    else:
        show_default_template_analysis()

def show_custom_indicators_analysis():
    """Show analysis for custom indicators data"""
    
    # Load custom indicators data
    indicators_data = load_custom_indicators_data()
    
    if indicators_data.empty:
        st.warning("⚠️ No custom indicators data found.")
        return
    
    # Get summary information
    summary = get_indicators_summary()
    
    st.info(f"📊 **Custom Indicators Analysis** - {summary['total_indicators']} indicators across {summary['unique_cities']} cities")
    
    # Analysis options
    analysis_type = st.selectbox(
        "Select Analysis Type:",
        [
            "Overview Dashboard",
            "City Comparison",
            "Indicator Analysis",
            "Category Analysis",
            "Data Explorer"
        ]
    )
    
    if analysis_type == "Overview Dashboard":
        show_custom_overview(indicators_data, summary)
    elif analysis_type == "City Comparison":
        show_custom_city_comparison(indicators_data)
    elif analysis_type == "Indicator Analysis":
        show_custom_indicator_analysis(indicators_data)
    elif analysis_type == "Category Analysis":
        show_custom_category_analysis(indicators_data, summary)
    else:
        show_custom_data_explorer(indicators_data)

def show_custom_overview(indicators_data, summary):
    """Show overview dashboard for custom indicators"""
    
    st.markdown('<h2 class="subsection-title">🎯 Overview Dashboard</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Indicators", summary['total_indicators'])
    with col2:
        st.metric("Cities", summary['unique_cities'])
    with col3:
        avg_per_city = summary['total_indicators'] / max(summary['unique_cities'], 1)
        st.metric("Avg per City", f"{avg_per_city:.1f}")
    with col4:
        st.metric("Categories", len(summary['categories']))
    
    # Indicators per city
    st.markdown('<h3 class="metric-category">📊 Indicators per City</h3>', unsafe_allow_html=True)
    
    city_counts = pd.DataFrame(list(summary['indicators_per_city'].items()), 
                              columns=['City', 'Indicator_Count'])
    
    fig = px.bar(
        city_counts,
        x='City',
        y='Indicator_Count',
        title="Number of Indicators per City",
        color='Indicator_Count',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_color='#1B4332',
        font_color='#2D5A3D'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Category distribution
    if summary['categories']:
        st.markdown('<h3 class="metric-category">🏷️ Indicators by Category</h3>', unsafe_allow_html=True)
        
        category_df = pd.DataFrame(list(summary['categories'].items()), 
                                  columns=['Category', 'Count'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                category_df,
                values='Count',
                names='Category',
                title="Distribution by Category",
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig.update_layout(title_font_color='#1B4332')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category breakdown per city
            category_city = indicators_data.groupby(['City', 'Category']).size().unstack(fill_value=0)
            
            fig = px.bar(
                category_city,
                title="Indicators by Category per City",
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                title_font_color='#1B4332',
                font_color='#2D5A3D'
            )
            st.plotly_chart(fig, use_container_width=True)

def show_custom_city_comparison(indicators_data):
    """Show city-by-city comparison of indicators"""
    
    st.markdown('<h2 class="subsection-title">🏙️ City Comparison</h2>', unsafe_allow_html=True)
    
    # Select cities to compare
    available_cities = indicators_data['City'].unique()
    selected_cities = st.multiselect(
        "Select cities to compare (max 4):",
        available_cities,
        default=available_cities[:min(4, len(available_cities))]
    )
    
    if len(selected_cities) < 2:
        st.warning("⚠️ Please select at least 2 cities to compare.")
        return
    
    # Filter data for selected cities
    filtered_data = indicators_data[indicators_data['City'].isin(selected_cities)]
    
    # Select indicators to compare
    available_indicators = filtered_data['Indicator_Name'].unique()
    selected_indicators = st.multiselect(
        "Select indicators to compare:",
        available_indicators,
        default=available_indicators[:min(6, len(available_indicators))]
    )
    
    if not selected_indicators:
        st.warning("⚠️ Please select at least one indicator.")
        return
    
    # Create comparison chart
    comparison_data = filtered_data[
        (filtered_data['City'].isin(selected_cities)) & 
        (filtered_data['Indicator_Name'].isin(selected_indicators))
    ]
    
    # Pivot for easier plotting
    pivot_data = comparison_data.pivot(index='City', columns='Indicator_Name', values='Value')
    
    # Create radar chart
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    
    for i, city in enumerate(selected_cities):
        if city in pivot_data.index:
            values = []
            labels = []
            
            for indicator in selected_indicators:
                if indicator in pivot_data.columns and not pd.isna(pivot_data.loc[city, indicator]):
                    values.append(pivot_data.loc[city, indicator])
                    labels.append(indicator)
            
            if values:  # Only add trace if we have data
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself',
                    name=city,
                    line_color=colors[i % len(colors)],
                    opacity=0.7
                ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(comparison_data['Value']) * 1.1] if not comparison_data.empty else [0, 100]
            )),
        showlegend=True,
        title="City Comparison - Selected Indicators",
        title_font_color='#1B4332'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.markdown('<h3 class="metric-category">📋 Comparison Data</h3>', unsafe_allow_html=True)
    display_data = comparison_data[['City', 'Indicator_Name', 'Value', 'Unit', 'Source']].copy()
    st.dataframe(display_data, use_container_width=True)

def show_custom_indicator_analysis(indicators_data):
    """Show analysis focused on specific indicators"""
    
    st.markdown('<h2 class="subsection-title">📈 Indicator Analysis</h2>', unsafe_allow_html=True)
    
    # Select indicator to analyze
    available_indicators = indicators_data['Indicator_Name'].unique()
    selected_indicator = st.selectbox("Select indicator to analyze:", available_indicators)
    
    if not selected_indicator:
        return
    
    # Filter data for selected indicator
    indicator_data = indicators_data[indicators_data['Indicator_Name'] == selected_indicator]
    
    if indicator_data.empty:
        st.warning("⚠️ No data found for this indicator.")
        return
    
    # Show indicator details
    sample = indicator_data.iloc[0]
    
    with st.container():
        st.markdown(f'<div class="indicator-card">', unsafe_allow_html=True)
        st.markdown(f"**📊 {selected_indicator}**")
        st.markdown(f"**Description:** {sample['Description']}")
        st.markdown(f"**Unit:** {sample['Unit']}")
        st.markdown(f"**Category:** {sample.get('Category', 'Not specified')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart of values by city
        fig = px.bar(
            indicator_data,
            x='City',
            y='Value',
            title=f"{selected_indicator} by City",
            color='Value',
            color_continuous_scale='Greens'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332',
            font_color='#2D5A3D'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Statistics
        st.markdown('<h3 class="metric-category">📊 Statistics</h3>', unsafe_allow_html=True)
        
        values = indicator_data['Value']
        st.metric("Maximum", f"{values.max():.2f} {sample['Unit']}")
        st.metric("Average", f"{values.mean():.2f} {sample['Unit']}")
        st.metric("Minimum", f"{values.min():.2f} {sample['Unit']}")
        st.metric("Std Deviation", f"{values.std():.2f}")
        
        # Best and worst performing cities
        best_city = indicator_data.loc[indicator_data['Value'].idxmax(), 'City']
        worst_city = indicator_data.loc[indicator_data['Value'].idxmin(), 'City']
        
        st.success(f"🏆 **Best:** {best_city}")
        st.error(f"📉 **Lowest:** {worst_city}")
    
    # Data sources
    st.markdown('<h3 class="metric-category">📚 Data Sources</h3>', unsafe_allow_html=True)
    sources = indicator_data[['City', 'Source']].drop_duplicates()
    st.dataframe(sources, use_container_width=True)

def show_custom_category_analysis(indicators_data, summary):
    """Show analysis by indicator categories"""
    
    st.markdown('<h2 class="subsection-title">🏷️ Category Analysis</h2>', unsafe_allow_html=True)
    
    if not summary['categories']:
        st.warning("⚠️ No category information available.")
        return
    
    # Select category to analyze
    selected_category = st.selectbox("Select category to analyze:", list(summary['categories'].keys()))
    
    if not selected_category:
        return
    
    # Filter data for selected category
    category_data = indicators_data[indicators_data['Category'] == selected_category]
    
    st.info(f"📊 **{selected_category} Category** - {len(category_data)} indicators")
    
    # Overview of indicators in this category
    indicators_in_category = category_data['Indicator_Name'].unique()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="metric-category">📋 Indicators in Category</h3>', unsafe_allow_html=True)
        for indicator in indicators_in_category:
            st.write(f"• {indicator}")
    
    with col2:
        # Cities coverage in this category
        city_coverage = category_data.groupby('City').size()
        
        fig = px.bar(
            x=city_coverage.index,
            y=city_coverage.values,
            title=f"{selected_category} Indicators per City",
            color=city_coverage.values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332',
            font_color='#2D5A3D'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis if there are multiple indicators
    if len(indicators_in_category) > 1:
        st.markdown('<h3 class="metric-category">🔍 Category Deep Dive</h3>', unsafe_allow_html=True)
        
        # Create a heatmap of all indicators in this category
        pivot_data = category_data.pivot(index='City', columns='Indicator_Name', values='Value')
        
        if not pivot_data.empty:
            fig = px.imshow(
                pivot_data,
                title=f"{selected_category} Indicators Heatmap",
                color_continuous_scale='Greens',
                aspect='auto'
            )
            fig.update_layout(title_font_color='#1B4332')
            st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed data
    st.markdown('<h3 class="metric-category">📋 Category Data</h3>', unsafe_allow_html=True)
    display_data = category_data[['City', 'Indicator_Name', 'Value', 'Unit', 'Description']].copy()
    st.dataframe(display_data, use_container_width=True)

def show_custom_data_explorer(indicators_data):
    """Show interactive data explorer"""
    
    st.markdown('<h2 class="subsection-title">🔍 Data Explorer</h2>', unsafe_allow_html=True)
    
    st.info("💡 Explore your data interactively. Filter and search to find insights.")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        city_filter = st.multiselect(
            "Filter by City:",
            indicators_data['City'].unique(),
            default=indicators_data['City'].unique()
        )
    
    with col2:
        category_filter = st.multiselect(
            "Filter by Category:",
            indicators_data['Category'].unique() if 'Category' in indicators_data.columns else [],
            default=indicators_data['Category'].unique() if 'Category' in indicators_data.columns else []
        )
    
    with col3:
        # Value range filter
        min_val, max_val = float(indicators_data['Value'].min()), float(indicators_data['Value'].max())
        value_range = st.slider(
            "Value Range:",
            min_val, max_val,
            (min_val, max_val)
        )
    
    # Apply filters
    filtered_data = indicators_data[
        (indicators_data['City'].isin(city_filter)) &
        (indicators_data['Value'] >= value_range[0]) &
        (indicators_data['Value'] <= value_range[1])
    ]
    
    if 'Category' in indicators_data.columns and category_filter:
        filtered_data = filtered_data[filtered_data['Category'].isin(category_filter)]
    
    # Search functionality
    search_term = st.text_input("🔍 Search indicators or descriptions:", "")
    
    if search_term:
        mask = (
            filtered_data['Indicator_Name'].str.contains(search_term, case=False, na=False) |
            filtered_data['Description'].str.contains(search_term, case=False, na=False)
        )
        filtered_data = filtered_data[mask]
    
    # Results
    st.markdown(f"**Results:** {len(filtered_data)} indicators found")
    
    if not filtered_data.empty:
        # Visualization options
        viz_type = st.selectbox(
            "Visualization:",
            ["Table View", "Scatter Plot", "Bar Chart", "Box Plot"]
        )
        
        if viz_type == "Table View":
            st.dataframe(filtered_data, use_container_width=True)
        
        elif viz_type == "Scatter Plot":
            if len(filtered_data['Indicator_Name'].unique()) >= 2:
                x_indicator = st.selectbox("X-axis indicator:", filtered_data['Indicator_Name'].unique())
                y_indicator = st.selectbox("Y-axis indicator:", 
                                         [i for i in filtered_data['Indicator_Name'].unique() if i != x_indicator])
                
                x_data = filtered_data[filtered_data['Indicator_Name'] == x_indicator]
                y_data = filtered_data[filtered_data['Indicator_Name'] == y_indicator]
                
                # Merge data for plotting
                merged = pd.merge(x_data[['City', 'Value']], y_data[['City', 'Value']], 
                                on='City', suffixes=('_x', '_y'))
                
                if not merged.empty:
                    fig = px.scatter(
                        merged,
                        x='Value_x',
                        y='Value_y',
                        hover_data=['City'],
                        title=f"{x_indicator} vs {y_indicator}",
                        labels={'Value_x': x_indicator, 'Value_y': y_indicator}
                    )
                    fig.update_layout(title_font_color='#1B4332')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Need at least 2 different indicators for scatter plot.")
        
        elif viz_type == "Bar Chart":
            selected_indicator = st.selectbox("Select indicator:", filtered_data['Indicator_Name'].unique())
            plot_data = filtered_data[filtered_data['Indicator_Name'] == selected_indicator]
            
            fig = px.bar(
                plot_data,
                x='City',
                y='Value',
                title=selected_indicator,
                color='Value',
                color_continuous_scale='Greens'
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                title_font_color='#1B4332'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Box Plot":
            if 'Category' in filtered_data.columns:
                fig = px.box(
                    filtered_data,
                    x='Category',
                    y='Value',
                    title="Value Distribution by Category"
                )
                fig.update_layout(
                    xaxis_tickangle=-45,
                    title_font_color='#1B4332'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Category information not available for box plot.")
    
    else:
        st.warning("No data matches your current filters.")

def show_default_template_analysis():
    """Show analysis for default template data (original functionality)"""
    
    df = pd.DataFrame(st.session_state.city_data)
    
    # Calculate sustainability scores
    df_with_scores = calculate_sustainability_scores(df)
    
    st.info("📊 **Default Template Analysis** - Using predefined sustainability indicators")
    
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
    """Calculate sustainability scores for each dimension (for default template)"""
    df = df.copy()
    
    # Check if required columns exist
    env_cols = ['Air_Quality', 'Green_Space', 'Renewable_Energy']
    social_cols = ['Education_Index', 'Healthcare_Access', 'Safety_Index']
    econ_cols = ['GDP_per_Capita', 'Innovation_Index', 'Unemployment_Rate']
    
    # Environmental score (higher is better)
    if all(col in df.columns for col in env_cols):
        df['Environmental_Score'] = (
            df['Air_Quality'] / 100 +
            df['Green_Space'] / 100 +
            df['Renewable_Energy'] / 100
        ) / 3
    else:
        df['Environmental_Score'] = 0
    
    # Social score (higher is better, but normalize Safety_Index and Healthcare_Access)
    if all(col in df.columns for col in social_cols):
        df['Social_Score'] = (
            df['Education_Index'] +
            df['Healthcare_Access'] / 100 +
            df['Safety_Index'] / 10
        ) / 3
    else:
        df['Social_Score'] = 0
    
    # Economic score (normalize and invert unemployment rate as it's negative)
    if all(col in df.columns for col in econ_cols):
        max_gdp = df['GDP_per_Capita'].max()
        df['Economic_Score'] = (
            df['GDP_per_Capita'] / max_gdp +
            df['Innovation_Index'] / 100 +
            (50 - df['Unemployment_Rate']) / 50  # Invert unemployment rate
        ) / 3
    else:
        df['Economic_Score'] = 0
    
    # Overall sustainability score
    df['Overall_Score'] = (
        df['Environmental_Score'] +
        df['Social_Score'] +
        df['Economic_Score']
    ) / 3
    
    return df

def show_overview_dashboard(df):
    """Show overview dashboard with key metrics (for default template)"""
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

def show_environmental_analysis(df):
    """Show environmental analysis (placeholder for default template)"""
    st.markdown('<h2 class="subsection-title">🌱 Environmental Analysis</h2>', unsafe_allow_html=True)
    st.info("Environmental analysis for default template data")
    
    # Show available environmental columns
    env_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['air', 'green', 'renewable', 'water', 'waste'])]
    
    if env_cols:
        st.dataframe(df[['City'] + env_cols])
    else:
        st.warning("No environmental indicators found in the data.")

def show_social_analysis(df):
    """Show social analysis (placeholder for default template)"""
    st.markdown('<h2 class="subsection-title">👥 Social Analysis</h2>', unsafe_allow_html=True)
    st.info("Social analysis for default template data")
    
    # Show available social columns
    social_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['education', 'health', 'safety', 'social', 'housing'])]
    
    if social_cols:
        st.dataframe(df[['City'] + social_cols])
    else:
        st.warning("No social indicators found in the data.")

def show_economic_analysis(df):
    """Show economic analysis (placeholder for default template)"""
    st.markdown('<h2 class="subsection-title">💰 Economic Analysis</h2>', unsafe_allow_html=True)
    st.info("Economic analysis for default template data")
    
    # Show available economic columns
    econ_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['gdp', 'income', 'unemployment', 'innovation', 'business'])]
    
    if econ_cols:
        st.dataframe(df[['City'] + econ_cols])
    else:
        st.warning("No economic indicators found in the data.")

def show_comparative_analysis(df):
    """Show comparative analysis (placeholder for default template)"""
    st.markdown('<h2 class="subsection-title">⚖️ Comparative Analysis</h2>', unsafe_allow_html=True)
    st.info("Comparative analysis for default template data")
    
    # Show basic comparison
    if 'Overall_Score' in df.columns:
        fig = px.bar(
            df,
            x='City',
            y='Overall_Score',
            title="City Comparison - Overall Scores",
            color='Overall_Score',
            color_continuous_scale='Greens'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font_color='#1B4332'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(df)
