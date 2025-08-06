import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from data import get_city_data

def show_spider_plot_section():
    """Display interactive spider plots for sustainability assessment"""
    
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
    
    st.markdown('<h1 class="section-title">🕸️ Spider Plot Analysis</h1>', unsafe_allow_html=True)
    
    # Get data from session state
    if 'city_data' not in st.session_state or not st.session_state.city_data:
        st.warning("⚠️ No data available. Please add city data first in the Data section above.")
        return
    
    df = pd.DataFrame(st.session_state.city_data)
    
    # Normalize data for spider plots
    df_normalized = normalize_data_for_spider(df)
    
    # Plot type selection
    plot_type = st.selectbox(
        "Select Spider Plot Type:",
        ["Individual City Analysis", "Multi-City Comparison", "Category-Specific Analysis", "Interactive Spider Plot"]
    )
    
    if plot_type == "Individual City Analysis":
        show_individual_spider_plot(df_normalized)
    elif plot_type == "Multi-City Comparison":
        show_multi_city_spider_plot(df_normalized)
    elif plot_type == "Category-Specific Analysis":
        show_category_spider_plot(df_normalized)
    else:
        show_interactive_spider_plot(df_normalized)

def normalize_data_for_spider(df):
    """Normalize data to 0-100 scale for spider plots"""
    df = df.copy()
    
    # Define metrics and their normalization
    metrics_config = {
        # Environmental metrics (higher is better)
        'Air_Quality': {'scale': 100, 'invert': False},
        'Green_Space': {'scale': 100, 'invert': False},
        'Renewable_Energy': {'scale': 100, 'invert': False},
        
        # Social metrics
        'Education_Index': {'scale': 1, 'invert': False},  # Convert to 0-100
        'Healthcare_Access': {'scale': 100, 'invert': False},
        'Safety_Index': {'scale': 10, 'invert': False},  # Convert to 0-100
        
        # Economic metrics
        'GDP_per_Capita': {'scale': None, 'invert': False},  # Normalize to max
        'Unemployment_Rate': {'scale': 100, 'invert': True},  # Invert (lower is better)
        'Innovation_Index': {'scale': 100, 'invert': False}
    }
    
    # Normalize each metric
    for metric, config in metrics_config.items():
        if config['scale'] is None:
            # Normalize to 0-100 based on min-max
            min_val = df[metric].min()
            max_val = df[metric].max()
            df[f"{metric}_normalized"] = ((df[metric] - min_val) / (max_val - min_val)) * 100
        else:
            # Direct scaling
            if config['invert']:
                df[f"{metric}_normalized"] = 100 - (df[metric] / config['scale'] * 100)
            else:
                df[f"{metric}_normalized"] = (df[metric] / config['scale']) * 100
    
    # Ensure Education_Index and Safety_Index are properly scaled
    df['Education_Index_normalized'] = df['Education_Index'] * 100
    df['Safety_Index_normalized'] = (df['Safety_Index'] / 10) * 100
    
    return df

