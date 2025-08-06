import streamlit as st
import datetime
import locale
import pytz
import pandas as pd
import numpy as np

# Import all modules
from intro import show_intro
from data import show_data_section
from flexible_analysis import show_analysis_section
from flexible_spider_plot import show_spider_plot_section
from flexible_ranking import show_ranking_section
from data_collector import show_initial_setup, show_data_entry, load_collected_data
from custom_indicators import show_custom_indicator_setup, convert_custom_indicators_for_analysis, get_indicators_summary, export_custom_indicators_data
from influence_matrix import show_influence_matrix_section

def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title="City Sustainability Assessment",
        page_icon="🌿",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for dark green theme
    st.markdown("""
    <style>
    /* Main theme colors */
    .stApp {
        background-color: #F8FDF8;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #E8F5E8;
    }
    
    /* Headers */
    .main-header {
        color: #1B4332;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #E8F5E8 0%, #D4E7D4 100%);
        border-radius: 10px;
        border-left: 5px solid #1B4332;
    }
    
    /* Sidebar navigation */
    .sidebar-nav {
        color: #2D5A3D;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Metrics and info boxes */
    .stMetric {
        background-color: #F0F8F0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #40736A;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #2D5A3D;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .stButton button:hover {
        background-color: #1B4332;
        color: white;
    }
    
    /* Success/Info messages */
    .stSuccess {
        background-color: #D4F1D4;
        border-left: 4px solid #2D5A3D;
    }
    
    .stInfo {
        background-color: #E8F5E8;
        border-left: 4px solid #40736A;
    }
    
    /* Tables */
    .stDataFrame {
        border: 1px solid #D4E7D4;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown(
        '<h1 class="main-header">🌿 City Sustainability Assessment</h1>',
        unsafe_allow_html=True
    )
    
    # Initialize session state for tracking progress
    if 'setup_complete' not in st.session_state:
        st.session_state.setup_complete = False
    if 'data_collection_complete' not in st.session_state:
        st.session_state.data_collection_complete = False
    if 'data_entered' not in st.session_state:
        st.session_state.data_entered = False
    if 'use_custom_indicators' not in st.session_state:
        st.session_state.use_custom_indicators = False
    
    # Load any existing collected data
    existing_data = load_collected_data()
    custom_indicators_data = convert_custom_indicators_for_analysis()
    
    # Check which data source to use
    if not custom_indicators_data.empty:
        st.session_state.data_entered = True
        st.session_state.data_collection_complete = True
        st.session_state.use_custom_indicators = True
        st.session_state.city_data = custom_indicators_data.to_dict('records')
    elif not existing_data.empty:
        st.session_state.data_entered = True
        st.session_state.data_collection_complete = True
        st.session_state.use_custom_indicators = False
    
    # Workflow Steps - All visible on same page
    
    # Step 1: Initial Setup (Research Question + City Selection)
    show_intro()
    st.markdown("---")
    
    setup_complete = show_initial_setup()
    
    # Step 2: Choose Data Entry Method (show if setup is complete)
    if setup_complete or st.session_state.get('setup_complete', False):
        st.markdown("---")
        st.markdown('<h2 style="color: #1B4332;">📊 Choose Your Data Entry Method</h2>', unsafe_allow_html=True)
        
        # Check if user has existing data
        existing_custom = convert_custom_indicators_for_analysis()
        existing_default = load_collected_data()
        
        if not existing_custom.empty or not existing_default.empty:
            # Show current data status
            col1, col2 = st.columns(2)
            
            with col1:
                if not existing_custom.empty:
                    summary = get_indicators_summary()
                    st.success(f"✅ **Custom Indicators Data Found**\n- {summary['total_indicators']} indicators\n- {summary['unique_cities']} cities")
                else:
                    st.info("⏳ No custom indicators data")
            
            with col2:
                if not existing_default.empty:
                    st.success(f"✅ **Default Template Data Found**\n- {len(existing_default)} cities\n- Standard indicators")
                else:
                    st.info("⏳ No default template data")
            
            # Option to continue with existing or start fresh
            data_choice = st.radio(
                "How would you like to proceed?",
                [
                    "Continue with Custom Indicators" if not existing_custom.empty else None,
                    "Continue with Default Template" if not existing_default.empty else None,
                    "Start Fresh with Custom Indicators",
                    "Start Fresh with Default Template",
                    "Start Completely Over"
                ],
                index=0 if not existing_custom.empty else (1 if not existing_default.empty else 2)
            )
            
            if data_choice == "Start Completely Over":
                if st.button("🔄 Clear All Data and Restart"):
                    # Clear all session state and files
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
            
            elif data_choice == "Start Fresh with Custom Indicators":
                show_custom_indicator_setup()
            
            elif data_choice == "Start Fresh with Default Template":
                show_data_entry()
            
            elif data_choice == "Continue with Custom Indicators":
                show_custom_indicator_setup()
            
            elif data_choice == "Continue with Default Template":
                show_data_entry()
                
        else:
            # No existing data - show choice
            data_entry_method = st.radio(
                "Choose your data entry approach:",
                [
                    "🎯 **Custom Indicators** - Define your own indicators (Recommended for research)",
                    "📋 **Default Template** - Use predefined sustainability indicators (Quick start)"
                ],
                help="Custom indicators give you full control over what you measure. Default template provides standard sustainability metrics."
            )
            
            if "Custom Indicators" in data_entry_method:
                show_custom_indicator_setup()
            else:
                show_data_entry()
    
    # Step 3: Analysis Phase (show if we have data)
    if st.session_state.get('city_data') and len(st.session_state.city_data) > 0:
        # Load and display the collected data
        st.markdown("---")
        st.markdown('<h2 style="color: #1B4332;">📊 Your Collected Data</h2>', unsafe_allow_html=True)
        
        # Choose data source to display
        if st.session_state.get('use_custom_indicators', False):
            # Display custom indicators data
            custom_data = convert_custom_indicators_for_analysis()
            indicators_summary = get_indicators_summary()
            
            if not custom_data.empty:
                # Show research context
                try:
                    metadata_path = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data/research_metadata.csv"
                    metadata_df = pd.read_csv(metadata_path)
                    if not metadata_df.empty:
                        with st.expander("🎯 Your Research Context", expanded=False):
                            st.write(f"**Research Question:** {metadata_df['Research_Question'].iloc[0]}")
                            st.write(f"**Cities:** {metadata_df['City_1'].iloc[0]} | {metadata_df['City_2'].iloc[0]} | {metadata_df['City_3'].iloc[0]} | {metadata_df['City_4'].iloc[0]}")
                            st.write("**Data Method:** Custom Indicators")
                except:
                    pass
                
                # Summary of custom indicators
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Cities", indicators_summary['unique_cities'])
                with col2:
                    st.metric("Total Indicators", indicators_summary['total_indicators'])
                with col3:
                    avg_indicators = indicators_summary['total_indicators'] / max(indicators_summary['unique_cities'], 1)
                    st.metric("Avg per City", f"{avg_indicators:.1f}")
                with col4:
                    st.metric("Categories", len(indicators_summary['categories']))
                
                # Show indicators by category
                if indicators_summary['categories']:
                    st.markdown("**📈 Indicators by Category:**")
                    category_cols = st.columns(len(indicators_summary['categories']))
                    for i, (category, count) in enumerate(indicators_summary['categories'].items()):
                        with category_cols[i]:
                            st.metric(category, count)
                
                # Data table with custom indicators
                indicators_data = indicators_summary['data']
                display_data = indicators_data[['City', 'Indicator_Name', 'Value', 'Unit', 'Category']].copy()
                st.dataframe(display_data, use_container_width=True)
                
                # Export options
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("🔄 Start New Research"):
                        # Clear all session state
                        for key in list(st.session_state.keys()):
                            del st.session_state[key]
                        st.rerun()
                with col2:
                    # Export custom indicators data
                    csv_data = export_custom_indicators_data()
                    if csv_data:
                        st.download_button(
                            label="📥 Download Indicators",
                            data=csv_data,
                            file_name=f"custom_indicators_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                with col3:
                    # Export analysis-ready data
                    analysis_csv = custom_data.to_csv(index=False)
                    st.download_button(
                        label="📊 Download Analysis Data",
                        data=analysis_csv,
                        file_name=f"analysis_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                # Check if analysis should be available
                from custom_indicators import check_analysis_readiness, get_common_indicators
                
                if check_analysis_readiness():
                    common_indicators = get_common_indicators()
                    
                    # Show analysis sections
                    st.markdown("---")
                    st.markdown('<h2 style="color: #1B4332;">📈 Analysis Dashboard</h2>', unsafe_allow_html=True)
                    
                    # Show common indicators info
                    if common_indicators:
                        st.success(f"✅ **Analysis Ready!** {len(common_indicators)} indicator(s) available for all cities: {', '.join(common_indicators)}")
                    else:
                        st.info("📊 **Partial Analysis Available** - All cities have data but no common indicators yet.")
                    
                    # Prepare session state for analysis
                    st.session_state.city_data = custom_data.to_dict('records')
                    
                    # Analysis sections in expandable containers
                    with st.expander("📊 **Comprehensive Analysis**", expanded=True):
                        show_analysis_section()
                    
                    with st.expander("🕸️ **Spider Plot Visualization**", expanded=False):
                        show_spider_plot_section()
                    
                    with st.expander("🏆 **City Rankings**", expanded=False):
                        show_ranking_section()
                    
                    with st.expander("🔗 **Influence Matrix & Activity-Passivity Analysis**", expanded=False):
                        show_influence_matrix_section()
                else:
                    st.info("📊 **Analysis will appear when you have at least one indicator for all 4 cities**")
        
        else:
            # Display default template data
            collected_df = load_collected_data()
            
            if not collected_df.empty:
                # Show research context
                try:
                    metadata_path = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data/research_metadata.csv"
                    metadata_df = pd.read_csv(metadata_path)
                    if not metadata_df.empty:
                        with st.expander("🎯 Your Research Context", expanded=False):
                            st.write(f"**Research Question:** {metadata_df['Research_Question'].iloc[0]}")
                            st.write(f"**Cities:** {metadata_df['City_1'].iloc[0]} | {metadata_df['City_2'].iloc[0]} | {metadata_df['City_3'].iloc[0]} | {metadata_df['City_4'].iloc[0]}")
                            st.write(f"**Data Method:** {metadata_df['Indicator_Approach'].iloc[0]}")
                except:
                    pass
                
                # Summary of collected data
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Cities Analyzed", len(collected_df))
                with col2:
                    st.metric("Countries", collected_df['Country'].nunique() if 'Country' in collected_df.columns else 0)
                with col3:
                    avg_pop = collected_df['Population'].mean() if 'Population' in collected_df.columns else 0
                    st.metric("Avg Population", f"{avg_pop:,.0f}")
                
                # Data table
                st.dataframe(collected_df, use_container_width=True)
                
                # Option to restart and export
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("🔄 Start New Research"):
                        # Clear all session state
                        for key in list(st.session_state.keys()):
                            del st.session_state[key]
                        st.rerun()
                with col2:
                    pass  # Empty column for spacing
                with col3:
                    # Export data button
                    csv = collected_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Data",
                        data=csv,
                        file_name=f"sustainability_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            # Now show the analysis sections
            st.markdown("---")
            st.markdown('<h2 style="color: #1B4332;">📈 Analysis Dashboard</h2>', unsafe_allow_html=True)
            
            # Analysis sections in expandable containers
            with st.expander("📊 **Comprehensive Analysis**", expanded=True):
                show_analysis_section()
            
            with st.expander("🕸️ **Spider Plot Visualization**", expanded=False):
                show_spider_plot_section()
            
            with st.expander("🏆 **City Rankings**", expanded=False):
                show_ranking_section()
    
    # Footer
    st.markdown("---")
    current_time = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    st.markdown(
        '<p style="text-align: center; color: #40736A; font-style: italic; font-size: 0.9rem;">'
        'Built with ❤️ for sustainable city development | '
        f'Last updated: {current_time.strftime("%Y-%m-%d %H:%M")} | '
        '💡 Imagined by <strong>Sven Hominal</strong></p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()