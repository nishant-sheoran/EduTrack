# 📊 Teacher Dashboard - EduTrack

A sleek, modern teacher dashboard built with Streamlit featuring a bento grid layout for comprehensive classroom analytics and management.

## 🚀 Features

### 📈 Key Performance Indicators
- **Attendance Summary**: Real-time attendance tracking with delta indicators
- **Engagement Summary**: Student engagement metrics with trend analysis
- **Session Duration**: Current and historical session length tracking

### 📊 Analytics & Insights
- **Engagement Timeline**: Interactive line chart showing daily engagement trends
- **Topic Engagement Analytics**: Bar chart displaying dissociation rates by subject

### 🎥 Media & Documents
- **Latest Video Session**: Embedded video player with session details
- **Generated Transcripts**: Downloadable PDF transcripts with metadata

### ⚙️ Configuration & System
- **Configuration Panel**: Customizable settings for video quality, animations, and sensitivity
- **System Health**: Real-time monitoring of API connections, disk usage, and system messages

## 🎨 Design Features

- **Dark Theme**: Modern dark interface with custom styling
- **Bento Grid Layout**: Responsive card-based design using Streamlit columns
- **Interactive Elements**: Dropdowns, sliders, and buttons for configuration
- **Real-time Updates**: Dynamic data visualization with Plotly charts
- **Responsive Design**: Optimized for laptop and desktop screens

## 🛠️ Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have the following files:
   # - dashboard.py
   # - .streamlit/config.toml
   # - requirements.txt
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - The dashboard will load with the dark theme automatically

## 📁 File Structure

```
frontend/
├── dashboard.py              # Main Streamlit application
├── .streamlit/
│   └── config.toml          # Streamlit configuration (dark theme)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🎯 Usage

### Dashboard Sections

1. **Key Performance Indicators (Row 1)**
   - View attendance, engagement, and session metrics
   - Monitor trends with delta indicators

2. **Analytics & Insights (Row 2)**
   - Analyze engagement patterns over time
   - Review topic-specific performance data

3. **Media & Documents (Row 3)**
   - Watch recorded video sessions
   - Download generated transcripts

4. **Configuration & System (Row 4)**
   - Adjust system settings and preferences
   - Monitor system health and status

### Interactive Features

- **Configuration Panel**: Modify video quality, animation style, and sensitivity thresholds
- **System Health**: Check API status, disk usage, and system messages
- **Download Transcripts**: Access generated PDF files
- **Refresh Data**: Update system status and metrics

## 🎨 Customization

### Theme Configuration
The dark theme is configured in `.streamlit/config.toml`:
- Primary color: `#667eea` (blue-purple gradient)
- Background: Dark theme with custom styling
- Font: Sans serif for modern appearance

### Adding New Features
To extend the dashboard:
1. Add new sections using `st.columns()`
2. Create custom CSS classes for styling
3. Integrate additional data sources
4. Add new interactive components

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive data visualization

### Data Sources
- Sample data is generated using random functions
- Real implementation would connect to actual databases/APIs
- Charts use Plotly for enhanced interactivity

### Performance
- Data caching with `@st.cache_data`
- Responsive layout for different screen sizes
- Optimized for desktop/laptop viewing

## 🚀 Deployment

### Local Development
```bash
streamlit run dashboard.py
```

### Production Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables if needed
3. Deploy to Streamlit Cloud, Heroku, or other platforms
4. Configure production settings in `.streamlit/config.toml`

## 📝 Notes

- The dashboard uses placeholder data for demonstration
- Video URL is a sample YouTube link
- Download buttons contain placeholder PDF content
- System health metrics are randomly generated
- Real implementation would require backend integration

## 🤝 Contributing

To enhance the dashboard:
1. Add new analytics sections
2. Improve data visualization
3. Enhance mobile responsiveness
4. Add more configuration options
5. Integrate with real data sources

---

**Built with ❤️ using Streamlit** 