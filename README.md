# 🌿 City Sustainability Assessment Platform

A comprehensive web application built with Streamlit for evaluating and comparing the sustainability performance of cities across multiple dimensions including environmental, social, and economic factors.

## 🌟 Features

### 📊 Data Management
- **Manual Input**: Add city data through an intuitive form interface
- **CSV Upload**: Bulk upload city data from CSV files
- **Sample Data**: Use pre-loaded sample cities for testing and demonstration
- **Data Validation**: Automatic validation and normalization of input data

### 📈 Comprehensive Analysis
- **Overview Dashboard**: High-level sustainability metrics and performance summaries
- **Environmental Analysis**: Air quality, green space, and renewable energy metrics
- **Social Analysis**: Education, healthcare, and safety indicators
- **Economic Analysis**: GDP, employment, and innovation metrics
- **Comparative Analysis**: Side-by-side city comparisons

### 🕸️ Interactive Spider Plots
- **Individual City Profiles**: Detailed radar charts for single cities
- **Multi-City Comparisons**: Compare up to 5 cities simultaneously
- **Category-Specific Views**: Focus on environmental, social, or economic dimensions
- **Customizable Visualizations**: Interactive plots with adjustable parameters

### 🏆 Comprehensive Rankings
- **Overall Sustainability Rankings**: Complete city performance rankings
- **Dimension-Specific Rankings**: Environmental, social, and economic leaderboards
- **Custom Weighted Rankings**: User-defined weights for personalized rankings
- **Performance Trends**: Statistical insights and correlation analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Sustainability_Assessment
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Open your browser**
   The application will automatically open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
Sustainability_Assessment/
│
├── main.py              # Main application entry point
├── intro.py             # Introduction and welcome page
├── data.py              # Data input and management functionality
├── analysis.py          # Comprehensive analysis and visualizations
├── spider_plot.py       # Interactive spider/radar plots
├── ranking.py           # City rankings and performance comparisons
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🎯 Usage Guide

### 1. Introduction Page
- Overview of the platform capabilities
- Key features and navigation guide
- Getting started instructions

### 2. Data Management
Choose from three data input methods:

**Manual Input:**
- Add cities one by one using the interactive form
- Input environmental, social, and economic metrics
- Real-time validation and feedback

**CSV Upload:**
- Upload bulk city data from CSV files
- Required columns: City, Country, Population, Air_Quality, Green_Space, Renewable_Energy, Education_Index, Healthcare_Access, Safety_Index, GDP_per_Capita, Unemployment_Rate, Innovation_Index

**Sample Data:**
- Load pre-configured sample cities (Copenhagen, Singapore, Zurich, Vancouver, Amsterdam)
- Perfect for testing and demonstration purposes

### 3. Analysis Dashboard
Explore comprehensive sustainability analysis:

- **Overview Dashboard**: Key performance indicators and top performers
- **Environmental Analysis**: Air quality, green space, renewable energy metrics
- **Social Analysis**: Education, healthcare, safety performance
- **Economic Analysis**: GDP, employment, innovation indicators
- **Comparative Analysis**: Multi-city performance comparisons

### 4. Spider Plot Visualizations
Create interactive radar charts:

- **Individual Analysis**: Detailed profile for single cities
- **Multi-City Comparison**: Compare multiple cities simultaneously
- **Category Views**: Focus on specific sustainability dimensions
- **Interactive Options**: Customize colors, opacity, and metrics

### 5. Ranking System
Comprehensive city rankings:

- **Overall Rankings**: Complete sustainability performance rankings
- **Category Rankings**: Environmental, social, economic leaderboards
- **Custom Weights**: Create personalized rankings with custom weights
- **Performance Insights**: Statistical analysis and trends

## 📊 Sustainability Metrics

### 🌱 Environmental Dimension
- **Air Quality Index** (0-100): Higher values indicate better air quality
- **Green Space Coverage** (%): Percentage of city area covered by green spaces
- **Renewable Energy Usage** (%): Percentage of energy from renewable sources

### 👥 Social Dimension
- **Education Index** (0-1): Composite measure of educational attainment and quality
- **Healthcare Access** (%): Percentage of population with access to quality healthcare
- **Safety Index** (0-10): Composite measure of public safety and crime rates

### 💰 Economic Dimension
- **GDP per Capita** ($): Economic output per person
- **Unemployment Rate** (%): Percentage of unemployed population (lower is better)
- **Innovation Index** (0-100): Measure of innovation capacity and technology adoption

## 🎨 Design Features

### Dark Green Theme
- Professional dark green color scheme (`#1B4332`, `#2D5A3D`, `#40736A`)
- Clean and modern interface design
- Consistent styling across all components

### Interactive Elements
- Responsive charts and visualizations
- Real-time data updates
- Intuitive navigation and user controls

### User Experience
- Clear section organization
- Comprehensive help and guidance
- Professional data presentation

## 🔧 Customization

### Adding New Metrics
1. Update the data input forms in `data.py`
2. Modify analysis calculations in `analysis.py`
3. Add new visualization components as needed
4. Update spider plot configurations in `spider_plot.py`

### Styling Modifications
- Update CSS styles in `main.py`
- Modify color schemes and themes
- Customize chart appearances in individual modules

### Extending Functionality
- Add new analysis types in `analysis.py`
- Create additional ranking methodologies in `ranking.py`
- Implement new visualization types

## 📈 Technical Details

### Data Processing
- Automatic normalization of metrics to 0-1 scale
- Weighted scoring algorithms for composite indices
- Statistical analysis and correlation calculations

### Visualization Engine
- Plotly for interactive charts and graphs
- Streamlit components for user interface
- Responsive design for various screen sizes

### Performance Optimization
- Efficient data handling with pandas
- Caching mechanisms for improved speed
- Modular architecture for maintainability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes and improvements
- New features and functionality
- Documentation enhancements
- Performance optimizations

## 📞 Support

For questions, issues, or suggestions:
- Create an issue in the project repository
- Review the documentation and usage examples
- Check existing issues for similar problems

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for sustainable city development**