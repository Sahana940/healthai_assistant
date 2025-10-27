import streamlit as st
import sys
sys.path.append('..')
from utils.ai_model import get_ai_model
from utils.data_handler import HealthDataHandler
from utils.visualizations import HealthVisualizations
import pandas as pd

st.set_page_config(
    page_title="Health Analytics - HealthAI",
    page_icon="📊",
    layout="wide"
)

# Initialize
if 'ai_model' not in st.session_state:
    st.session_state.ai_model = get_ai_model()

if 'health_data' not in st.session_state:
    st.session_state.health_data = HealthDataHandler.generate_sample_health_data(30)

# Header
st.title("📊 Health Analytics Dashboard")
st.markdown("### Visualize and Monitor Your Health Metrics")

st.markdown("---")

# Time Period Selector
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    time_period = st.selectbox(
        "Select Time Period:",
        ["Last 7 Days", "Last 14 Days", "Last 30 Days", "Last 90 Days"],
        index=2
    )

with col2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        days_map = {
            "Last 7 Days": 7,
            "Last 14 Days": 14,
            "Last 30 Days": 30,
            "Last 90 Days": 90
        }
        st.session_state.health_data = HealthDataHandler.generate_sample_health_data(
            days_map[time_period]
        )
        st.rerun()

with col3:
    if st.button("📥 Export Data", use_container_width=True):
        csv = st.session_state.health_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="health_data.csv",
            mime="text/csv"
        )

# Get data
df = st.session_state.health_data
latest_metrics = df.iloc[-1]

st.markdown("---")

# Key Metrics Dashboard
st.subheader("🎯 Current Health Metrics")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    status, color, unit = HealthDataHandler.get_metric_status(
        'heart_rate', latest_metrics['heart_rate']
    )
    st.metric(
        "Heart Rate",
        f"{int(latest_metrics['heart_rate'])} {unit}",
        delta=f"{status}",
        delta_color="normal" if status == "Normal" else "inverse"
    )

with metric_col3:
    status, color, unit = HealthDataHandler.get_metric_status(
        'blood_glucose', latest_metrics['blood_glucose']
    )
    st.metric(
        "Blood Glucose",
        f"{int(latest_metrics['blood_glucose'])} {unit}",
        delta=f"{status}",
        delta_color="normal" if status == "Normal" else "inverse"
    )

with metric_col4:
    status, color, unit = HealthDataHandler.get_metric_status(
        'oxygen_saturation', latest_metrics['oxygen_saturation']
    )
    st.metric(
        "Oxygen Saturation",
        f"{int(latest_metrics['oxygen_saturation'])} {unit}",
        delta=f"{status}",
        delta_color="normal" if status == "Normal" else "inverse"
    )

st.markdown("---")

# Health Score Section
st.subheader("🏆 Overall Health Score")

health_score = HealthDataHandler.calculate_health_score({
    'heart_rate': latest_metrics['heart_rate'],
    'blood_pressure_systolic': latest_metrics['blood_pressure_systolic'],
    'blood_glucose': latest_metrics['blood_glucose'],
    'oxygen_saturation': latest_metrics['oxygen_saturation']
})

score_col1, score_col2 = st.columns([1, 2])

with score_col1:
    # Display gauge chart
    gauge_fig = HealthVisualizations.create_health_score_gauge(health_score)
    st.plotly_chart(gauge_fig, use_container_width=True)
    
    risk_level, risk_color = HealthDataHandler.get_risk_level(health_score)
    st.markdown(f"### Risk Level: :{risk_color}[{risk_level}]")

with score_col2:
    st.markdown("### 📈 Health Score Breakdown")
    
    score_components = {
        "Cardiovascular": 85 if latest_metrics['heart_rate'] <= 100 else 70,
        "Blood Pressure": 90 if latest_metrics['blood_pressure_systolic'] <= 120 else 75,
        "Metabolic": 80 if latest_metrics['blood_glucose'] <= 100 else 65,
        "Respiratory": 95 if latest_metrics['oxygen_saturation'] >= 95 else 70
    }
    
    for component, score in score_components.items():
        st.progress(score / 100, text=f"{component}: {score}/100")

st.markdown("---")

