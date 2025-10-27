import streamlit as st
import sys
sys.path.append('..')
from utils.ai_model import get_ai_model
from utils.data_handler import HealthDataHandler
from config import config

st.set_page_config(
    page_title="Disease Prediction - HealthAI",
    page_icon="🩺",
    layout="wide"
)

# Initialize AI model
if 'ai_model' not in st.session_state:
    st.session_state.ai_model = get_ai_model()

if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {
        'age': 30,
        'gender': 'Not specified'
    }

# Header
st.title("🩺 Disease Prediction System")
st.markdown("### Analyze your symptoms to identify potential health conditions")

st.markdown("---")

# Symptom Input Section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Enter Your Symptoms")
    
    # Common symptoms checklist
    st.markdown("**Select from common symptoms:**")
    
    symptom_cols = st.columns(3)
    
    common_symptoms = [
        "Fever", "Cough", "Headache", "Fatigue", "Nausea",
        "Sore Throat", "Body Aches", "Shortness of Breath",
        "Chest Pain", "Dizziness", "Abdominal Pain", "Runny Nose",
        "Sneezing", "Vomiting", "Diarrhea", "Rash",
        "Joint Pain", "Back Pain", "Loss of Appetite", "Insomnia"
    ]
    
    selected_symptoms = []
    
    for idx, symptom in enumerate(common_symptoms):
        col_idx = idx % 3
        with symptom_cols[col_idx]:
            if st.checkbox(symptom, key=f"symptom_{symptom}"):
                selected_symptoms.append(symptom.lower())
    
    st.markdown("---")
    
    # Additional symptoms
    additional_symptoms = st.text_area(
        "Add other symptoms (comma-separated):",
        placeholder="e.g., difficulty swallowing, numbness in hands",
        help="Enter any additional symptoms not listed above"
    )
    
    if additional_symptoms:
        additional = [s.strip().lower() for s in additional_symptoms.split(",") if s.strip()]
        selected_symptoms.extend(additional)
    
    # Symptom duration
    duration = st.selectbox(
        "How long have you experienced these symptoms?",
        ["Less than 1 day", "1-3 days", "3-7 days", "1-2 weeks", "More than 2 weeks"]
    )
    
    # Severity
    severity = st.slider(
        "Rate the overall severity (1=Mild, 10=Severe)",
        min_value=1,
        max_value=10,
        value=5
    )

with col2:
    st.subheader("👤 Patient Information")
    
    # Patient details
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    existing_conditions = st.text_area(
        "Existing Conditions",
        placeholder="e.g., Diabetes, Hypertension",
        help="List any chronic health conditions"
    )
    
    # Update session state
    st.session_state.patient_data['age'] = age
    st.session_state.patient_data['gender'] = gender
    st.session_state.patient_data['conditions'] = existing_conditions

st.markdown("---")

# Analysis Section
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    analyze_button = st.button(
        "🔍 Analyze Symptoms",
        type="primary",
        use_container_width=True,
        disabled=len(selected_symptoms) == 0
    )

if len(selected_symptoms) == 0:
    st.info("👆 Please select at least one symptom to begin analysis")

if analyze_button and len(selected_symptoms) > 0:
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    with st.spinner("🤖 AI is analyzing your symptoms..."):
        # Prepare patient data
        patient_info = {
            'age': age,
            'gender': gender,
            'conditions': existing_conditions,
            'duration': duration,
            'severity': severity
        }
        
        # Get AI analysis
        analysis_result = st.session_state.ai_model.analyze_symptoms(
            selected_symptoms,
            patient_info
        )
        
        # Save to history
        st.session_state.prediction_history.append({
            'symptoms': selected_symptoms,
            'analysis': analysis_result['analysis'],
            'timestamp': analysis_result['timestamp']
        })
    
    # Display results
    st.success("✅ Analysis Complete")
    
    # Symptoms summary
    st.markdown("**Reported Symptoms:**")
    st.info(", ".join([s.title() for s in selected_symptoms]))
    
    # Display severity indicator
    severity_color = "🟢" if severity <= 3 else "🟡" if severity <= 6 else "🔴"
    st.markdown(f"**Severity Level:** {severity_color} {severity}/10")
    st.markdown(f"**Duration:** {duration}")
    
    st.markdown("---")
    
    # AI Analysis
    st.markdown("### 🤖 AI Medical Analysis")
    
    analysis_container = st.container()
    with analysis_container:
        st.markdown(
            f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 10px; 
                        border-left: 5px solid #00b4d8;'>
                {analysis_result['analysis'].replace('\n', '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Warning section
    st.markdown("---")
    st.warning("""
    ⚠️ **Important Medical Disclaimer**
    
    This analysis is AI-generated and for informational purposes only. It should NOT replace 
    professional medical advice, diagnosis, or treatment. 
    
    **Please consult a healthcare provider if:**
    - Symptoms are severe or worsening
    - You have difficulty breathing or chest pain
    - Symptoms persist for more than a few days
    - You have concerns about your health
    """)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Save Report", use_container_width=True):
            st.success("Report saved to history!")
    
    with col2:
        if st.button("💊 Get Treatment Plan", use_container_width=True):
            st.switch_page("pages/2_💊_Treatment_Plans.py")
    
    with col3:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.rerun()

# History Section
if st.session_state.prediction_history:
    st.markdown("---")
    st.subheader("📜 Previous Analyses")
    
    for idx, record in enumerate(reversed(st.session_state.prediction_history[-5:])):
        with st.expander(f"Analysis {len(st.session_state.prediction_history) - idx} - {record['timestamp']}"):
            st.markdown(f"**Symptoms:** {', '.join([s.title() for s in record['symptoms']])}")
            st.markdown("**Analysis:**")
            st.write(record['analysis'])

# Sidebar
with st.sidebar:
    st.header("ℹ️ About Disease Prediction")
    st.markdown("""
    This AI-powered system analyzes your symptoms using IBM Granite's advanced 
    language model to provide potential condition assessments.
    
    **How it works:**
    1. Select your symptoms
    2. Provide patient information
    3. Get AI-powered analysis
    4. Receive recommendations
    
    **Remember:** Always consult healthcare professionals for accurate diagnosis.
    """)
    
    st.divider()
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.prediction_history = []
        st.rerun()