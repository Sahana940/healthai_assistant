import streamlit as st
from huggingface_hub import InferenceClient
from config import config
import time
import traceback


class GraniteHealthAI:
    """IBM Granite AI Model Handler for Healthcare"""

    def __init__(self):
        self.client = None
        self.model_name = config.MODEL_NAME or "Qwen/Qwen2.5-7B-Instruct"
        self._initialize_client()

    def _initialize_client(self):
        try:
            if not config.HUGGINGFACE_TOKEN:
                st.error("❌ Hugging Face Token missing in .env")
                return

            self.client = InferenceClient(
                model=self.model_name,
                token=config.HUGGINGFACE_TOKEN
            )
            st.success(f"✅ Model Ready: {self.model_name}")

        except Exception as e:
            st.error(f"🔥 AI Initialization Failed: {str(e)}")
            st.code(traceback.format_exc())

    def generate_response(self, prompt: str, max_tokens: int = 512) -> str:
        """Chat response using Hugging Face Granite model"""
        try:
            if not self.client:
                return "❌ Model not initialized. Verify API token/model name."

            messages = [
                {"role": "system", "content": "You are a professional healthcare assistant."},
                {"role": "user", "content": prompt}
            ]

            response = self.client.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=float(config.TEMPERATURE),
                top_p=float(config.TOP_P),
            )

            return response.choices[0].message["content"].strip()

        except Exception as e:
            st.error(f"⚠️ Error generating response:\n{e}")
            st.code(traceback.format_exc())
            return f"Error generating response: {e}"

    def analyze_symptoms(self, symptoms: list, patient_data: dict = None) -> dict:
        symptoms_text = ", ".join(symptoms)
        prompt = f"""
Analyze symptoms and provide information:

✅ Likely medical conditions (Top 3-5)
✅ Severity level (Low/Moderate/High)
✅ Suggested first-aid and precautions
✅ When to seek urgent care

Symptoms: {symptoms_text}
"""
        if patient_data:
            prompt += f"\nPatient: Age {patient_data.get('age')}, Gender: {patient_data.get('gender')}"

        return {
            "analysis": self.generate_response(prompt, max_tokens=700),
            "symptoms": symptoms,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def generate_treatment_plan(self, condition: str, patient_data: dict = None) -> dict:
        prompt = f"""
Provide a medical treatment plan for: {condition}

Include:

✅ Medication suggestions (general OTC, if applicable)
✅ Diet and lifestyle recommendations
✅ Follow-up advice
✅ Warning symptoms to monitor
"""
        if patient_data:
            prompt += f"\nPatient: Age {patient_data.get('age')} Gender: {patient_data.get('gender')}"

        return {
            "plan": self.generate_response(prompt, max_tokens=700),
            "condition": condition,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def chat_response(self, user_message: str, chat_history: list = None) -> str:
        history = ""
        if chat_history:
            history = "\n".join(
                [f"User: {msg['user']}\nAssistant: {msg['assistant']}"
                 for msg in chat_history[-3:]]
            )

        prompt = f"""
{history}

User: {user_message}
"""
        return self.generate_response(prompt, max_tokens=450)

    def analyze_health_trends(self, metrics_data: dict) -> str:
        prompt = f"""
Analyze these health metrics:
{self._format_metrics(metrics_data)}

Provide:

✅ Positive health trends
✅ Concerning health risks
✅ Actionable health improvement suggestions
"""
        return self.generate_response(prompt, max_tokens=550)

    def _format_metrics(self, metrics: dict) -> str:
        formatted = []
        for key, value in metrics.items():
            if isinstance(value, list) and value:
                formatted.append(f"{key}: Avg {sum(value)/len(value):.1f} | Range {min(value)}–{max(value)}")
            else:
                formatted.append(f"{key}: {value}")
        return "\n".join(formatted)


@st.cache_resource
def get_ai_model():
    return GraniteHealthAI()
