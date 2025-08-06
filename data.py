import streamlit as st
import pandas as pd
import numpy as np

def show_data_section():
    """Display the data input and management section - Legacy support"""
    
    # Custom CSS for dark green styling
    st.markdown("""
    <style>
    .section-title {
        color: #1B4332;
        font-size: 2.0rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subsection-title {
        color: #2D5A3D;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    .metric-title {
        color: #40736A;
        font-size: 1.1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">📊 Legacy Data Input (Optional)</h2>', unsafe_allow_html=True)
    
    st.info("""
    ℹ️ **Note:** This is the legacy data input method. The recommended approach is to use the 
    structured research setup at the beginning of the application, but you can still use this 
    for quick testing or additional data entry.
    """)
    
    # Data input method selection
    st.markdown('<h3 class="subsection-title">Quick Data Input</h3>', unsafe_allow_html=True)
    
    input_method = st.radio(
        "Choose how to input city data:",
        ["Use Sample Data", "Upload CSV File", "Manual Input"]
    )
    
    if input_method == "Manual Input":
        show_manual_input()
    elif input_method == "Upload CSV File":
        show_file_upload()
    else:
        show_sample_data()
    
    # Always display current data if available
    if 'city_data' in st.session_state and st.session_state.city_data:
        display_current_data()
        return pd.DataFrame(st.session_state.city_data)
    
    return None

def show_manual_input():
    """Show manual data input form"""
    st.markdown('<h3 class="subsection-title">🏙️ Add City Data Manually</h3>', unsafe_allow_html=True)
    
    with st.form("city_data_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            city_name = st.text_input("City Name")
            country = st.text_input("Country")
            population = st.number_input("Population", min_value=0, value=0)
            
        with col2:
            # Environmental metrics
            st.markdown('<p class="metric-title">🌱 Environmental Metrics</p>', unsafe_allow_html=True)
            air_quality = st.slider("Air Quality Index (0-100)", 0, 100, 50)
            green_space = st.slider("Green Space Coverage (%)", 0, 100, 30)
            renewable_energy = st.slider("Renewable Energy Usage (%)", 0, 100, 25)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Social metrics
            st.markdown('<p class="metric-title">👥 Social Metrics</p>', unsafe_allow_html=True)
            education_index = st.slider("Education Index (0-1)", 0.0, 1.0, 0.7)
            healthcare_access = st.slider("Healthcare Access (%)", 0, 100, 80)
            safety_index = st.slider("Safety Index (0-10)", 0.0, 10.0, 7.0)
            
        with col4:
            # Economic metrics
            st.markdown('<p class="metric-title">💰 Economic Metrics</p>', unsafe_allow_html=True)
            gdp_per_capita = st.number_input("GDP per Capita ($)", min_value=0, value=30000)
            unemployment_rate = st.slider("Unemployment Rate (%)", 0.0, 50.0, 5.0)
            innovation_index = st.slider("Innovation Index (0-100)", 0, 100, 60)
        
        submitted = st.form_submit_button("Add City Data")
        
        if submitted and city_name:
            # Store data in session state
            if 'city_data' not in st.session_state:
                st.session_state.city_data = []
            
            city_data = {
                'City': city_name,
                'Country': country,
                'Population': population,
                'Air_Quality': air_quality,
                'Green_Space': green_space,
                'Renewable_Energy': renewable_energy,
                'Education_Index': education_index,
                'Healthcare_Access': healthcare_access,
                'Safety_Index': safety_index,
                'GDP_per_Capita': gdp_per_capita,
                'Unemployment_Rate': unemployment_rate,
                'Innovation_Index': innovation_index
            }
            
            st.session_state.city_data.append(city_data)
            st.success(f"✅ Data for {city_name} has been added successfully!")
            st.rerun()

def show_file_upload():
    """Show file upload interface"""
    st.markdown('<h3 class="subsection-title">📁 Upload CSV File</h3>', unsafe_allow_html=True)
    
    st.info("""
    **CSV Format Requirements:**
    Your CSV file should contain columns for: City, Country, Population, Air_Quality, 
    Green_Space, Renewable_Energy, Education_Index, Healthcare_Access, Safety_Index, 
    GDP_per_Capita, Unemployment_Rate, Innovation_Index
    """)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.city_data = df.to_dict('records')
            st.success(f"✅ Successfully uploaded data for {len(df)} cities!")
            st.dataframe(df)
            st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

def show_sample_data():
    """Show sample data option"""
    st.markdown('<h3 class="subsection-title">🎯 Use Sample Data</h3>', unsafe_allow_html=True)
    
    if st.button("Load Sample Cities Data"):
        sample_data = [
            {
                'City': 'Copenhagen', 'Country': 'Denmark', 'Population': 660000,
                'Air_Quality': 85, 'Green_Space': 60, 'Renewable_Energy': 80,
                'Education_Index': 0.9, 'Healthcare_Access': 95, 'Safety_Index': 8.5,
                'GDP_per_Capita': 65000, 'Unemployment_Rate': 4.2, 'Innovation_Index': 88
            },
            {
                'City': 'Singapore', 'Country': 'Singapore', 'Population': 5900000,
                'Air_Quality': 75, 'Green_Space': 47, 'Renewable_Energy': 45,
                'Education_Index': 0.85, 'Healthcare_Access': 92, 'Safety_Index': 9.2,
                'GDP_per_Capita': 72000, 'Unemployment_Rate': 2.8, 'Innovation_Index': 85
            },
            {
                'City': 'Zurich', 'Country': 'Switzerland', 'Population': 420000,
                'Air_Quality': 88, 'Green_Space': 55, 'Renewable_Energy': 70,
                'Education_Index': 0.92, 'Healthcare_Access': 96, 'Safety_Index': 8.8,
                'GDP_per_Capita': 85000, 'Unemployment_Rate': 2.5, 'Innovation_Index': 90
            },
            {
                'City': 'Vancouver', 'Country': 'Canada', 'Population': 675000,
                'Air_Quality': 82, 'Green_Space': 65, 'Renewable_Energy': 85,
                'Education_Index': 0.88, 'Healthcare_Access': 90, 'Safety_Index': 8.0,
                'GDP_per_Capita': 55000, 'Unemployment_Rate': 5.1, 'Innovation_Index': 75
            },
            {
                'City': 'Amsterdam', 'Country': 'Netherlands', 'Population': 875000,
                'Air_Quality': 78, 'Green_Space': 45, 'Renewable_Energy': 65,
                'Education_Index': 0.86, 'Healthcare_Access': 88, 'Safety_Index': 7.8,
                'GDP_per_Capita': 58000, 'Unemployment_Rate': 3.8, 'Innovation_Index': 82
            }
        ]
        
        st.session_state.city_data = sample_data
        st.success("✅ Sample data loaded successfully!")
        st.rerun()

def display_current_data():
    """Display currently loaded city data"""
    st.markdown('<h3 class="subsection-title">📋 Current Data</h3>', unsafe_allow_html=True)
    
    if 'city_data' in st.session_state and st.session_state.city_data:
        df = pd.DataFrame(st.session_state.city_data)
        
        # Display summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Cities", len(df))
        with col2:
            st.metric("Countries", df['Country'].nunique())
        with col3:
            st.metric("Avg Population", f"{df['Population'].mean():,.0f}")
        
        # Display the data table
        st.dataframe(df, use_container_width=True)
        
        # Option to clear data
        if st.button("🗑️ Clear All Data"):
            st.session_state.city_data = []
            st.success("All data cleared!")
            st.rerun()
    else:
        st.info("No data loaded yet. Please add some city data above.")

def get_city_data():
    """Return the current city data as a DataFrame"""
    if 'city_data' in st.session_state and st.session_state.city_data:
        return pd.DataFrame(st.session_state.city_data)
    return pd.DataFrame()
