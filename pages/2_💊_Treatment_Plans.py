import streamlit as st
import sys
sys.path.append('..')
from utils.ai_model import get_ai_model
from config import config

st.set_page_config(
    page_title="Treatment Plans - HealthAI",
    page_icon="💊",
    layout="wide"
)

# Initialize
if 'ai_model' not in st.session_state:
    st.session_state.ai_model = get_ai_model()

if 'treatment_history' not in st.session_state:
    st.session_state.treatment_history = []

if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {
        'age': 30,
        'gender': 'Not specified',
        'conditions': 'None'
    }

# Header
st.title("💊 Personalized Treatment Plans")
st.markdown("### AI-Generated Treatment Recommendations Based on Your Health Profile")

st.markdown("---")

# Input Section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🏥 Condition Information")
    
    # Condition input method
    input_method = st.radio(
        "Choose input method:",
        ["Select from Common Conditions", "Enter Custom Condition"],
        horizontal=True
    )
    
    if input_method == "Select from Common Conditions":
        common_conditions = [
            "Common Cold",
            "Seasonal Flu",
            "Migraine",
            "Type 2 Diabetes",
            "Hypertension (High Blood Pressure)",
            "Anxiety Disorder",
            "Depression",
            "Gastritis",
            "Allergic Rhinitis",
            "Asthma",
            "Back Pain",
            "Insomnia",
            "Acid Reflux (GERD)",
            "Arthritis",
            "Sinusitis"
        ]
        
        condition = st.selectbox(
            "Select Condition:",
            common_conditions
        )
    else:
        condition = st.text_input(
            "Enter Condition:",
            placeholder="e.g., Chronic Fatigue Syndrome"
        )
    
    # Additional details
    st.markdown("---")
    
    symptom_severity = st.select_slider(
        "Current Symptom Severity:",
        options=["Mild", "Moderate", "Severe", "Very Severe"],
        value="Moderate"
    )
    
    treatment_goals = st.multiselect(
        "Treatment Goals:",
        ["Pain Relief", "Symptom Management", "Long-term Health", 
         "Quality of Life", "Prevent Complications", "Cure/Recovery"],
        default=["Symptom Management"]
    )
    
    additional_notes = st.text_area(
        "Additional Information:",
        placeholder="Any specific concerns, allergies, or preferences...",
        help="Provide context that might help customize your treatment plan"
    )

with col2:
    st.subheader("👤 Patient Profile")
    
    age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state.patient_data.get('age', 30))
    gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    
    weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    
    # Calculate BMI
    if height > 0:
        bmi = weight / ((height / 100) ** 2)
        bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
        st.metric("BMI", f"{bmi:.1f}", f"{bmi_category}")
    
    existing_conditions = st.text_area(
        "Other Health Conditions:",
        value=st.session_state.patient_data.get('conditions', ''),
        placeholder="List any other conditions"
    )
    
    current_medications = st.text_area(
        "Current Medications:",
        placeholder="List medications you're taking"
    )
    
    allergies = st.text_input(
        "Known Allergies:",
        placeholder="e.g., Penicillin, Sulfa drugs"
    )

st.markdown("---")

# Generate Treatment Plan Button
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate_button = st.button(
        "🎯 Generate Treatment Plan",
        type="primary",
        use_container_width=True,
        disabled=not condition
    )

if not condition:
    st.info("👆 Please select or enter a condition to generate a treatment plan")

