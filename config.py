import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Hugging Face
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    MODEL_NAME = os.getenv("MODEL_NAME", "ibm-granite/granite-3b-code-instruct")
    
    # App Settings
    APP_TITLE = os.getenv("APP_TITLE", "HealthAI: Intelligent Healthcare Assistant")
    APP_ICON = os.getenv("APP_ICON", "🏥")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"
    
    # Model Parameters
    MAX_LENGTH = int(os.getenv("MAX_LENGTH", "512"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P = float(os.getenv("TOP_P", "0.9"))
    
    # Health Conditions Database
    COMMON_CONDITIONS = {
        "cold": ["runny nose", "sneezing", "sore throat", "cough"],
        "flu": ["fever", "body aches", "fatigue", "headache"],
        "migraine": ["severe headache", "nausea", "light sensitivity"],
        "allergies": ["sneezing", "itchy eyes", "runny nose"],
        "diabetes": ["increased thirst", "frequent urination", "fatigue"],
        "hypertension": ["headache", "dizziness", "chest pain"],
        "gastritis": ["stomach pain", "nausea", "bloating"],
        "anxiety": ["restlessness", "rapid heartbeat", "worry"],
        "depression": ["sadness", "fatigue", "loss of interest"],
    }
    
    # Treatment Guidelines
    TREATMENT_TEMPLATES = {
        "medications": "Recommended medications and dosages",
        "lifestyle": "Lifestyle modifications and habits",
        "diet": "Dietary recommendations",
        "exercise": "Physical activity suggestions",
        "monitoring": "Health metrics to track",
        "follow_up": "Follow-up schedule"
    }

config = Config()