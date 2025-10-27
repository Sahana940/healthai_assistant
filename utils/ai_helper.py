import os

try:
    import openai  # optional if using OpenAI API
except ImportError:
    openai = None

from config import Config


    
class GraniteAI:
    """
    Helper class to interact with IBM Granite AI model.
    """

    def __init__(self):
        # Load API token from config
        self.api_token = Config.HUGGINGFACE_TOKEN
        self.model_name = Config.MODEL_NAME

        # Optional: initialize client if needed
        # Example using Hugging Face API:
        # self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def analyze_health_metrics(self, metrics_summary: dict) -> str:
        """
        Analyze health metrics and return insights.
        For now, returns dummy insights; later you can integrate API call.
        """
        insights = []

        hr = metrics_summary.get("heart_rate", 70)
        if hr < 60:
            insights.append("Heart rate is slightly low. Consider light physical activity.")
        elif hr > 100:
            insights.append("Heart rate is high. Monitor and consult a doctor if persistent.")
        else:
            insights.append("Heart rate is normal.")

        glucose = metrics_summary.get("blood_glucose", 90)
        if glucose > 125:
            insights.append("Blood glucose is high. Maintain a balanced diet.")
        elif glucose < 70:
            insights.append("Blood glucose is low. Eat regular meals.")
        else:
            insights.append("Blood glucose is within normal range.")

        bp_sys = metrics_summary.get("blood_pressure_systolic", 120)
        bp_dia = metrics_summary.get("blood_pressure_diastolic", 80)
        if bp_sys >= 140 or bp_dia >= 90:
            insights.append("Blood pressure is elevated. Reduce salt and stress.")
        else:
            insights.append("Blood pressure is normal.")

        return "\n".join(insights)
    def generate_response(self, user_input, context=None):
        # This is likely what you want instead of chat_response
        return "AI reply"
    

    # Optional: Add method to call IBM Granite API
    # def call_ibm_granite(self, prompt: str) -> str:
    #     url = f"https://api-inference.huggingface.co/models/{self.model_name}"
    #     payload = {"inputs": prompt}
    #     response = requests.post(url, headers=self.headers, json=payload)
    #     return response.json()[0]["generated_text"]
