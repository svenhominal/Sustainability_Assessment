"""
Custom Indicators Module
This module handles flexible custom indicator entry where users can define their own
sustainability indicators with name, description, value, unit, and source for each city.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json

def show_custom_indicator_setup():
    """Display interface for setting up custom indicators for each city"""
    
    st.markdown("""
    <style>
    .custom-title {
        color: #1B4332;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .custom-subtitle {
        color: #2D5A3D;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    .indicator-card {
        background-color: #F0F8F0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #40736A;
        margin: 0.5rem 0;
    }
    .city-section {
        background-color: #E8F5E8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 2px solid #D4E7D4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="custom-title">🎯 Custom Indicators Data Entry</h1>', unsafe_allow_html=True)
    
    # Check if setup is complete
    if not st.session_state.get('setup_complete', False):
        st.warning("⚠️ Please complete the initial setup first (research question and city selection).")
        return False
    
    research_data = st.session_state.research_data
    
    # Show research context
    with st.expander("🎯 Your Research Context", expanded=False):
        st.write(f"**Research Question:** {research_data.get('research_question', '')}")
        cities = [
            f"{research_data.get('city1', '')}, {research_data.get('country1', '')}",
            f"{research_data.get('city2', '')}, {research_data.get('country2', '')}",
            f"{research_data.get('city3', '')}, {research_data.get('country3', '')}",
            f"{research_data.get('city4', '')}, {research_data.get('country4', '')}"
        ]
        st.write("**Cities:** " + " | ".join(cities))
    
    # CSV Upload/Load Section
    st.markdown('<h2 class="custom-subtitle">📂 Load Data (Optional)</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📤 Upload CSV File**")
        uploaded_file = st.file_uploader(
            "Upload your prepared indicator data",
            type="csv",
            help="Upload a CSV file with your indicator data to load existing entries"
        )
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_cols = ['City', 'Indicator_Name', 'Description', 'Value', 'Unit', 'Source']
                if all(col in uploaded_df.columns for col in required_cols):
                    
                    # Save to session state and CSV
                    save_custom_indicators_data(uploaded_df)
                    st.success(f"✅ Successfully loaded {len(uploaded_df)} indicator entries!")
                    
                    # Show preview
                    with st.expander("📊 Uploaded Data Preview", expanded=False):
                        st.dataframe(uploaded_df)
                    
                    st.rerun()
                else:
                    st.error(f"❌ CSV must contain columns: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"❌ Error reading CSV: {str(e)}")
    
    with col2:
        st.markdown("**📥 Download Template**")
        st.write("Download a template CSV to fill out offline:")
        
        template_data = {
            'City': ['Your City 1', 'Your City 1', 'Your City 2'],
            'Country': ['Country 1', 'Country 1', 'Country 2'],
            'Indicator_Name': ['Air Quality Index', 'Public Transport Coverage', 'Green Space per Capita'],
            'Description': [
                'Air quality measurement index',
                'Percentage of city covered by public transport',
                'Square meters of green space per resident'
            ],
            'Value': [75.5, 85.2, 25.8],
            'Unit': ['Index (0-100)', 'Percentage', 'sq m per person'],
            'Source': ['Environmental Agency 2024', 'Transport Department', 'City Planning Office'],
            'Category': ['Environmental', 'Social', 'Environmental'],
            'Data_Entry_Date': [datetime.now().isoformat()] * 3
        }
        
        template_df = pd.DataFrame(template_data)
        csv = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Template",
            data=csv,
            file_name="indicator_template.csv",
            mime="text/csv"
        )
    
    # Load existing data if available
    existing_data = load_custom_indicators_data()
    
    # City-by-city indicator entry
    st.markdown('<h2 class="custom-subtitle">🏙️ Enter Indicators by City</h2>', unsafe_allow_html=True)
    
    # Get city information
    city_info = []
    for i in range(1, 5):
        city = research_data.get(f'city{i}', '')
        country = research_data.get(f'country{i}', 'Not specified')
        city_info.append({'city': city, 'country': country})
    
    # Initialize session state for indicators
    if 'custom_indicators' not in st.session_state:
        st.session_state.custom_indicators = {}
    
    # Clear all data button (show only if there is data)
    if not existing_data.empty:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:  # Center the button
            if st.button("🗑️ Clear All Indicators", type="secondary", help="This will delete all entered indicators and clear the CSV file"):
                if st.session_state.get('confirm_clear_all', False):
                    clear_all_custom_indicators()
                    st.success("✅ All indicators have been cleared!")
                    st.session_state.confirm_clear_all = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear_all = True
                    st.warning("⚠️ Click again to confirm clearing all indicators. This action cannot be undone!")
    
    # Progress tracking
    show_custom_indicators_progress(city_info, existing_data)
    
    # City selection for data entry
    city_options = []
    for info in city_info:
        if info['country'] != "Not specified":
            city_options.append(f"{info['city']} ({info['country']})")
        else:
            city_options.append(info['city'])
    
    selected_city_display = st.selectbox("Select city to enter indicators for:", city_options)
    selected_city_index = city_options.index(selected_city_display)
    selected_city_info = city_info[selected_city_index]
    
    # Show indicator entry for selected city
    show_city_indicator_entry(selected_city_info, existing_data)
    
    return True

def show_city_indicator_entry(city_info, existing_data):
    """Show indicator entry interface for a specific city"""
    
    city_name = city_info['city']
    country_name = city_info['country']
    
    st.markdown(f'<div class="city-section"><h3>🏙️ {city_name}, {country_name}</h3></div>', unsafe_allow_html=True)
    
    # Get existing indicators for this city
    city_indicators = existing_data[existing_data['City'] == city_name] if not existing_data.empty else pd.DataFrame()
    
    # Show existing indicators
    if not city_indicators.empty:
        st.markdown("**📊 Current Indicators:**")
        for idx, indicator in city_indicators.iterrows():
            with st.expander(f"📈 {indicator['Indicator_Name']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {indicator['Description']}")
                    st.write(f"**Value:** {indicator['Value']} {indicator['Unit']}")
                with col2:
                    st.write(f"**Source:** {indicator['Source']}")
                    st.write(f"**Category:** {indicator.get('Category', 'Not specified')}")
                
                # Delete button
                if st.button(f"🗑️ Delete", key=f"delete_{idx}"):
                    delete_indicator(city_name, indicator['Indicator_Name'])
                    st.rerun()
    
    # Add new indicator form
    st.markdown("**➕ Add New Indicator:**")
    
    with st.form(f"add_indicator_{city_name}"):
        col1, col2 = st.columns(2)
        
        with col1:
            indicator_name = st.text_input(
                "Indicator Name*",
                placeholder="e.g., Air Quality Index",
                help="A clear, concise name for your indicator"
            )
            
            description = st.text_area(
                "Description*",
                placeholder="e.g., Measures air pollution levels using PM2.5 and NO2 concentrations",
                help="Detailed description of what this indicator measures"
            )
            
            category = st.selectbox(
                "Category",
                ["Environmental", "Social", "Economic", "Governance", "Cultural", "Other"],
                help="Choose the sustainability category this indicator belongs to"
            )
        
        with col2:
            value = st.number_input(
                "Value*",
                help="The numerical value for this indicator"
            )
            
            unit = st.text_input(
                "Unit*",
                placeholder="e.g., Index (0-100), %, kg/capita, etc.",
                help="The unit of measurement for this indicator"
            )
            
            source = st.text_input(
                "Source*",
                placeholder="e.g., WHO Global Urban Ambient Air Pollution Database 2024",
                help="Where this data comes from (organization, report, website, etc.)"
            )
        
        submitted = st.form_submit_button("➕ Add Indicator")
        
        if submitted:
            # Validation
            if not all([indicator_name.strip(), description.strip(), unit.strip(), source.strip()]):
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                # Check for duplicate indicator names for this city
                if not city_indicators.empty and indicator_name in city_indicators['Indicator_Name'].values:
                    st.error(f"❌ An indicator named '{indicator_name}' already exists for {city_name}. Please use a different name.")
                else:
                    # Add the indicator
                    new_indicator = {
                        'City': city_name,
                        'Country': country_name,
                        'Indicator_Name': indicator_name.strip(),
                        'Description': description.strip(),
                        'Value': value,
                        'Unit': unit.strip(),
                        'Source': source.strip(),
                        'Category': category,
                        'Data_Entry_Date': datetime.now().isoformat()
                    }
                    
                    add_custom_indicator(new_indicator)
                    st.success(f"✅ Added '{indicator_name}' for {city_name}!")
                    st.rerun()

def add_custom_indicator(indicator_data):
    """Add a custom indicator to the data store"""
    
    # Load existing data
    existing_data = load_custom_indicators_data()
    
    # Add new indicator
    new_df = pd.DataFrame([indicator_data])
    
    if existing_data.empty:
        updated_data = new_df
    else:
        updated_data = pd.concat([existing_data, new_df], ignore_index=True)
    
    # Save to CSV
    save_custom_indicators_data(updated_data)
    
    # Update session state for immediate analysis availability
    update_session_state_for_analysis()

def delete_indicator(city_name, indicator_name):
    """Delete a specific indicator for a city"""
    
    existing_data = load_custom_indicators_data()
    
    if not existing_data.empty:
        # Remove the specific indicator
        updated_data = existing_data[
            ~((existing_data['City'] == city_name) & (existing_data['Indicator_Name'] == indicator_name))
        ]
        
        save_custom_indicators_data(updated_data)
        
        # Update session state for analysis availability
        update_session_state_for_analysis()

def clear_all_custom_indicators():
    """Clear all custom indicators data from CSV file and session state"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    csv_path = f"{data_dir}/custom_indicators.csv"
    
    try:
        # Remove the CSV file if it exists
        if os.path.exists(csv_path):
            os.remove(csv_path)
        
        # Clear session state
        if 'custom_indicators_data' in st.session_state:
            del st.session_state['custom_indicators_data']
        
        if 'custom_indicators' in st.session_state:
            del st.session_state['custom_indicators']
            
        # Clear any confirmation state
        if 'confirm_clear_all' in st.session_state:
            del st.session_state['confirm_clear_all']
            
    except Exception as e:
        st.error(f"Error clearing data: {str(e)}")

def save_custom_indicators_data(df):
    """Save custom indicators data to CSV file"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    os.makedirs(data_dir, exist_ok=True)
    
    csv_path = f"{data_dir}/custom_indicators.csv"
    df.to_csv(csv_path, index=False)
    
    # Also update session state
    st.session_state.custom_indicators_data = df.to_dict('records')
    
    # Update analysis state
    update_session_state_for_analysis()

def load_custom_indicators_data():
    """Load custom indicators data from CSV file"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    csv_path = f"{data_dir}/custom_indicators.csv"
    
    try:
        df = pd.read_csv(csv_path)
        st.session_state.custom_indicators_data = df.to_dict('records')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def show_custom_indicators_progress(city_info, existing_data):
    """Show progress of custom indicators entry"""
    
    st.markdown('<h3 class="custom-subtitle">📈 Entry Progress</h3>', unsafe_allow_html=True)
    
    if existing_data.empty:
        st.info("No indicators entered yet. Start by selecting a city and adding your first indicator.")
        return
    
    # Count indicators per city
    target_cities = [info['city'] for info in city_info]
    city_counts = existing_data.groupby('City').size().to_dict() if not existing_data.empty else {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_indicators = len(existing_data)
        st.metric("Total Indicators", total_indicators)
    
    with col2:
        cities_with_data = len([city for city in target_cities if city_counts.get(city, 0) > 0])
        st.metric("Cities with Data", f"{cities_with_data}/4")
    
    with col3:
        avg_indicators = sum(city_counts.get(city, 0) for city in target_cities) / 4
        st.metric("Avg Indicators/City", f"{avg_indicators:.1f}")
    
    # Show city-by-city progress
    progress_cols = st.columns(4)
    for i, info in enumerate(city_info):
        city = info['city']
        count = city_counts.get(city, 0)
        
        with progress_cols[i]:
            if count > 0:
                st.success(f"✅ **{city}**\n{count} indicators")
            else:
                st.info(f"⏳ **{city}**\nNo data yet")
    
    # Show data preview
    if total_indicators > 0:
        with st.expander("📊 Current Data Overview", expanded=False):
            # Summary by category
            if 'Category' in existing_data.columns:
                category_counts = existing_data['Category'].value_counts()
                st.write("**By Category:**")
                for category, count in category_counts.items():
                    st.write(f"- {category}: {count} indicators")
            
            st.write("**All Indicators:**")
            st.dataframe(existing_data[['City', 'Indicator_Name', 'Value', 'Unit', 'Category']], use_container_width=True)

def export_custom_indicators_data():
    """Export custom indicators data for download"""
    
    data = load_custom_indicators_data()
    
    if not data.empty:
        csv = data.to_csv(index=False)
        return csv
    
    return None

def convert_custom_indicators_for_analysis():
    """Convert custom indicators data to format compatible with existing analysis modules"""
    
    indicators_data = load_custom_indicators_data()
    
    if indicators_data.empty:
        return pd.DataFrame()
    
    # Get research data for city information
    research_data = st.session_state.get('research_data', {})
    
    # Create a base structure for each city
    cities_data = []
    
    for i in range(1, 5):
        city = research_data.get(f'city{i}', '')
        country = research_data.get(f'country{i}', 'Not specified')
        
        if city:
            city_indicators = indicators_data[indicators_data['City'] == city]
            
            if not city_indicators.empty:
                # Build city data record
                city_record = {
                    'City': city,
                    'Country': country,
                    'Data_Source': 'Custom Indicators',
                    'Data_Entry_Date': datetime.now().isoformat()
                }
                
                # Add all indicators as columns
                for _, indicator in city_indicators.iterrows():
                    # Create a safe column name
                    col_name = indicator['Indicator_Name'].replace(' ', '_').replace('-', '_')
                    city_record[col_name] = indicator['Value']
                    
                    # Store metadata for later use
                    city_record[f"{col_name}_unit"] = indicator['Unit']
                    city_record[f"{col_name}_source"] = indicator['Source']
                    city_record[f"{col_name}_description"] = indicator['Description']
                    city_record[f"{col_name}_category"] = indicator.get('Category', 'Other')
                
                cities_data.append(city_record)
    
    if cities_data:
        return pd.DataFrame(cities_data)
    
    return pd.DataFrame()

def get_indicators_summary():
    """Get a summary of all custom indicators for display"""
    
    data = load_custom_indicators_data()
    
    if data.empty:
        return {}
    
    summary = {
        'total_indicators': len(data),
        'unique_cities': data['City'].nunique(),
        'categories': data['Category'].value_counts().to_dict() if 'Category' in data.columns else {},
        'indicators_per_city': data.groupby('City').size().to_dict(),
        'data': data
    }
    
    return summary

def check_analysis_readiness():
    """Check if analysis should be enabled - returns True if at least one indicator exists for all 4 cities"""
    
    # Get research data for city names
    if 'research_data' not in st.session_state:
        return False
    
    research_data = st.session_state.research_data
    target_cities = []
    
    for i in range(1, 5):
        city = research_data.get(f'city{i}', '')
        if city:
            target_cities.append(city)
    
    if len(target_cities) != 4:
        return False
    
    # Load indicators data
    indicators_data = load_custom_indicators_data()
    
    if indicators_data.empty:
        return False
    
    # Check if all cities have at least one indicator
    cities_with_data = set(indicators_data['City'].unique())
    target_cities_set = set(target_cities)
    
    # Return True if all 4 target cities have at least one indicator
    return target_cities_set.issubset(cities_with_data)

def get_common_indicators():
    """Get indicators that exist for all 4 cities"""
    
    if 'research_data' not in st.session_state:
        return []
    
    research_data = st.session_state.research_data
    target_cities = []
    
    for i in range(1, 5):
        city = research_data.get(f'city{i}', '')
        if city:
            target_cities.append(city)
    
    if len(target_cities) != 4:
        return []
    
    # Load indicators data
    indicators_data = load_custom_indicators_data()
    
    if indicators_data.empty:
        return []
    
    # Find indicators that exist for all cities
    common_indicators = []
    
    # Get all unique indicator names
    all_indicators = indicators_data['Indicator_Name'].unique()
    
    for indicator in all_indicators:
        indicator_cities = set(indicators_data[indicators_data['Indicator_Name'] == indicator]['City'].unique())
        
        # Check if this indicator exists for all target cities
        if set(target_cities).issubset(indicator_cities):
            common_indicators.append(indicator)
    
    return common_indicators

def update_session_state_for_analysis():
    """Update session state to enable analysis when data is ready"""
    
    # Check if analysis should be available
    if check_analysis_readiness():
        # Convert custom indicators to analysis format
        analysis_data = convert_custom_indicators_for_analysis()
        
        if not analysis_data.empty:
            # Update session state
            st.session_state.city_data = analysis_data.to_dict('records')
            st.session_state.use_custom_indicators = True
            st.session_state.data_collection_complete = True
            st.session_state.data_entered = True