def show_individual_spider_plot(df):
    """Show spider plot for individual city analysis"""
    st.markdown('<h2 class="subsection-title">🎯 Individual City Analysis</h2>', unsafe_allow_html=True)
    
    # City selection
    selected_city = st.selectbox("Select a city to analyze:", df['City'].tolist())
    
    if selected_city:
        city_data = df[df['City'] == selected_city].iloc[0]
        
        # Create comprehensive spider plot
        categories = [
            'Air Quality', 'Green Space', 'Renewable Energy',
            'Education', 'Healthcare', 'Safety',
            'GDP per Capita', 'Employment', 'Innovation'
        ]
        
        values = [
            city_data['Air_Quality_normalized'],
            city_data['Green_Space_normalized'],
            city_data['Renewable_Energy_normalized'],
            city_data['Education_Index_normalized'],
            city_data['Healthcare_Access_normalized'],
            city_data['Safety_Index_normalized'],
            city_data['GDP_per_Capita_normalized'],
            city_data['Unemployment_Rate_normalized'],
            city_data['Innovation_Index_normalized']
        ]
        
        # Create spider plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_city,
            line_color='#2D5A3D',
            fillcolor='rgba(45, 90, 61, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    gridcolor='lightgray'
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            showlegend=True,
            title=f"Sustainability Profile: {selected_city}",
            title_font=dict(size=20, color='#1B4332'),
            font=dict(color='#2D5A3D')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed metrics
        st.markdown('<h3 class="metric-category">📊 Detailed Metrics</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🌱 Environmental**")
            st.metric("Air Quality", f"{city_data['Air_Quality']}/100")
            st.metric("Green Space", f"{city_data['Green_Space']}%")
            st.metric("Renewable Energy", f"{city_data['Renewable_Energy']}%")
        
        with col2:
            st.markdown("**👥 Social**")
            st.metric("Education Index", f"{city_data['Education_Index']:.2f}")
            st.metric("Healthcare Access", f"{city_data['Healthcare_Access']}%")
            st.metric("Safety Index", f"{city_data['Safety_Index']:.1f}/10")
        
        with col3:
            st.markdown("**💰 Economic**")
            st.metric("GDP per Capita", f"${city_data['GDP_per_Capita']:,.0f}")
            st.metric("Unemployment Rate", f"{city_data['Unemployment_Rate']}%")
            st.metric("Innovation Index", f"{city_data['Innovation_Index']}/100")

def show_multi_city_spider_plot(df):
    """Show spider plot comparing multiple cities"""
    st.markdown('<h2 class="subsection-title">🏙️ Multi-City Comparison</h2>', unsafe_allow_html=True)
    
    # City selection
    selected_cities = st.multiselect(
        "Select cities to compare (max 5):",
        df['City'].tolist(),
        default=df['City'].tolist()[:3] if len(df) >= 3 else df['City'].tolist()
    )
    
    if len(selected_cities) > 5:
        st.warning("Please select maximum 5 cities for better visualization.")
        selected_cities = selected_cities[:5]
    
    if selected_cities:
        # Create spider plot
        categories = [
            'Air Quality', 'Green Space', 'Renewable Energy',
            'Education', 'Healthcare', 'Safety',
            'GDP per Capita', 'Employment', 'Innovation'
        ]
        
        fig = go.Figure()
        
        colors = ['#1B4332', '#2D5A3D', '#40736A', '#52A379', '#6BB58A']
        
        for i, city in enumerate(selected_cities):
            city_data = df[df['City'] == city].iloc[0]
            
            values = [
                city_data['Air_Quality_normalized'],
                city_data['Green_Space_normalized'],
                city_data['Renewable_Energy_normalized'],
                city_data['Education_Index_normalized'],
                city_data['Healthcare_Access_normalized'],
                city_data['Safety_Index_normalized'],
                city_data['GDP_per_Capita_normalized'],
                city_data['Unemployment_Rate_normalized'],
                city_data['Innovation_Index_normalized']
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=city,
                line_color=colors[i % len(colors)],
                fillcolor=f'rgba{tuple(list(bytes.fromhex(colors[i % len(colors)][1:])) + [0.2])}',
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            title="Multi-City Sustainability Comparison",
            title_font=dict(size=20, color='#1B4332')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show comparison summary
        show_comparison_summary(df, selected_cities)

def show_category_spider_plot(df):
    """Show spider plots by sustainability categories"""
    st.markdown('<h2 class="subsection-title">📂 Category-Specific Analysis</h2>', unsafe_allow_html=True)
    
    category = st.selectbox(
        "Select category to analyze:",
        ["Environmental", "Social", "Economic"]
    )
    
    if category == "Environmental":
        show_environmental_spider(df)
    elif category == "Social":
        show_social_spider(df)
    else:
        show_economic_spider(df)

def show_environmental_spider(df):
    """Show environmental-focused spider plot"""
    st.markdown('<h3 class="metric-category">🌱 Environmental Performance</h3>', unsafe_allow_html=True)
    
    categories = ['Air Quality', 'Green Space', 'Renewable Energy']
    
    fig = go.Figure()
    
    for idx, row in df.iterrows():
        values = [
            row['Air_Quality_normalized'],
            row['Green_Space_normalized'],
            row['Renewable_Energy_normalized']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row['City'],
            opacity=0.6
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Environmental Performance Comparison",
        title_font=dict(color='#1B4332')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_social_spider(df):
    """Show social-focused spider plot"""
    st.markdown('<h3 class="metric-category">👥 Social Performance</h3>', unsafe_allow_html=True)
    
    categories = ['Education', 'Healthcare', 'Safety']
    
    fig = go.Figure()
    
    for idx, row in df.iterrows():
        values = [
            row['Education_Index_normalized'],
            row['Healthcare_Access_normalized'],
            row['Safety_Index_normalized']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row['City'],
            opacity=0.6
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Social Performance Comparison",
        title_font=dict(color='#1B4332')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_economic_spider(df):
    """Show economic-focused spider plot"""
    st.markdown('<h3 class="metric-category">💰 Economic Performance</h3>', unsafe_allow_html=True)
    
    categories = ['GDP per Capita', 'Employment Rate', 'Innovation']
    
    fig = go.Figure()
    
    for idx, row in df.iterrows():
        values = [
            row['GDP_per_Capita_normalized'],
            row['Unemployment_Rate_normalized'],
            row['Innovation_Index_normalized']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=row['City'],
            opacity=0.6
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Economic Performance Comparison",
        title_font=dict(color='#1B4332')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_interactive_spider_plot(df):
    """Show interactive spider plot with customizable options"""
    st.markdown('<h2 class="subsection-title">🎮 Interactive Spider Plot</h2>', unsafe_allow_html=True)
    
    # Customization options
    col1, col2 = st.columns(2)
    
    with col1:
        selected_cities = st.multiselect(
            "Select cities:",
            df['City'].tolist(),
            default=[df['City'].tolist()[0]] if len(df) > 0 else []
        )
        
        fill_area = st.checkbox("Fill area", value=True)
        show_grid = st.checkbox("Show grid", value=True)
    
    with col2:
        opacity = st.slider("Opacity", 0.1, 1.0, 0.6, 0.1)
        color_theme = st.selectbox("Color theme", ["Greens", "Blues", "Reds", "Custom"])
    
    # Metric selection
    st.markdown('<h3 class="metric-category">🎯 Select Metrics to Display</h3>', unsafe_allow_html=True)
    
    metric_options = {
        'Air Quality': 'Air_Quality_normalized',
        'Green Space': 'Green_Space_normalized',
        'Renewable Energy': 'Renewable_Energy_normalized',
        'Education': 'Education_Index_normalized',
        'Healthcare': 'Healthcare_Access_normalized',
        'Safety': 'Safety_Index_normalized',
        'GDP per Capita': 'GDP_per_Capita_normalized',
        'Employment': 'Unemployment_Rate_normalized',
        'Innovation': 'Innovation_Index_normalized'
    }
    
    selected_metrics = st.multiselect(
        "Choose metrics:",
        list(metric_options.keys()),
        default=list(metric_options.keys())
    )
    
    if selected_cities and selected_metrics:
        # Create interactive spider plot
        fig = go.Figure()
        
        for i, city in enumerate(selected_cities):
            city_data = df[df['City'] == city].iloc[0]
            
            values = [city_data[metric_options[metric]] for metric in selected_metrics]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=selected_metrics,
                fill='toself' if fill_area else 'none',
                name=city,
                opacity=opacity,
                hovertemplate=f"<b>{city}</b><br>" +
                            "%{theta}: %{r:.1f}<br>" +
                            "<extra></extra>"
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showgrid=show_grid,
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    showgrid=show_grid
                )
            ),
            showlegend=True,
            title="Interactive Sustainability Analysis",
            title_font=dict(size=20, color='#1B4332'),
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select at least one city and one metric to display the spider plot.")

def show_comparison_summary(df, selected_cities):
    """Show summary comparison of selected cities"""
    st.markdown('<h3 class="metric-category">📋 Comparison Summary</h3>', unsafe_allow_html=True)
    
    comparison_df = df[df['City'].isin(selected_cities)]
    
    # Calculate category averages
    env_metrics = ['Air_Quality_normalized', 'Green_Space_normalized', 'Renewable_Energy_normalized']
    social_metrics = ['Education_Index_normalized', 'Healthcare_Access_normalized', 'Safety_Index_normalized']
    economic_metrics = ['GDP_per_Capita_normalized', 'Unemployment_Rate_normalized', 'Innovation_Index_normalized']
    
    comparison_summary = pd.DataFrame({
        'City': comparison_df['City'],
        'Environmental_Avg': comparison_df[env_metrics].mean(axis=1),
        'Social_Avg': comparison_df[social_metrics].mean(axis=1),
        'Economic_Avg': comparison_df[economic_metrics].mean(axis=1)
    })
    
    comparison_summary['Overall_Avg'] = comparison_summary[['Environmental_Avg', 'Social_Avg', 'Economic_Avg']].mean(axis=1)
    comparison_summary = comparison_summary.round(1)
    
    st.dataframe(comparison_summary, use_container_width=True)
