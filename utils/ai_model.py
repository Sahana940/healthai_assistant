import streamlit as st
from huggingface_hub import InferenceClient
from config import config
import time
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

client = InferenceClient(
    model=MODEL_NAME,
    token=HF_TOKEN
)

def generate_response(user_input):
    response = client.text_generation(
        user_input,
        max_new_tokens=256
    )
    return response

class GraniteHealthAI:
    """IBM Granite AI Model Handler for Healthcare"""
    
    def __init__(self):
        self.client = None
        self.model_name = config.MODEL_NAME
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Hugging Face Inference Client"""
        try:
            if config.HUGGINGFACE_TOKEN:
                self.client = InferenceClient(
                    model=self.model_name,
                    token=config.HUGGINGFACE_TOKEN
                )
            else:
                st.error("⚠️ Hugging Face token not found. Please add it to .env file")
        except Exception as e:
            st.error(f"Failed to initialize AI model: {str(e)}")
    
    def generate_response(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate AI response using Granite model"""
        try:
            if not self.client:
                return "AI model not initialized. Please check your Hugging Face token."
            
            response = self.client.text_generation(
                prompt,
                max_new_tokens=max_tokens,
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P,
                repetition_penalty=1.1,
                return_full_text=False
            )
            
            return response.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def analyze_symptoms(self, symptoms: list, patient_data: dict = None) -> dict:
        """Analyze symptoms and predict potential conditions"""
        
        symptoms_text = ", ".join(symptoms)
        
        prompt = f"""You are a medical AI assistant. Analyze the following symptoms and provide a structured medical assessment.

Symptoms: {symptoms_text}

Provide your analysis in the following format:
1. Possible Conditions (list 3-4 most likely conditions)
2. Severity Assessment (Low/Moderate/High)
3. Recommended Actions
4. When to Seek Immediate Care

Keep your response professional, clear, and concise. Use bullet points where appropriate."""

        if patient_data:
            prompt += f"\n\nPatient Information:\nAge: {patient_data.get('age', 'N/A')}\nGender: {patient_data.get('gender', 'N/A')}"
        
        response = self.generate_response(prompt, max_tokens=600)
        
        return {
            "analysis": response,
            "symptoms": symptoms,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_treatment_plan(self, condition: str, patient_data: dict = None) -> dict:
        """Generate personalized treatment plan"""
        
        prompt = f"""You are a medical AI assistant. Create a comprehensive treatment plan for: {condition}

Provide a structured treatment plan including:
1. Medications and Dosages
2. Lifestyle Modifications
3. Dietary Recommendations
4. Exercise Guidelines
5. Monitoring Requirements
6. Follow-up Schedule
7. Warning Signs to Watch For

Make recommendations evidence-based and patient-friendly."""

        if patient_data:
            prompt += f"\n\nPatient Profile:\nAge: {patient_data.get('age', 'N/A')}\nGender: {patient_data.get('gender', 'N/A')}\nExisting Conditions: {patient_data.get('conditions', 'None')}"
        
        response = self.generate_response(prompt, max_tokens=800)
        
        return {
            "plan": response,
            "condition": condition,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def chat_response(self, user_message: str, chat_history: list = None) -> str:
        """Generate conversational health advice"""
        
        context = ""
        if chat_history:
            context = "\n".join([f"User: {msg['user']}\nAssistant: {msg['assistant']}" 
                               for msg in chat_history[-3:]])  # Last 3 exchanges
        
        prompt = f"""You are a helpful medical AI assistant. Provide accurate, empathetic health information.

{context}

User: {user_message}
Assistant:"""
        
        return self.generate_response(prompt, max_tokens=400)
    
    def analyze_health_trends(self, metrics_data: dict) -> str:
        """Analyze health metrics and provide insights"""
        
        prompt = f"""You are a medical data analyst. Analyze the following health metrics and provide insights:

Health Metrics Summary:
{self._format_metrics(metrics_data)}

Provide:
1. Key Observations
2. Concerning Trends (if any)
3. Positive Trends
4. Recommendations for Improvement

Be specific and actionable."""
        
        return self.generate_response(prompt, max_tokens=500)
    
    def _format_metrics(self, metrics: dict) -> str:
        """Format metrics for prompt"""
        formatted = []
        for key, value in metrics.items():
            if isinstance(value, list):
                formatted.append(f"{key}: Average {sum(value)/len(value):.1f}, Range {min(value)}-{max(value)}")
            else:
                formatted.append(f"{key}: {value}")
        return "\n".join(formatted)

# Initialize model (singleton pattern)
@st.cache_resource
def get_ai_model():
    """Get or create AI model instance"""
    return GraniteHealthAI()