if generate_button and condition:
    st.markdown("---")
    st.subheader("📋 Your Personalized Treatment Plan")
    
    with st.spinner("🤖 AI is creating your personalized treatment plan..."):
        # Prepare patient data
        patient_info = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'bmi': f"{bmi:.1f}" if height > 0 else "N/A",
            'conditions': existing_conditions,
            'medications': current_medications,
            'allergies': allergies,
            'severity': symptom_severity,
            'goals': ", ".join(treatment_goals),
            'notes': additional_notes
        }
        
        # Generate treatment plan
        treatment_result = st.session_state.ai_model.generate_treatment_plan(
            condition,
            patient_info
        )
        
        # Save to history
        st.session_state.treatment_history.append({
            'condition': condition,
            'plan': treatment_result['plan'],
            'timestamp': treatment_result['timestamp'],
            'patient_info': patient_info
        })
    
    st.success("✅ Treatment Plan Generated Successfully")
    
    # Display condition summary
    st.markdown("### 🏥 Condition Summary")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("Condition", condition)
    with summary_col2:
        st.metric("Severity", symptom_severity)
    with summary_col3:
        st.metric("Patient Age", f"{age} years")
    
    st.markdown("---")
    
    # Display treatment plan
    st.markdown("### 💊 Comprehensive Treatment Plan")
    
    plan_container = st.container()
    with plan_container:
        # Format and display the plan
        st.markdown(
            f"""
            <div style='background-color: #f8f9fa; padding: 25px; border-radius: 10px; 
                        border-left: 5px solid #00b4d8; line-height: 1.8;'>
                {treatment_result['plan'].replace('\n', '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Key Highlights
    st.markdown("### 🌟 Key Highlights")
    
    highlight_col1, highlight_col2 = st.columns(2)
    
    with highlight_col1:
        st.info("""
        **✓ Treatment Goals**
        
        """ + "\n- ".join(treatment_goals))
    
    with highlight_col2:
        st.warning("""
        **⚠️ Important Reminders**
        
        - Follow prescribed dosages
        - Monitor for side effects
        - Schedule follow-up appointments
        - Report unusual symptoms
        """)
    
    # Medical Disclaimer
    st.markdown("---")
    st.error("""
    **🚨 CRITICAL MEDICAL DISCLAIMER**
    
    This treatment plan is AI-generated for informational and educational purposes ONLY. 
    
    **DO NOT start any treatment without consulting a licensed healthcare provider.**
    
    - This is NOT a prescription
    - This does NOT replace professional medical advice
    - Always verify with your doctor before taking medications
    - Individual circumstances may require different approaches
    
    **Seek immediate medical attention if you experience severe or worsening symptoms.**
    """)
    
    # Action Buttons
    st.markdown("---")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("📥 Download Plan", use_container_width=True):
            st.success("Download feature coming soon!")
    
    with action_col2:
        if st.button("📧 Email Plan", use_container_width=True):
            st.success("Email feature coming soon!")
    
    with action_col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/3_📊_Health_Analytics.py")
    
    with action_col4:
        if st.button("🔄 New Plan", use_container_width=True):
            st.rerun()

# Treatment History
if st.session_state.treatment_history:
    st.markdown("---")
    st.subheader("📜 Treatment Plan History")
    
    for idx, record in enumerate(reversed(st.session_state.treatment_history[-5:])):
        with st.expander(f"Plan {len(st.session_state.treatment_history) - idx}: {record['condition']} - {record['timestamp']}"):
            st.markdown(f"**Condition:** {record['condition']}")
            st.markdown(f"**Patient Age:** {record['patient_info']['age']} years")
            st.markdown(f"**Severity:** {record['patient_info']['severity']}")
            st.markdown("---")
            st.markdown("**Treatment Plan:**")
            st.write(record['plan'])

# Sidebar
with st.sidebar:
    st.header("💊 About Treatment Plans")
    st.markdown("""
    Our AI-powered system generates personalized treatment plans based on:
    
    - Your health condition
    - Patient demographics
    - Existing health issues
    - Current medications
    - Treatment goals
    
    **The AI considers:**
    - Evidence-based medicine
    - Clinical guidelines
    - Individual patient factors
    - Drug interactions
    - Lifestyle modifications
    """)
    
    st.divider()
    
    st.markdown("### 📚 Resources")
    st.markdown("""
    - [Medical Guidelines](https://www.who.int)
    - [Drug Information](https://www.drugs.com)
    - [Find a Doctor](https://www.healthgrades.com)
    """)
    
    st.divider()
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.treatment_history = []
        st.rerun()