import streamlit as st

def show_intro():
    """Display a compact introduction for the sustainability assessment app"""
    
    # Always show the full intro since we're keeping everything on one page
    st.markdown("""
    <style>
    .intro-title {
        color: #1B4332;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .intro-section {
        color: #2D5A3D;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    .intro-subsection {
        color: #40736A;
        font-size: 1.1rem;
        font-weight: bold;
        margin: 0.5rem 0 0.3rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    # Introduction content
    st.markdown('<h2 class="intro-section">Welcome to Our Sustainability Platform</h2>', unsafe_allow_html=True)
    
    st.write("""
    This comprehensive tool helps evaluate and compare the sustainability performance of cities 
    across multiple dimensions including environmental, social, and economic factors.
    """)
    
    # Key features
    st.markdown('<h3 class="subsection-title">🎯 Key Features</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Data Analysis**")
        st.write("- Comprehensive sustainability metrics")
        st.write("- Multi-dimensional assessment")
        st.write("- Real-time data processing")
        
    with col2:
        st.write("**📈 Visualization**")
        st.write("- Interactive spider plots")
        st.write("- City ranking systems")
        st.write("- Comparative analysis")
    
    # How it works
    st.markdown('<h3 class="subsection-title">🔄 How It Works</h3>', unsafe_allow_html=True)
    
    st.write("""
    1. **Data Input**: Upload or input sustainability data for cities
    2. **Analysis**: Our algorithms process and analyze the data
    3. **Visualization**: View results through interactive charts and rankings
    4. **Comparison**: Compare cities across different sustainability metrics
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #40736A; font-style: italic;">'
        'Building sustainable cities for a better future 🌍</p>', 
        unsafe_allow_html=True
    )
