"""
Flexible Spider Plot Module
This module creates spider plots that adapt to any custom indicators or default template data.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from custom_indicators import load_custom_indicators_data, get_indicators_summary

def show_spider_plot_section():
    """Display interactive spider plots for sustainability assessment - adapts to available data"""
    
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
    .spider-info {
        background-color: #E8F5E8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #40736A;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="section-title">🕸️ Spider Plot Visualization</h1>', unsafe_allow_html=True)
    
    # Get data from session state
    if 'city_data' not in st.session_state or not st.session_state.city_data:
        st.warning("⚠️ No data available. Please add city data first in the Data section above.")
        return
    
    # Determine data type and adapt visualization
    use_custom = st.session_state.get('use_custom_indicators', False)
    
    if use_custom:
        show_custom_indicators_spider_plots()
    else:
        show_default_template_spider_plots()

def show_custom_indicators_spider_plots():
    """Show spider plots for custom indicators data"""
    
    # Load custom indicators data
    indicators_data = load_custom_indicators_data()
    
    if indicators_data.empty:
        st.warning("⚠️ No custom indicators data found.")
        return
    
    summary = get_indicators_summary()
    
    st.markdown("""
    <div class="spider-info">
    <strong>🎯 Custom Indicators Spider Plot</strong><br>
    Spider plots help visualize multiple indicators simultaneously, making it easy to compare cities across different dimensions.
    </div>
    """, unsafe_allow_html=True)
    
    # Plot type selection
    plot_type = st.selectbox(
        "Select Visualization Type:",
        [
            "City Comparison Spider",
            "Category-Based Spider",
            "Selected Indicators Spider",
            "All Indicators Overview"
        ]
    )
    
    if plot_type == "City Comparison Spider":
        show_custom_city_comparison_spider(indicators_data)
    elif plot_type == "Category-Based Spider":
        show_custom_category_spider(indicators_data)
    elif plot_type == "Selected Indicators Spider":
        show_custom_selected_indicators_spider(indicators_data)
    else:
        show_custom_overview_spider(indicators_data)

def show_custom_city_comparison_spider(indicators_data):
    """Show spider plot comparing selected cities across their indicators"""
    
    st.markdown('<h2 class="subsection-title">🏙️ City Comparison Spider Plot</h2>', unsafe_allow_html=True)
    
    # Select cities to compare
    available_cities = indicators_data['City'].unique()
    
    if len(available_cities) < 2:
        st.warning("⚠️ Need at least 2 cities for comparison.")
        return
    
    selected_cities = st.multiselect(
        "Select cities to compare (max 4 recommended):",
        available_cities,
        default=available_cities[:min(4, len(available_cities))]
    )
    
    if len(selected_cities) < 2:
        st.warning("⚠️ Please select at least 2 cities.")
        return
    
    # Select indicators for the spider plot
    available_indicators = indicators_data['Indicator_Name'].unique()
    selected_indicators = st.multiselect(
        "Select indicators for spider plot (3-8 recommended):",
        available_indicators,
        default=available_indicators[:min(6, len(available_indicators))]
    )
    
    if len(selected_indicators) < 3:
        st.warning("⚠️ Please select at least 3 indicators for a meaningful spider plot.")
        return
    
    # Create spider plot
    fig = create_custom_spider_plot(indicators_data, selected_cities, selected_indicators)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Show data table (without expander since we're already in one)
        st.markdown("**📊 Data Used in Spider Plot:**")
        comparison_data = indicators_data[
            (indicators_data['City'].isin(selected_cities)) &
            (indicators_data['Indicator_Name'].isin(selected_indicators))
        ]
        pivot_data = comparison_data.pivot(index='City', columns='Indicator_Name', values='Value')
        st.dataframe(pivot_data, use_container_width=True)

def show_custom_category_spider(indicators_data):
    """Show spider plots organized by indicator categories"""
    
    st.markdown('<h2 class="subsection-title">🏷️ Category-Based Spider Plot</h2>', unsafe_allow_html=True)
    
    if 'Category' not in indicators_data.columns:
        st.warning("⚠️ No category information available in the data.")
        return
    
    # Select category
    available_categories = indicators_data['Category'].unique()
    selected_category = st.selectbox("Select category to visualize:", available_categories)
    
    if not selected_category:
        return
    
    # Filter data for selected category
    category_data = indicators_data[indicators_data['Category'] == selected_category]
    
    if category_data.empty:
        st.warning(f"⚠️ No data found for category: {selected_category}")
        return
    
    # Select cities
    available_cities = category_data['City'].unique()
    selected_cities = st.multiselect(
        "Select cities to compare:",
        available_cities,
        default=available_cities
    )
    
    if not selected_cities:
        st.warning("⚠️ Please select at least one city.")
        return
    
    # Get all indicators in this category
    category_indicators = category_data['Indicator_Name'].unique()
    
    st.info(f"📊 Showing all **{selected_category}** indicators: {', '.join(category_indicators)}")
    
    # Create spider plot
    fig = create_custom_spider_plot(category_data, selected_cities, category_indicators)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def show_custom_selected_indicators_spider(indicators_data):
    """Show spider plot with user-selected indicators"""
    
    st.markdown('<h2 class="subsection-title">🎯 Custom Indicator Selection</h2>', unsafe_allow_html=True)
    
    st.info("💡 Choose specific indicators and cities to create a focused comparison.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Select indicators
        available_indicators = indicators_data['Indicator_Name'].unique()
        selected_indicators = st.multiselect(
            "Select indicators (3-10 recommended):",
            available_indicators,
            help="Choose indicators that are relevant to your analysis"
        )
    
    with col2:
        # Select cities
        available_cities = indicators_data['City'].unique()
        selected_cities = st.multiselect(
            "Select cities:",
            available_cities,
            default=available_cities
        )
    
    if len(selected_indicators) >= 3 and len(selected_cities) >= 1:
        
        # Show indicator details (without expander since we're already in one)
        st.markdown("**📋 Selected Indicators Details:**")
        for indicator in selected_indicators:
            indicator_info = indicators_data[indicators_data['Indicator_Name'] == indicator].iloc[0]
            st.write(f"**{indicator}:** {indicator_info['Description']} ({indicator_info['Unit']})")
        
        st.markdown("---")  # Visual separator
        
        # Create spider plot
        fig = create_custom_spider_plot(indicators_data, selected_cities, selected_indicators)
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Normalization explanation
            st.markdown("""
            <div class="spider-info">
            <strong>📊 Normalization Note:</strong> Values are normalized to 0-100 scale for visualization. 
            Higher values (further from center) indicate better performance for that indicator.
            </div>
            """, unsafe_allow_html=True)
    
    else:
        if len(selected_indicators) < 3:
            st.warning("⚠️ Please select at least 3 indicators.")
        if len(selected_cities) < 1:
            st.warning("⚠️ Please select at least 1 city.")

def show_custom_overview_spider(indicators_data):
    """Show overview spider plot with key indicators"""
    
    st.markdown('<h2 class="subsection-title">🌟 Overview Spider Plot</h2>', unsafe_allow_html=True)
    
    st.info("📊 This view shows the most important indicators for each city in a comprehensive spider plot.")
    
    # Auto-select important indicators (limit to avoid overcrowding)
    all_indicators = indicators_data['Indicator_Name'].unique()
    
    # Limit to 8 indicators for readability
    max_indicators = min(8, len(all_indicators))
    selected_indicators = all_indicators[:max_indicators]
    
    if len(selected_indicators) < 3:
        st.warning("⚠️ Need at least 3 indicators for overview plot.")
        return
    
    # Get all cities
    all_cities = indicators_data['City'].unique()
    
    st.write(f"**Showing:** {len(selected_indicators)} indicators across {len(all_cities)} cities")
    st.write(f"**Indicators:** {', '.join(selected_indicators)}")
    
    # Create spider plot
    fig = create_custom_spider_plot(indicators_data, all_cities, selected_indicators)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Show ranking based on total area (without expander since we're already in one)
        st.markdown("**🏆 Performance Ranking:**")
        calculate_spider_ranking(indicators_data, all_cities, selected_indicators)

def create_custom_spider_plot(indicators_data, cities, indicators):
    """Create a spider plot for custom indicators"""
    
    if not cities or not indicators:
        return None
    
    # Filter data
    filtered_data = indicators_data[
        (indicators_data['City'].isin(cities)) &
        (indicators_data['Indicator_Name'].isin(indicators))
    ]
    
    if filtered_data.empty:
        st.warning("⚠️ No data available for the selected combination.")
        return None
    
    # Pivot data for easier plotting
    pivot_data = filtered_data.pivot(index='City', columns='Indicator_Name', values='Value')
    
    # Handle missing data
    pivot_data = pivot_data.fillna(0)
    
    # Normalize data to 0-100 scale
    normalized_data = normalize_custom_indicators(pivot_data)
    
    # Create spider plot
    fig = go.Figure()
    
    # Color palette
    colors = px.colors.qualitative.Set2
    
    for i, city in enumerate(cities):
        if city in normalized_data.index:
            values = []
            labels = []
            
            for indicator in indicators:
                if indicator in normalized_data.columns:
                    values.append(normalized_data.loc[city, indicator])
                    labels.append(indicator)
            
            if values:  # Only add trace if we have data
                # Close the polygon
                values.append(values[0])
                labels.append(labels[0])
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself',
                    name=city,
                    line_color=colors[i % len(colors)],
                    opacity=0.7
                ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickfont=dict(size=10),
                rotation=90,
                direction='clockwise'
            )
        ),
        showlegend=True,
        title={
            'text': f"Spider Plot: {', '.join(cities)} - {len(indicators)} Indicators",
            'x': 0.5,
            'font': {'color': '#1B4332', 'size': 16}
        },
        font=dict(color='#2D5A3D'),
        height=600
    )
    
    return fig

def normalize_custom_indicators(pivot_data):
    """Normalize custom indicators to 0-100 scale"""
    
    normalized = pivot_data.copy()
    
    # Normalize each column to 0-100 scale using min-max normalization
    for column in normalized.columns:
        min_val = normalized[column].min()
        max_val = normalized[column].max()
        
        if max_val > min_val:
            normalized[column] = ((normalized[column] - min_val) / (max_val - min_val)) * 100
        else:
            # If all values are the same, set to 50
            normalized[column] = 50
    
    return normalized

def calculate_spider_ranking(indicators_data, cities, indicators):
    """Calculate ranking based on spider plot area/performance"""
    
    # Filter data
    filtered_data = indicators_data[
        (indicators_data['City'].isin(cities)) &
        (indicators_data['Indicator_Name'].isin(indicators))
    ]
    
    # Pivot and normalize
    pivot_data = filtered_data.pivot(index='City', columns='Indicator_Name', values='Value')
    normalized_data = normalize_custom_indicators(pivot_data.fillna(0))
    
    # Calculate average performance (simple metric)
    city_scores = normalized_data.mean(axis=1).sort_values(ascending=False)
    
    # Display ranking
    for rank, (city, score) in enumerate(city_scores.items(), 1):
        if rank == 1:
            st.success(f"🥇 **{rank}. {city}** - Average Score: {score:.1f}")
        elif rank == 2:
            st.info(f"🥈 **{rank}. {city}** - Average Score: {score:.1f}")
        elif rank == 3:
            st.info(f"🥉 **{rank}. {city}** - Average Score: {score:.1f}")
        else:
            st.write(f"**{rank}. {city}** - Average Score: {score:.1f}")

def show_default_template_spider_plots():
    """Show spider plots for default template data"""
    
    df = pd.DataFrame(st.session_state.city_data)
    
    st.markdown("""
    <div class="spider-info">
    <strong>📊 Default Template Spider Plot</strong><br>
    Visualizing cities using standard sustainability indicators across Environmental, Social, and Economic dimensions.
    </div>
    """, unsafe_allow_html=True)
    
    # Normalize data for spider plots
    df_normalized = normalize_default_data_for_spider(df)
    
    # Plot type selection
    plot_type = st.selectbox(
        "Select Spider Plot Type:",
        ["All Cities Overview", "Selected Cities", "By Dimension", "Individual City"]
    )
    
    if plot_type == "All Cities Overview":
        show_default_overview_spider(df_normalized)
    elif plot_type == "Selected Cities":
        show_default_selected_cities_spider(df_normalized)
    elif plot_type == "By Dimension":
        show_default_dimension_spider(df_normalized)
    else:
        show_default_individual_spider(df_normalized)

def normalize_default_data_for_spider(df):
    """Normalize default template data to 0-100 scale for spider plots"""
    df = df.copy()
    
    # Define standard metrics and their normalization
    metrics_config = {
        # Environmental metrics (higher is better)
        'Air_Quality': {'scale': 100, 'invert': False},
        'Green_Space': {'scale': 100, 'invert': False},
        'Renewable_Energy': {'scale': 100, 'invert': False},
        'Waste_Management': {'scale': 100, 'invert': False},
        'Water_Quality': {'scale': 100, 'invert': False},
        
        # Social metrics
        'Education_Index': {'scale': 1, 'invert': False},
        'Healthcare_Access': {'scale': 100, 'invert': False},
        'Safety_Index': {'scale': 10, 'invert': False},
        'Social_Inclusion': {'scale': 100, 'invert': False},
        'Housing_Affordability': {'scale': 100, 'invert': False},
        
        # Economic metrics
        'GDP_per_Capita': {'scale': None, 'invert': False},
        'Unemployment_Rate': {'scale': 100, 'invert': True},
        'Innovation_Index': {'scale': 100, 'invert': False},
        'Business_Environment': {'scale': 100, 'invert': False},
        'Income_Equality': {'scale': 100, 'invert': False}
    }
    
    # Normalize each metric
    for metric, config in metrics_config.items():
        if metric in df.columns:
            if config['scale'] is None:
                # Normalize to 0-100 based on min-max
                min_val = df[metric].min()
                max_val = df[metric].max()
                if max_val > min_val:
                    df[f"{metric}_normalized"] = ((df[metric] - min_val) / (max_val - min_val)) * 100
                else:
                    df[f"{metric}_normalized"] = 50
            else:
                # Direct scaling
                if config['invert']:
                    df[f"{metric}_normalized"] = 100 - (df[metric] / config['scale'] * 100)
                else:
                    if config['scale'] == 1:  # Education_Index case
                        df[f"{metric}_normalized"] = df[metric] * 100
                    elif config['scale'] == 10:  # Safety_Index case
                        df[f"{metric}_normalized"] = (df[metric] / 10) * 100
                    else:
                        df[f"{metric}_normalized"] = (df[metric] / config['scale']) * 100
    
    return df

def show_default_overview_spider(df_normalized):
    """Show overview spider plot for default template"""
    
    st.markdown('<h2 class="subsection-title">🌟 All Cities Overview</h2>', unsafe_allow_html=True)
    
    # Select key indicators for overview
    key_indicators = [
        'Air_Quality_normalized', 'Green_Space_normalized', 'Renewable_Energy_normalized',
        'Education_Index_normalized', 'Healthcare_Access_normalized', 'Safety_Index_normalized',
        'GDP_per_Capita_normalized', 'Innovation_Index_normalized'
    ]
    
    # Filter to available indicators
    available_indicators = [ind for ind in key_indicators if ind in df_normalized.columns]
    
    if len(available_indicators) < 3:
        st.warning("⚠️ Not enough indicators available for spider plot.")
        return
    
    # Create spider plot
    fig = go.Figure()
    colors = px.colors.qualitative.Set2
    
    for i, (idx, row) in enumerate(df_normalized.iterrows()):
        values = [row[ind] for ind in available_indicators]
        labels = [ind.replace('_normalized', '').replace('_', ' ') for ind in available_indicators]
        
        # Close the polygon
        values.append(values[0])
        labels.append(labels[0])
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=row['City'],
            line_color=colors[i % len(colors)],
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10),
                rotation=90,
                direction='clockwise'
            )
        ),
        showlegend=True,
        title={
            'text': "City Sustainability Overview - Spider Plot",
            'x': 0.5,
            'font': {'color': '#1B4332', 'size': 16}
        },
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_default_selected_cities_spider(df_normalized):
    """Show spider plot for selected cities in default template"""
    
    st.markdown('<h2 class="subsection-title">🏙️ Selected Cities Comparison</h2>', unsafe_allow_html=True)
    
    # City selection
    available_cities = df_normalized['City'].tolist()
    selected_cities = st.multiselect(
        "Select cities to compare:",
        available_cities,
        default=available_cities[:min(3, len(available_cities))]
    )
    
    if not selected_cities:
        st.warning("⚠️ Please select at least one city.")
        return
    
    # Filter data
    filtered_df = df_normalized[df_normalized['City'].isin(selected_cities)]
    
    # Standard indicators
    indicators = [col for col in df_normalized.columns if col.endswith('_normalized')]
    
    if len(indicators) < 3:
        st.warning("⚠️ Not enough normalized indicators available.")
        return
    
    # Create spider plot
    fig = go.Figure()
    colors = px.colors.qualitative.Set2
    
    for i, (idx, row) in enumerate(filtered_df.iterrows()):
        values = [row[ind] for ind in indicators]
        labels = [ind.replace('_normalized', '').replace('_', ' ') for ind in indicators]
        
        # Close the polygon
        values.append(values[0])
        labels.append(labels[0])
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=row['City'],
            line_color=colors[i % len(colors)],
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10),
                rotation=90,
                direction='clockwise'
            )
        ),
        showlegend=True,
        title={
            'text': f"Comparison: {', '.join(selected_cities)}",
            'x': 0.5,
            'font': {'color': '#1B4332', 'size': 16}
        },
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_default_dimension_spider(df_normalized):
    """Show spider plot by sustainability dimension"""
    
    st.markdown('<h2 class="subsection-title">📊 By Sustainability Dimension</h2>', unsafe_allow_html=True)
    
    dimension = st.selectbox(
        "Select dimension:",
        ["Environmental", "Social", "Economic"]
    )
    
    # Define indicators by dimension
    dimension_indicators = {
        "Environmental": [col for col in df_normalized.columns if any(env in col.lower() for env in ['air', 'green', 'renewable', 'waste', 'water']) and col.endswith('_normalized')],
        "Social": [col for col in df_normalized.columns if any(soc in col.lower() for soc in ['education', 'health', 'safety', 'social', 'housing']) and col.endswith('_normalized')],
        "Economic": [col for col in df_normalized.columns if any(econ in col.lower() for econ in ['gdp', 'unemployment', 'innovation', 'business', 'income']) and col.endswith('_normalized')]
    }
    
    indicators = dimension_indicators.get(dimension, [])
    
    if len(indicators) < 2:
        st.warning(f"⚠️ Not enough {dimension.lower()} indicators available.")
        return
    
    # Create spider plot
    fig = go.Figure()
    colors = px.colors.qualitative.Set2
    
    for i, (idx, row) in enumerate(df_normalized.iterrows()):
        values = [row[ind] for ind in indicators]
        labels = [ind.replace('_normalized', '').replace('_', ' ') for ind in indicators]
        
        # Close the polygon
        values.append(values[0])
        labels.append(labels[0])
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=row['City'],
            line_color=colors[i % len(colors)],
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title=f"{dimension} Indicators Comparison",
        title_font_color='#1B4332',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_default_individual_spider(df_normalized):
    """Show individual city spider plot"""
    
    st.markdown('<h2 class="subsection-title">🎯 Individual City Analysis</h2>', unsafe_allow_html=True)
    
    # City selection
    selected_city = st.selectbox("Select city to analyze:", df_normalized['City'].tolist())
    
    if not selected_city:
        return
    
    city_data = df_normalized[df_normalized['City'] == selected_city].iloc[0]
    
    # Get all normalized indicators
    indicators = [col for col in df_normalized.columns if col.endswith('_normalized')]
    
    if len(indicators) < 3:
        st.warning("⚠️ Not enough indicators available.")
        return
    
    # Create spider plot
    values = [city_data[ind] for ind in indicators]
    labels = [ind.replace('_normalized', '').replace('_', ' ') for ind in indicators]
    
    # Close the polygon
    values.append(values[0])
    labels.append(labels[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name=selected_city,
        line_color='#2D5A3D',
        fillcolor='rgba(45, 90, 61, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title=f"Sustainability Profile: {selected_city}",
        title_font_color='#1B4332',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
