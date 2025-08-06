"""
Influence Matrix Module
This module handles the creation of influence matrices between indicators
and generates activity-passivity plots for structural analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime
from custom_indicators import load_custom_indicators_data, get_common_indicators

def show_influence_matrix_section():
    """Display the influence matrix interface and analysis"""
    
    st.markdown("""
    <style>
    .influence-title {
        color: #1B4332;
        font-size: 2.0rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .influence-subtitle {
        color: #2D5A3D;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    .matrix-info {
        background-color: #E8F5E8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #40736A;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="influence-title">🔗 Indicator Influence Matrix</h1>', unsafe_allow_html=True)
    
    # Check if we have indicators to work with
    common_indicators = get_common_indicators()
    
    if len(common_indicators) < 2:
        st.warning("⚠️ You need at least 2 common indicators across all cities to create an influence matrix.")
        st.info("Complete your indicator data entry first, ensuring that at least 2 indicators exist for all 4 cities.")
        return
    
    # Information about influence matrix (without expander since we're already in one)
    st.markdown("""
    **Influence Matrix Analysis** is a structural analysis method that helps understand:
    
    - **Direct influences** between different sustainability indicators
    - **Activity vs Passivity** of each indicator in the system
    - **System dynamics** and key leverage points
    
    **How to use:**
    1. For each pair of indicators, rate the influence from -2 to +2:
       - **-2**: Strong negative influence
       - **-1**: Weak negative influence  
       - **0**: No influence
       - **+1**: Weak positive influence
       - **+2**: Strong positive influence
    
    2. The system will generate an **Activity-Passivity Plot** showing:
       - **Indifferent indicators**: Low activity and passivity (lower-left)
       - **Passive indicators**: High passivity, low activity (lower-right)
       - **Active indicators**: High activity, low passivity (upper-left)
       - **Ambivalent indicators**: High activity and passivity (upper-right)
    """)
    
    st.markdown('<div class="matrix-info">📊 <strong>Available Indicators:</strong> ' + ', '.join(common_indicators) + '</div>', unsafe_allow_html=True)
    
    # Load existing matrix if available
    existing_matrix = load_influence_matrix()
    
    # Matrix entry interface
    st.markdown('<h2 class="influence-subtitle">📝 Define Influence Relationships</h2>', unsafe_allow_html=True)
    
    # Create influence matrix input
    matrix_data = create_influence_matrix_input(common_indicators, existing_matrix)
    
    # Save and analyze button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Save Matrix", type="primary"):
            save_influence_matrix(matrix_data, common_indicators)
            st.success("✅ Influence matrix saved!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Clear Matrix", type="secondary"):
            clear_influence_matrix()
            st.success("✅ Matrix cleared!")
            st.rerun()
    
    with col3:
        if matrix_data is not None and not np.all(matrix_data == 0):
            if st.button("📊 Generate Analysis", type="primary"):
                st.session_state.show_influence_analysis = True
                st.rerun()
    
    # Show analysis if matrix is complete
    if matrix_data is not None and not np.all(matrix_data == 0):
        if st.session_state.get('show_influence_analysis', False):
            st.markdown("---")
            show_influence_analysis(matrix_data, common_indicators)

def create_influence_matrix_input(indicators, existing_matrix=None):
    """Create the influence matrix input interface"""
    
    n_indicators = len(indicators)
    
    # Initialize matrix
    if existing_matrix is not None:
        matrix = existing_matrix.copy()
    else:
        matrix = np.zeros((n_indicators, n_indicators))
    
    st.markdown("**Rate the influence of each indicator (rows) on others (columns):**")
    st.markdown("*Scale: -2 (strong negative) to +2 (strong positive)*")
    
    # Create input grid
    cols = st.columns(n_indicators + 1)
    
    # Header row
    with cols[0]:
        st.markdown("**From → To**")
    
    for j, indicator_to in enumerate(indicators):
        with cols[j + 1]:
            st.markdown(f"**{indicator_to[:15]}...**" if len(indicator_to) > 15 else f"**{indicator_to}**")
    
    # Matrix input rows
    for i, indicator_from in enumerate(indicators):
        cols = st.columns(n_indicators + 1)
        
        with cols[0]:
            st.markdown(f"**{indicator_from[:15]}...**" if len(indicator_from) > 15 else f"**{indicator_from}**")
        
        for j, indicator_to in enumerate(indicators):
            with cols[j + 1]:
                if i == j:
                    # Diagonal - no self-influence
                    st.markdown("—")
                    matrix[i, j] = 0
                else:
                    # Get influence value
                    key = f"influence_{i}_{j}"
                    value = st.selectbox(
                        "",
                        options=[-2, -1, 0, 1, 2],
                        index=int(matrix[i, j]) + 2,  # Convert -2..2 to 0..4 index
                        key=key,
                        label_visibility="collapsed"
                    )
                    matrix[i, j] = value
    
    return matrix

def save_influence_matrix(matrix, indicators):
    """Save influence matrix to CSV file"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Create DataFrame
    df = pd.DataFrame(matrix, index=indicators, columns=indicators)
    
    # Add metadata
    df.to_csv(f"{data_dir}/influence_matrix.csv")
    
    # Save metadata
    metadata = {
        'indicators': indicators,
        'creation_date': datetime.now().isoformat(),
        'matrix_size': len(indicators)
    }
    
    import json
    with open(f"{data_dir}/influence_matrix_metadata.json", 'w') as f:
        json.dump(metadata, f)

def load_influence_matrix():
    """Load influence matrix from CSV file"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    matrix_path = f"{data_dir}/influence_matrix.csv"
    
    try:
        df = pd.read_csv(matrix_path, index_col=0)
        return df.values
    except FileNotFoundError:
        return None

def clear_influence_matrix():
    """Clear influence matrix files"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    
    files_to_remove = [
        f"{data_dir}/influence_matrix.csv",
        f"{data_dir}/influence_matrix_metadata.json"
    ]
    
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
    
    # Clear session state
    if 'show_influence_analysis' in st.session_state:
        del st.session_state['show_influence_analysis']

def show_influence_analysis(matrix, indicators):
    """Show the analysis results including activity-passivity plot"""
    
    st.markdown('<h2 class="influence-subtitle">📈 Structural Analysis Results</h2>', unsafe_allow_html=True)
    
    # Calculate activity and passivity scores
    activity_scores = np.sum(np.abs(matrix), axis=1)  # Sum of absolute influences FROM each indicator
    passivity_scores = np.sum(np.abs(matrix), axis=0)  # Sum of absolute influences TO each indicator
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'Indicator': indicators,
        'Activity': activity_scores,
        'Passivity': passivity_scores,
        'Total_Influence': activity_scores + passivity_scores
    })
    
    # Sort by total influence
    results_df = results_df.sort_values('Total_Influence', ascending=False)
    
    # Display matrix
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**🔢 Influence Matrix**")
        matrix_df = pd.DataFrame(matrix, index=indicators, columns=indicators)
        
        # Style the matrix
        styled_matrix = matrix_df.style.applymap(lambda x: 
            'background-color: #ffcccc' if x < 0 else 
            'background-color: #ccffcc' if x > 0 else 
            'background-color: #f0f0f0'
        ).format('{:.0f}')
        
        st.dataframe(styled_matrix)
        
        # Matrix legend
        st.markdown("""
        **Legend:**
        - 🟢 Positive influence (+1, +2)
        - 🔴 Negative influence (-1, -2)  
        - ⚪ No influence (0)
        """)
    
    with col2:
        st.markdown("**📊 Activity-Passivity Scores**")
        st.dataframe(results_df.round(2))
        
        # Interpretation
        st.markdown("**Interpretation:**")
        st.markdown("- **Activity**: How much this indicator influences others")
        st.markdown("- **Passivity**: How much this indicator is influenced by others")
        st.markdown("- **Total**: Overall importance in the system")
    
    # Activity-Passivity Plot
    st.markdown('<h3 class="influence-subtitle">🎯 Activity-Passivity Plot</h3>', unsafe_allow_html=True)
    
    # Create interactive plot with Plotly
    fig = create_activity_passivity_plot(results_df)
    st.plotly_chart(fig, use_container_width=True)
    
    # Quadrant analysis
    show_quadrant_analysis(results_df)
    
    # Export options
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export matrix
        matrix_csv = matrix_df.to_csv()
        st.download_button(
            label="📥 Download Matrix",
            data=matrix_csv,
            file_name=f"influence_matrix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export results
        results_csv = results_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Results",
            data=results_csv,
            file_name=f"activity_passivity_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col3:
        # Export plot as PNG
        if st.button("🖼️ Download Plot as PNG"):
            try:
                # Generate filename
                filename = f"activity_passivity_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                
                # Save plot as PNG bytes
                img_bytes = fig.to_image(format="png", width=800, height=600)
                
                # Provide download button for the PNG file
                st.download_button(
                    label="📥 Download PNG File",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/png"
                )
                st.success("PNG file ready for download!")
                
            except Exception as e:
                st.error(f"Error creating PNG: {str(e)}")
                st.info("💡 Note: PNG export requires 'kaleido' package. Install with: pip install kaleido")

def create_activity_passivity_plot(results_df):
    """Create the activity-passivity plot using Plotly"""
    
    # Calculate quadrant boundaries (median values)
    median_activity = results_df['Activity'].median()
    median_passivity = results_df['Passivity'].median()
    
    # Create scatter plot
    fig = go.Figure()
    
    # Add points (swap x and y axes: passivity on x-axis, activity on y-axis)
    fig.add_trace(go.Scatter(
        x=results_df['Passivity'],
        y=results_df['Activity'],
        mode='markers+text',
        text=results_df['Indicator'],
        textposition="top center",
        marker=dict(
            size=12,
            color=results_df['Total_Influence'],
            colorscale='Viridis',
            colorbar=dict(title="Total Influence"),
            line=dict(width=2, color='white')
        ),
        name="Indicators"
    ))
    
    # Add quadrant lines
    max_activity = results_df['Activity'].max() * 1.1
    max_passivity = results_df['Passivity'].max() * 1.1
    
    fig.add_hline(y=median_activity, line_dash="dash", line_color="gray", annotation_text="Median Activity")
    fig.add_vline(x=median_passivity, line_dash="dash", line_color="gray", annotation_text="Median Passivity")
    
    # Add quadrant labels (updated for new axis configuration)
    fig.add_annotation(x=max_passivity * 0.8, y=max_activity * 0.8, text="Ambivalent<br>(High Passivity & Activity)", 
                      showarrow=False, bgcolor="rgba(255,255,0,0.3)", bordercolor="orange")
    fig.add_annotation(x=max_passivity * 0.8, y=max_activity * 0.2, text="Passive<br>(High Passivity, Low Activity)", 
                      showarrow=False, bgcolor="rgba(255,0,0,0.3)", bordercolor="red")
    fig.add_annotation(x=max_passivity * 0.2, y=max_activity * 0.8, text="Active<br>(Low Passivity, High Activity)", 
                      showarrow=False, bgcolor="rgba(0,255,0,0.3)", bordercolor="green")
    fig.add_annotation(x=max_passivity * 0.2, y=max_activity * 0.2, text="Indifferent<br>(Low Passivity & Activity)", 
                      showarrow=False, bgcolor="rgba(0,0,255,0.3)", bordercolor="blue")
    
    # Update layout
    fig.update_layout(
        title="Activity-Passivity Plot of Sustainability Indicators",
        xaxis_title="Passivity (Influenced by Others)",
        yaxis_title="Activity (Influence on Others)",
        width=800,
        height=600,
        showlegend=False,
        template="plotly_white"
    )
    
    return fig

def show_quadrant_analysis(results_df):
    """Show analysis of indicators by quadrant"""
    
    median_activity = results_df['Activity'].median()
    median_passivity = results_df['Passivity'].median()
    
    # Classify indicators (updated for new axis configuration)
    quadrants = {
        'Ambivalent (High Passivity & Activity)': results_df[
            (results_df['Passivity'] > median_passivity) & 
            (results_df['Activity'] > median_activity)
        ],
        'Active (Low Passivity, High Activity)': results_df[
            (results_df['Passivity'] <= median_passivity) & 
            (results_df['Activity'] > median_activity)
        ],
        'Passive (High Passivity, Low Activity)': results_df[
            (results_df['Passivity'] > median_passivity) & 
            (results_df['Activity'] <= median_activity)
        ],
        'Indifferent (Low Passivity & Activity)': results_df[
            (results_df['Passivity'] <= median_passivity) & 
            (results_df['Activity'] <= median_activity)
        ]
    }
    
    st.markdown("**🎯 Quadrant Analysis:**")
    
    for quadrant_name, quadrant_data in quadrants.items():
        if not quadrant_data.empty:
            st.markdown(f"**{quadrant_name}** ({len(quadrant_data)} indicators)")
            for _, indicator in quadrant_data.iterrows():
                st.write(f"• **{indicator['Indicator']}** - Activity: {indicator['Activity']:.1f}, Passivity: {indicator['Passivity']:.1f}")
            
            # Interpretation (updated for new quadrant names)
            if 'Ambivalent' in quadrant_name:
                st.info("💡 **Strategy**: These are leverage points - focus on these indicators for maximum system impact!")
            elif 'Active' in quadrant_name:
                st.success("🎯 **Strategy**: These drive the system - monitor and optimize these indicators.")
            elif 'Passive' in quadrant_name:
                st.warning("📊 **Strategy**: These are outcomes - they reflect system performance.")
            else:
                st.info("🔄 **Strategy**: These are relatively independent - monitor for unexpected changes.")
            
            st.markdown("---")
