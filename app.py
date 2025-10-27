import streamlit as st
from config import config
from utils.ai_model import get_ai_model
from utils.data_handler import HealthDataHandler

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #00b4d8;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #00b4d8;
        margin: 0.5rem 0;
    }
    .stButton>button {
        background-color: #00b4d8;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0077b6;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'ai_model' not in st.session_state:
    st.session_state.ai_model = get_ai_model()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {
        'age': 30,
        'gender': 'Not specified',
        'conditions': 'None',
        'medications': 'None'
    }

def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">🏥 HealthAI: Intelligent Healthcare Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Powered by IBM Granite AI • Your Personal Health Companion</div>', unsafe_allow_html=True)
    
    # Sidebar - Patient Profile
    with st.sidebar:
        st.header("👤 Patient Profile")
        
        st.session_state.patient_data['age'] = st.number_input(
            "Age", 
            min_value=1, 
            max_value=120, 
            value=st.session_state.patient_data['age']
        )
        
        st.session_state.patient_data['gender'] = st.selectbox(
            "Gender",
            ["Male", "Female", "Other", "Prefer not to say"],
            index=0 if st.session_state.patient_data['gender'] == 'Male' else 1
        )
        
        st.session_state.patient_data['conditions'] = st.text_area(
            "Existing Conditions",
            value=st.session_state.patient_data['conditions'],
            help="List any chronic conditions"
        )
        
        st.session_state.patient_data['medications'] = st.text_area(
            "Current Medications",
            value=st.session_state.patient_data['medications'],
            help="List current medications"
        )
        
        st.divider()
        
        # Quick Stats
        st.subheader("📊 Quick Stats")
        health_data = HealthDataHandler.generate_sample_health_data(30)
        latest_metrics = health_data.iloc[-1]
        
        health_score = HealthDataHandler.calculate_health_score({
            'heart_rate': latest_metrics['heart_rate'],
            'blood_pressure_systolic': latest_metrics['blood_pressure_systolic'],
            'blood_glucose': latest_metrics['blood_glucose'],
            'oxygen_saturation': latest_metrics['oxygen_saturation']
        })
        
        risk_level, risk_color = HealthDataHandler.get_risk_level(health_score)
        
        st.metric("Health Score", f"{health_score}/100")
        st.markdown(f"**Risk Level:** :{risk_color}[{risk_level}]")
        
        st.divider()
        st.markdown("**ℹ️ Disclaimer**")
        st.caption("This AI assistant provides information for educational purposes only. Always consult healthcare professionals for medical advice.")
    
    # Main Content
    st.markdown("---")
    
    # Welcome Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Patient Chat</h3>
            <p>Ask health questions and get AI-powered answers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🩺 Disease Prediction</h3>
            <p>Analyze symptoms for potential conditions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💊 Treatment Plans</h3>
            <p>Get personalized treatment recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Patient Chat Interface
    st.header("💬 Chat with HealthAI")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(msg['user'])
            with st.chat_message("assistant", avatar="🏥"):
                st.write(msg['assistant'])
    
    # Chat input
    user_input = st.chat_input("Ask me anything about your health...")
    
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generate AI response
        with st.chat_message("assistant", avatar="🏥"):
            with st.spinner("Thinking..."):
                ai_response = st.session_state.ai_model.chat_response(
                    user_input,
                    st.session_state.chat_history
                )
                st.write(ai_response)
        
        # Save to history
        st.session_state.chat_history.append({
            'user': user_input,
            'assistant': ai_response
        })
        
        # Keep only last 10 exchanges
        if len(st.session_state.chat_history) > 10:
            st.session_state.chat_history = st.session_state.chat_history[-10:]
        
        st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")
    
    # Quick Links
    st.subheader("🚀 Quick Access")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🩺 Go to Disease Prediction", use_container_width=True):
            st.switch_page("pages/1_🩺_Disease_Prediction.py")
    
    with col2:
        if st.button("💊 Go to Treatment Plans", use_container_width=True):
            st.switch_page("pages/2_💊_Treatment_Plans.py")
    
    with col3:
        if st.button("📊 Go to Health Analytics", use_container_width=True):
            st.switch_page("pages/3_📊_Health_Analytics.py")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>HealthAI</strong> - Empowering Health Decisions with AI</p>
        <p>Powered by IBM Granite AI Model • Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()