# Comprehensive Dashboard
st.subheader("📊 Comprehensive Health Metrics Dashboard")

dashboard_fig = HealthVisualizations.create_multi_metric_dashboard(df)
st.plotly_chart(dashboard_fig, use_container_width=True)

st.markdown("---")

# Detailed Metrics Section
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💓 Heart Rate", 
    "🩸 Blood Pressure", 
    "🍬 Blood Glucose", 
    "🫁 Oxygen & Temp",
    "📈 Correlations"
])

with tab1:
    st.markdown("### Heart Rate Trends")
    hr_fig = HealthVisualizations.create_metric_trend_chart(df, 'heart_rate', 'Heart Rate (bpm)')
    st.plotly_chart(hr_fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Heart Rate", f"{df['heart_rate'].mean():.1f} bpm")
        st.metric("Minimum", f"{df['heart_rate'].min()} bpm")
    with col2:
        st.metric("Maximum", f"{df['heart_rate'].max()} bpm")
        st.metric("Standard Deviation", f"{df['heart_rate'].std():.1f} bpm")
    
    # Distribution
    hr_dist = HealthVisualizations.create_metric_distribution(df, 'heart_rate', 'Heart Rate')
    st.plotly_chart(hr_dist, use_container_width=True)

with tab2:
    st.markdown("### Blood Pressure Analysis")
    
    bp_scatter = HealthVisualizations.create_bp_scatter(df)
    st.plotly_chart(bp_scatter, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Systolic Pressure")
        st.metric("Average", f"{df['blood_pressure_systolic'].mean():.1f} mmHg")
        st.metric("Range", f"{df['blood_pressure_systolic'].min()}-{df['blood_pressure_systolic'].max()} mmHg")
        
        sys_fig = HealthVisualizations.create_metric_trend_chart(
            df, 'blood_pressure_systolic', 'Systolic BP'
        )
        st.plotly_chart(sys_fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Diastolic Pressure")
        st.metric("Average", f"{df['blood_pressure_diastolic'].mean():.1f} mmHg")
        st.metric("Range", f"{df['blood_pressure_diastolic'].min()}-{df['blood_pressure_diastolic'].max()} mmHg")
        
        dia_fig = HealthVisualizations.create_metric_trend_chart(
            df, 'blood_pressure_diastolic', 'Diastolic BP'
        )
        st.plotly_chart(dia_fig, use_container_width=True)

with tab3:
    st.markdown("### Blood Glucose Monitoring")
    
    glucose_fig = HealthVisualizations.create_metric_trend_chart(
        df, 'blood_glucose', 'Blood Glucose (mg/dL)'
    )
    st.plotly_chart(glucose_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Glucose", f"{df['blood_glucose'].mean():.1f} mg/dL")
    with col2:
        high_readings = len(df[df['blood_glucose'] > 100])
        st.metric("High Readings", f"{high_readings}/{len(df)}")
    with col3:
        low_readings = len(df[df['blood_glucose'] < 70])
        st.metric("Low Readings", f"{low_readings}/{len(df)}")
    
    glucose_dist = HealthVisualizations.create_metric_distribution(
        df, 'blood_glucose', 'Blood Glucose'
    )
    st.plotly_chart(glucose_dist, use_container_width=True)

with tab4:
    st.markdown("### Oxygen Saturation & Body Temperature")
    
    col1, col2 = st.columns(2)
    
    with col1:
        o2_fig = HealthVisualizations.create_metric_trend_chart(
            df, 'oxygen_saturation', 'Oxygen Saturation (%)'
        )
        st.plotly_chart(o2_fig, use_container_width=True)
        
        st.metric("Average O2 Saturation", f"{df['oxygen_saturation'].mean():.1f}%")
        low_o2 = len(df[df['oxygen_saturation'] < 95])
        st.metric("Readings Below 95%", f"{low_o2}/{len(df)}")
    
    with col2:
        temp_fig = HealthVisualizations.create_metric_trend_chart(
            df, 'temperature', 'Body Temperature (°F)'
        )
        st.plotly_chart(temp_fig, use_container_width=True)
        
        st.metric("Average Temperature", f"{df['temperature'].mean():.1f}°F")
        fever_count = len(df[df['temperature'] > 99.5])
        st.metric("Fever Readings", f"{fever_count}/{len(df)}")

with tab5:
    st.markdown("### Metric Correlations")
    st.info("Understanding how your health metrics relate to each other")
    
    corr_heatmap = HealthVisualizations.create_correlation_heatmap(df)
    st.plotly_chart(corr_heatmap, use_container_width=True)
    
    st.markdown("""
    **Interpreting the Heatmap:**
    - Values close to 1 (red): Strong positive correlation
    - Values close to 0 (white): No correlation
    - Values close to -1 (blue): Strong negative correlation
    """)

st.markdown("---")

# AI Insights Section
st.subheader("🤖 AI-Powered Health Insights")

if st.button("🔍 Generate AI Analysis", type="primary"):
    with st.spinner("Analyzing your health trends..."):
        # Prepare metrics summary
        metrics_summary = {
            'heart_rate': df['heart_rate'].tolist(),
            'blood_pressure_systolic': df['blood_pressure_systolic'].tolist(),
            'blood_glucose': df['blood_glucose'].tolist(),
            'oxygen_saturation': df['oxygen_saturation'].tolist(),
            'temperature': df['temperature'].tolist()
        }
        
        # Get AI analysis
        ai_insights = st.session_state.ai_model.analyze_health_trends(metrics_summary)
        
        st.success("✅ Analysis Complete")
        
        st.markdown(
            f"""
            <div style='background-color: #e8f4f8; padding: 25px; border-radius: 10px; 
                        border-left: 5px solid #00b4d8; line-height: 1.8;'>
                {ai_insights.replace('\n', '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# Health Recommendations
st.subheader("💡 Personalized Recommendations")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("""
    ### 🥗 Lifestyle Tips
    
    Based on your current metrics:
    
    - **Exercise**: 30 minutes daily moderate activity
    - **Diet**: Balanced nutrition, limit processed foods
    - **Hydration**: 8 glasses of water per day
    - **Sleep**: 7-9 hours per night
    - **Stress**: Practice relaxation techniques
    """)

with rec_col2:
    st.markdown("""
    ### ⚠️ Warning Signs to Watch
    
    Seek medical attention if you experience:
    
    - Chest pain or pressure
    - Difficulty breathing
    - Severe headache
    - Blood pressure > 180/120
    - Blood glucose < 70 or > 200
    - Persistent symptoms
    """)

# Data Table
st.markdown("---")
st.subheader("📋 Detailed Data Table")

if st.checkbox("Show Raw Data"):
    st.dataframe(
        df.style.background_gradient(cmap='RdYlGn', subset=['heart_rate', 'blood_glucose']),
        use_container_width=True
    )

# Sidebar
with st.sidebar:
    st.header("📊 Analytics Info")
    st.markdown("""
    This dashboard provides comprehensive visualization 
    and analysis of your health metrics.
    
    **Features:**
    - Real-time metric tracking
    - Trend analysis
    - AI-powered insights
    - Correlation analysis
    - Risk assessment
    """)
    
    st.divider()
    
    st.markdown("### ⚙️ Settings")
    
    show_normal_ranges = st.checkbox("Show Normal Ranges", value=True)
    auto_refresh = st.checkbox("Auto Refresh", value=False)
    
    if auto_refresh:
        import time
        time.sleep(5)
        st.rerun()
    
    st.divider()
    
    st.markdown("### 📈 Quick Stats")
    st.metric("Total Data Points", len(df))
    st.metric("Time Period", time_period)
    st.metric("Data Quality", "Good ✓")
    
    st.divider()
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🔄 Reset Data", use_container_width=True):
        st.session_state.health_data = HealthDataHandler.generate_sample_health_data(30)
        st.rerun()
delta_color="normal" if status == "Normal" else "inverse"

with metric_col2:
    status, color, unit = HealthDataHandler.get_metric_status(
        'blood_pressure_systolic', latest_metrics['blood_pressure_systolic']
    )
    st.metric(
        "Blood Pressure",
        f"{int(latest_metrics['blood_pressure_systolic'])}/{int(latest_metrics['blood_pressure_diastolic'])} {unit}",
        delta=f"{status}",)