"""
City Data Collector - Initial Setup Module
This module handles the initial data collection process where users define their research question
and select 4 cities to study, with options for default indicators.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Default indicators configuration
DEFAULT_INDICATORS = {
    'environmental': {
        'Air_Quality': {'default': 70, 'min': 0, 'max': 100, 'description': 'Air Quality Index'},
        'Green_Space': {'default': 35, 'min': 0, 'max': 100, 'description': 'Green Space Coverage (%)'},
        'Renewable_Energy': {'default': 30, 'min': 0, 'max': 100, 'description': 'Renewable Energy Usage (%)'},
        'Waste_Management': {'default': 60, 'min': 0, 'max': 100, 'description': 'Waste Management Efficiency (%)'},
        'Water_Quality': {'default': 75, 'min': 0, 'max': 100, 'description': 'Water Quality Index'}
    },
    'social': {
        'Education_Index': {'default': 0.75, 'min': 0.0, 'max': 1.0, 'description': 'Education Development Index'},
        'Healthcare_Access': {'default': 80, 'min': 0, 'max': 100, 'description': 'Healthcare Access (%)'},
        'Safety_Index': {'default': 7.5, 'min': 0.0, 'max': 10.0, 'description': 'Safety Index (0-10)'},
        'Social_Inclusion': {'default': 65, 'min': 0, 'max': 100, 'description': 'Social Inclusion Index'},
        'Housing_Affordability': {'default': 60, 'min': 0, 'max': 100, 'description': 'Housing Affordability Index'}
    },
    'economic': {
        'GDP_per_Capita': {'default': 45000, 'min': 0, 'max': 150000, 'description': 'GDP per Capita ($)'},
        'Unemployment_Rate': {'default': 5.0, 'min': 0.0, 'max': 50.0, 'description': 'Unemployment Rate (%)'},
        'Innovation_Index': {'default': 65, 'min': 0, 'max': 100, 'description': 'Innovation Index'},
        'Business_Environment': {'default': 70, 'min': 0, 'max': 100, 'description': 'Business Environment Score'},
        'Income_Equality': {'default': 60, 'min': 0, 'max': 100, 'description': 'Income Equality Index'}
    }
}

def show_initial_setup():
    """Display the initial setup form for research question and city selection"""
    
    st.markdown("""
    <style>
    .setup-title {
        color: #1B4332;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .setup-subtitle {
        color: #2D5A3D;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    .info-box {
        background-color: #E8F5E8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #40736A;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="setup-title">🏗️ Research Setup & City Selection</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'setup_complete' not in st.session_state:
        st.session_state.setup_complete = False
    if 'research_data' not in st.session_state:
        st.session_state.research_data = {}
    
    # Step 1: Research Question
    st.markdown('<h2 class="setup-subtitle">🎯 Step 1: Define Your Research Question</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>💡 Research Focus:</strong> Define what you want to investigate about city sustainability. 
    This will guide your analysis and help you choose relevant indicators.
    </div>
    """, unsafe_allow_html=True)
    
    research_question = st.text_area(
        "What is your research question?",
        placeholder="Example: How do European cities compare in terms of environmental sustainability and social equity?",
        help="Be specific about what you want to study. This will be saved and referenced throughout your analysis.",
        value=st.session_state.research_data.get('research_question', '')
    )
    
    # Step 2: City Selection
    st.markdown('<h2 class="setup-subtitle">🏙️ Step 2: Select Four Cities to Study</h2>', unsafe_allow_html=True)
    
    st.info("Choose 4 cities that are relevant to your research question. Consider geographic diversity, size, or specific characteristics that match your research focus.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        city1 = st.text_input("City 1", value=st.session_state.research_data.get('city1', ''), placeholder="e.g., Copenhagen")
        country1 = st.text_input("Country 1 (optional)", value=st.session_state.research_data.get('country1', ''), placeholder="e.g., Denmark")
        
        city2 = st.text_input("City 2", value=st.session_state.research_data.get('city2', ''), placeholder="e.g., Singapore")
        country2 = st.text_input("Country 2 (optional)", value=st.session_state.research_data.get('country2', ''), placeholder="e.g., Singapore")
    
    with col2:
        city3 = st.text_input("City 3", value=st.session_state.research_data.get('city3', ''), placeholder="e.g., Vancouver")
        country3 = st.text_input("Country 3 (optional)", value=st.session_state.research_data.get('country3', ''), placeholder="e.g., Canada")
        
        city4 = st.text_input("City 4", value=st.session_state.research_data.get('city4', ''), placeholder="e.g., Amsterdam")
        country4 = st.text_input("Country 4 (optional)", value=st.session_state.research_data.get('country4', ''), placeholder="e.g., Netherlands")
    
    # Step 3: Indicator Selection
    st.markdown('<h2 class="setup-subtitle">📊 Step 3: Choose Your Indicators</h2>', unsafe_allow_html=True)
    
    indicator_choice = st.radio(
        "How would you like to handle sustainability indicators?",
        [
            "Use default values for all indicators (recommended for quick start)",
            "Customize some indicators",
            "Enter all indicators manually"
        ]
    )
    
    # Step 4: Setup Confirmation
    st.markdown('<h2 class="setup-subtitle">✅ Step 4: Confirm Setup</h2>', unsafe_allow_html=True)
    
    # Validation
    cities_filled = all([city1.strip(), city2.strip(), city3.strip(), city4.strip()])
    research_filled = len(research_question.strip()) > 10
    
    if cities_filled and research_filled:
        st.success("✅ All required information provided!")
        
        # Show summary
        with st.expander("📋 Review Your Setup", expanded=True):
            st.write(f"**Research Question:** {research_question}")
            st.write("**Selected Cities:**")
            st.write(f"1. {city1}{f', {country1}' if country1.strip() else ''}")
            st.write(f"2. {city2}{f', {country2}' if country2.strip() else ''}")
            st.write(f"3. {city3}{f', {country3}' if country3.strip() else ''}")
            st.write(f"4. {city4}{f', {country4}' if country4.strip() else ''}")
            st.write(f"**Indicator Approach:** {indicator_choice}")
        
        if st.button("🚀 Start Data Collection", type="primary"):
            # Save setup data
            research_data = {
                'research_question': research_question,
                'city1': city1, 'country1': country1 or "Not specified",
                'city2': city2, 'country2': country2 or "Not specified",
                'city3': city3, 'country3': country3 or "Not specified",
                'city4': city4, 'country4': country4 or "Not specified",
                'indicator_choice': indicator_choice,
                'setup_date': datetime.now().isoformat(),
                'setup_complete': True
            }
            
            st.session_state.research_data = research_data
            st.session_state.setup_complete = True
            
            # Create initial CSV file
            create_initial_csv(research_data)
            
            st.success("🎉 Setup complete! You can now proceed to data entry.")
            st.rerun()
    
    else:
        missing_items = []
        if not research_filled:
            missing_items.append("Research question (minimum 10 characters)")
        if not cities_filled:
            missing_items.append("All 4 city names")
        
        st.warning(f"⚠️ Please complete: {', '.join(missing_items)}")
    
    return st.session_state.get('setup_complete', False)

def show_data_entry():
    """Display the data entry interface after setup is complete"""
    
    st.markdown('<h1 class="setup-title">📝 City Data Entry</h1>', unsafe_allow_html=True)
    
    research_data = st.session_state.research_data
    indicator_choice = research_data.get('indicator_choice', '')
    
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
    
    # City selection for data entry
    city_options = []
    for i in range(1, 5):
        city = research_data.get(f'city{i}', '')
        country = research_data.get(f'country{i}', '')
        if country and country != "Not specified":
            city_options.append(f"{city} ({country})")
        else:
            city_options.append(city)
    
    selected_city_display = st.selectbox("Select city to enter data for:", city_options)
    selected_city_index = city_options.index(selected_city_display)
    
    city_names = [
        research_data.get('city1', ''),
        research_data.get('city2', ''),
        research_data.get('city3', ''),
        research_data.get('city4', '')
    ]
    country_names = [
        research_data.get('country1', 'Not specified'),
        research_data.get('country2', 'Not specified'),
        research_data.get('country3', 'Not specified'),
        research_data.get('country4', 'Not specified')
    ]
    
    selected_city = city_names[selected_city_index]
    selected_country = country_names[selected_city_index]
    
    # Data entry form
    if indicator_choice == "Use default values for all indicators (recommended for quick start)":
        show_default_data_entry(selected_city, selected_country)
    elif indicator_choice == "Customize some indicators":
        show_custom_data_entry(selected_city, selected_country)
    else:
        show_manual_data_entry(selected_city, selected_country)
    
    # Show current progress
    show_data_progress()

def show_default_data_entry(city_name, country_name):
    """Show data entry with default values"""
    
    st.markdown(f'<h3 class="setup-subtitle">🏙️ {city_name}, {country_name} - Quick Entry</h3>', unsafe_allow_html=True)
    
    st.info("🚀 Using default indicator values. You can adjust any values that you have specific data for.")
    
    with st.form(f"city_data_form_{city_name}"):
        # Basic info
        population = st.number_input("Population", min_value=0, value=1000000, help="Total city population")
        
        # Show all indicators with defaults
        st.markdown("**🌱 Environmental Indicators**")
        env_data = {}
        col1, col2 = st.columns(2)
        
        env_indicators = list(DEFAULT_INDICATORS['environmental'].items())
        for i, (key, config) in enumerate(env_indicators):
            with col1 if i % 2 == 0 else col2:
                if key == 'Air_Quality':
                    env_data[key] = st.slider(config['description'], config['min'], config['max'], config['default'])
                else:
                    env_data[key] = st.number_input(config['description'], 
                                                  min_value=float(config['min']), 
                                                  max_value=float(config['max']), 
                                                  value=float(config['default']))
        
        st.markdown("**👥 Social Indicators**")
        social_data = {}
        col3, col4 = st.columns(2)
        
        social_indicators = list(DEFAULT_INDICATORS['social'].items())
        for i, (key, config) in enumerate(social_indicators):
            with col3 if i % 2 == 0 else col4:
                if key == 'Education_Index':
                    social_data[key] = st.slider(config['description'], config['min'], config['max'], config['default'])
                else:
                    social_data[key] = st.number_input(config['description'], 
                                                     min_value=float(config['min']), 
                                                     max_value=float(config['max']), 
                                                     value=float(config['default']))
        
        st.markdown("**💰 Economic Indicators**")
        economic_data = {}
        col5, col6 = st.columns(2)
        
        economic_indicators = list(DEFAULT_INDICATORS['economic'].items())
        for i, (key, config) in enumerate(economic_indicators):
            with col5 if i % 2 == 0 else col6:
                if key == 'GDP_per_Capita':
                    economic_data[key] = st.number_input(config['description'], 
                                                       min_value=config['min'], 
                                                       max_value=config['max'], 
                                                       value=config['default'])
                else:
                    economic_data[key] = st.number_input(config['description'], 
                                                       min_value=float(config['min']), 
                                                       max_value=float(config['max']), 
                                                       value=float(config['default']))
        
        submitted = st.form_submit_button(f"💾 Save Data for {city_name}")
        
        if submitted:
            # Combine all data
            city_data = {
                'City': city_name,
                'Country': country_name,
                'Population': population,
                **env_data,
                **social_data,
                **economic_data,
                'Data_Entry_Date': datetime.now().isoformat(),
                'Data_Source': 'Default + User Input'
            }
            
            save_city_data(city_data)
            st.success(f"✅ Data saved for {city_name}!")
            st.rerun()

def show_custom_data_entry(city_name, country_name):
    """Show data entry with option to customize some indicators"""
    
    st.markdown(f'<h3 class="setup-subtitle">🏙️ {city_name}, {country_name} - Custom Entry</h3>', unsafe_allow_html=True)
    
    st.info("🎨 Choose which indicators to customize. Others will use default values.")
    
    # Let user choose which categories to customize
    customize_env = st.checkbox("Customize Environmental Indicators", value=False)
    customize_social = st.checkbox("Customize Social Indicators", value=False)
    customize_economic = st.checkbox("Customize Economic Indicators", value=False)
    
    with st.form(f"custom_city_data_form_{city_name}"):
        # Basic info
        population = st.number_input("Population", min_value=0, value=1000000)
        
        # Environmental indicators
        env_data = {}
        if customize_env:
            st.markdown("**🌱 Environmental Indicators (Customizable)**")
            col1, col2 = st.columns(2)
            env_indicators = list(DEFAULT_INDICATORS['environmental'].items())
            for i, (key, config) in enumerate(env_indicators):
                with col1 if i % 2 == 0 else col2:
                    env_data[key] = st.number_input(
                        config['description'], 
                        min_value=float(config['min']), 
                        max_value=float(config['max']), 
                        value=float(config['default'])
                    )
        else:
            # Use defaults
            for key, config in DEFAULT_INDICATORS['environmental'].items():
                env_data[key] = config['default']
            st.info("🔧 Environmental indicators will use default values")
        
        # Social indicators
        social_data = {}
        if customize_social:
            st.markdown("**👥 Social Indicators (Customizable)**")
            col3, col4 = st.columns(2)
            social_indicators = list(DEFAULT_INDICATORS['social'].items())
            for i, (key, config) in enumerate(social_indicators):
                with col3 if i % 2 == 0 else col4:
                    social_data[key] = st.number_input(
                        config['description'], 
                        min_value=float(config['min']), 
                        max_value=float(config['max']), 
                        value=float(config['default'])
                    )
        else:
            for key, config in DEFAULT_INDICATORS['social'].items():
                social_data[key] = config['default']
            st.info("🔧 Social indicators will use default values")
        
        # Economic indicators
        economic_data = {}
        if customize_economic:
            st.markdown("**💰 Economic Indicators (Customizable)**")
            col5, col6 = st.columns(2)
            economic_indicators = list(DEFAULT_INDICATORS['economic'].items())
            for i, (key, config) in enumerate(economic_indicators):
                with col5 if i % 2 == 0 else col6:
                    economic_data[key] = st.number_input(
                        config['description'], 
                        min_value=float(config['min']), 
                        max_value=float(config['max']), 
                        value=float(config['default'])
                    )
        else:
            for key, config in DEFAULT_INDICATORS['economic'].items():
                economic_data[key] = config['default']
            st.info("🔧 Economic indicators will use default values")
        
        submitted = st.form_submit_button(f"💾 Save Data for {city_name}")
        
        if submitted:
            city_data = {
                'City': city_name,
                'Country': country_name,
                'Population': population,
                **env_data,
                **social_data,
                **economic_data,
                'Data_Entry_Date': datetime.now().isoformat(),
                'Data_Source': 'Custom + Defaults'
            }
            
            save_city_data(city_data)
            st.success(f"✅ Data saved for {city_name}!")
            st.rerun()

def show_manual_data_entry(city_name, country_name):
    """Show completely manual data entry"""
    
    st.markdown(f'<h3 class="setup-subtitle">🏙️ {city_name}, {country_name} - Manual Entry</h3>', unsafe_allow_html=True)
    
    st.info("✏️ Enter all indicator values manually. This gives you full control over your data.")
    
    # This is similar to your existing manual input but more structured
    with st.form(f"manual_city_data_form_{city_name}"):
        population = st.number_input("Population", min_value=0, value=0)
        
        st.markdown("**🌱 Environmental Indicators**")
        col1, col2 = st.columns(2)
        with col1:
            air_quality = st.slider("Air Quality Index (0-100)", 0, 100, 50)
            green_space = st.slider("Green Space Coverage (%)", 0, 100, 30)
            renewable_energy = st.slider("Renewable Energy Usage (%)", 0, 100, 25)
        with col2:
            waste_management = st.slider("Waste Management Efficiency (%)", 0, 100, 60)
            water_quality = st.slider("Water Quality Index", 0, 100, 75)
        
        st.markdown("**👥 Social Indicators**")
        col3, col4 = st.columns(2)
        with col3:
            education_index = st.slider("Education Index (0-1)", 0.0, 1.0, 0.7)
            healthcare_access = st.slider("Healthcare Access (%)", 0, 100, 80)
            safety_index = st.slider("Safety Index (0-10)", 0.0, 10.0, 7.0)
        with col4:
            social_inclusion = st.slider("Social Inclusion Index", 0, 100, 65)
            housing_affordability = st.slider("Housing Affordability Index", 0, 100, 60)
        
        st.markdown("**💰 Economic Indicators**")
        col5, col6 = st.columns(2)
        with col5:
            gdp_per_capita = st.number_input("GDP per Capita ($)", min_value=0, value=30000)
            unemployment_rate = st.slider("Unemployment Rate (%)", 0.0, 50.0, 5.0)
            innovation_index = st.slider("Innovation Index (0-100)", 0, 100, 60)
        with col6:
            business_environment = st.slider("Business Environment Score", 0, 100, 70)
            income_equality = st.slider("Income Equality Index", 0, 100, 60)
        
        submitted = st.form_submit_button(f"💾 Save Data for {city_name}")
        
        if submitted:
            city_data = {
                'City': city_name,
                'Country': country_name,
                'Population': population,
                'Air_Quality': air_quality,
                'Green_Space': green_space,
                'Renewable_Energy': renewable_energy,
                'Waste_Management': waste_management,
                'Water_Quality': water_quality,
                'Education_Index': education_index,
                'Healthcare_Access': healthcare_access,
                'Safety_Index': safety_index,
                'Social_Inclusion': social_inclusion,
                'Housing_Affordability': housing_affordability,
                'GDP_per_Capita': gdp_per_capita,
                'Unemployment_Rate': unemployment_rate,
                'Innovation_Index': innovation_index,
                'Business_Environment': business_environment,
                'Income_Equality': income_equality,
                'Data_Entry_Date': datetime.now().isoformat(),
                'Data_Source': 'Manual Entry'
            }
            
            save_city_data(city_data)
            st.success(f"✅ Data saved for {city_name}!")
            st.rerun()

def create_initial_csv(research_data):
    """Create initial CSV file with research setup"""
    
    # Create data directory if it doesn't exist
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Create research metadata file
    metadata = {
        'Research_Question': [research_data['research_question']],
        'Setup_Date': [research_data['setup_date']],
        'City_1': [f"{research_data['city1']}, {research_data['country1']}"],
        'City_2': [f"{research_data['city2']}, {research_data['country2']}"],
        'City_3': [f"{research_data['city3']}, {research_data['country3']}"],
        'City_4': [f"{research_data['city4']}, {research_data['country4']}"],
        'Indicator_Approach': [research_data['indicator_choice']]
    }
    
    metadata_df = pd.DataFrame(metadata)
    metadata_df.to_csv(f"{data_dir}/research_metadata.csv", index=False)
    
    # Create empty cities data file with proper columns
    columns = [
        'City', 'Country', 'Population',
        # Environmental
        'Air_Quality', 'Green_Space', 'Renewable_Energy', 'Waste_Management', 'Water_Quality',
        # Social  
        'Education_Index', 'Healthcare_Access', 'Safety_Index', 'Social_Inclusion', 'Housing_Affordability',
        # Economic
        'GDP_per_Capita', 'Unemployment_Rate', 'Innovation_Index', 'Business_Environment', 'Income_Equality',
        # Metadata
        'Data_Entry_Date', 'Data_Source'
    ]
    
    empty_df = pd.DataFrame(columns=columns)
    empty_df.to_csv(f"{data_dir}/cities_data.csv", index=False)

def save_city_data(city_data):
    """Save city data to CSV file"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    csv_path = f"{data_dir}/cities_data.csv"
    
    # Read existing data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame()
    
    # Remove existing entry for this city if it exists
    if not df.empty and 'City' in df.columns:
        df = df[df['City'] != city_data['City']]
    
    # Add new data
    new_df = pd.DataFrame([city_data])
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Save back to CSV
    df.to_csv(csv_path, index=False)
    
    # Also update session state for immediate use
    if 'city_data' not in st.session_state:
        st.session_state.city_data = []
    
    # Update session state
    st.session_state.city_data = df.to_dict('records')

def show_data_progress():
    """Show progress of data entry"""
    
    st.markdown('<h3 class="setup-subtitle">📈 Data Entry Progress</h3>', unsafe_allow_html=True)
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    csv_path = f"{data_dir}/cities_data.csv"
    
    try:
        df = pd.read_csv(csv_path)
        if not df.empty:
            research_data = st.session_state.research_data
            target_cities = [
                research_data.get('city1', ''),
                research_data.get('city2', ''),
                research_data.get('city3', ''),
                research_data.get('city4', '')
            ]
            
            entered_cities = df['City'].tolist() if 'City' in df.columns else []
            progress = len([city for city in target_cities if city in entered_cities])
            
            st.progress(progress / 4)
            st.write(f"**Progress:** {progress}/4 cities completed")
            
            if progress > 0:
                st.write("**Cities with data:**")
                for city in target_cities:
                    if city in entered_cities:
                        st.write(f"✅ {city}")
                    else:
                        st.write(f"⏳ {city} - Pending")
            
            if progress == 4:
                st.success("🎉 All cities completed! Analysis sections are now available below.")
                
                # Show preview of collected data
                with st.expander("📊 Preview Collected Data", expanded=False):
                    st.dataframe(df)
        else:
            st.info("No data entered yet. Start with your first city above.")
    
    except FileNotFoundError:
        st.info("No data file found. Complete the setup first.")

def load_collected_data():
    """Load the collected data for analysis"""
    
    data_dir = "/Users/svenhominal/Desktop/PROJET START-UP/Sustainability_Assessment/Sustainability_Assessment/data"
    csv_path = f"{data_dir}/cities_data.csv"
    
    try:
        df = pd.read_csv(csv_path)
        if not df.empty:
            # Convert to the format expected by existing analysis modules
            st.session_state.city_data = df.to_dict('records')
            return df
    except FileNotFoundError:
        pass
    
    return pd.DataFrame()
