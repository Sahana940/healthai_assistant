import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class HealthDataHandler:
    """Handle patient health data and metrics"""
    
    @staticmethod
    def generate_sample_health_data(days: int = 30):
        """Generate sample health metrics for demonstration"""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        data = {
            'date': dates,
            'heart_rate': np.random.normal(75, 10, days).astype(int),
            'blood_pressure_systolic': np.random.normal(120, 15, days).astype(int),
            'blood_pressure_diastolic': np.random.normal(80, 10, days).astype(int),
            'blood_glucose': np.random.normal(95, 15, days).astype(int),
            'temperature': np.random.normal(98.6, 0.5, days).round(1),
            'oxygen_saturation': np.random.normal(98, 2, days).astype(int),
            'weight': np.random.normal(70, 2, days).round(1)
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def calculate_health_score(metrics: dict) -> int:
        """Calculate overall health score from metrics"""
        score = 100
        
        # Heart rate check (60-100 normal)
        hr = metrics.get('heart_rate', 75)
        if hr < 60 or hr > 100:
            score -= 10
        
        # Blood pressure check
        bp_sys = metrics.get('blood_pressure_systolic', 120)
        if bp_sys > 130 or bp_sys < 90:
            score -= 15
        
        # Blood glucose check (70-100 normal)
        glucose = metrics.get('blood_glucose', 95)
        if glucose > 100 or glucose < 70:
            score -= 10
        
        # Oxygen saturation check (>95 normal)
        o2 = metrics.get('oxygen_saturation', 98)
        if o2 < 95:
            score -= 20
        
        return max(score, 0)
    
    @staticmethod
    def get_metric_status(metric_name: str, value: float) -> tuple:
        """Get status and color for a metric"""
        ranges = {
            'heart_rate': {'low': 60, 'high': 100, 'unit': 'bpm'},
            'blood_pressure_systolic': {'low': 90, 'high': 120, 'unit': 'mmHg'},
            'blood_pressure_diastolic': {'low': 60, 'high': 80, 'unit': 'mmHg'},
            'blood_glucose': {'low': 70, 'high': 100, 'unit': 'mg/dL'},
            'temperature': {'low': 97.0, 'high': 99.5, 'unit': '°F'},
            'oxygen_saturation': {'low': 95, 'high': 100, 'unit': '%'},
        }
        
        if metric_name not in ranges:
            return "Unknown", "gray", ranges.get(metric_name, {}).get('unit', '')
        
        r = ranges[metric_name]
        unit = r['unit']
        
        if value < r['low']:
            return "Low", "orange", unit
        elif value > r['high']:
            return "High", "red", unit
        else:
            return "Normal", "green", unit
    
    @staticmethod
    def save_patient_data(patient_data: dict, filename: str = "data/patient_profile.json"):
        """Save patient data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(patient_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    @staticmethod
    def load_patient_data(filename: str = "data/patient_profile.json") -> dict:
        """Load patient data from JSON file"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    
    @staticmethod
    def format_symptoms_list(symptoms: list) -> str:
        """Format symptoms list for display"""
        if not symptoms:
            return "No symptoms recorded"
        return ", ".join([s.title() for s in symptoms])
    
    @staticmethod
    def get_risk_level(score: int) -> tuple:
        """Get risk level and color based on health score"""
        if score >= 80:
            return "Low Risk", "green"
        elif score >= 60:
            return "Moderate Risk", "orange"
        else:
            return "High Risk", "red"