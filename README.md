# 🏥 HealthAI: Intelligent Healthcare Assistant

An AI-powered healthcare platform using IBM Granite models to provide intelligent medical assistance, disease prediction, personalized treatment plans, and health analytics.

## 🌟 Features

### 1. 💬 Patient Chat
- Interactive AI-powered chat for health questions
- Context-aware responses
- Medical information and guidance

### 2. 🩺 Disease Prediction
- Symptom analysis and assessment
- Potential condition identification
- Severity evaluation
- Recommended next steps

### 3. 💊 Treatment Plans
- Personalized treatment recommendations
- Evidence-based medical guidance
- Lifestyle and dietary advice
- Medication suggestions

### 4. 📊 Health Analytics
- Comprehensive health metrics visualization
- Trend analysis and insights
- AI-powered health assessment
- Interactive dashboards

## 🚀 Technology Stack

- **Frontend**: Streamlit
- **AI Model**: IBM Granite (via Hugging Face)
- **Visualization**: Plotly, Matplotlib
- **Data Processing**: Pandas, NumPy
- **Language**: Python 3.9+

## 📋 Prerequisites

- Python 3.9 or higher
- Hugging Face account and API token
- 8GB RAM minimum (16GB recommended)
- Git

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/healthai-assistant.git
cd healthai-assistant
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```bash
HUGGINGFACE_TOKEN=your_token_here
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
APP_TITLE=HealthAI: Intelligent Healthcare Assistant
```

Get your Hugging Face token:
1. Go to https://huggingface.co/
2. Sign up/Login
3. Go to Settings → Access Tokens
4. Create new token with "Read" permissions

## 🎮 Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
healthai-assistant/
├── app.py                          # Main application
├── config.py                       # Configuration settings
├── requirements.txt                # Dependencies
├── .env                           # Environment variables
├── pages/
│   ├── 1_🩺_Disease_Prediction.py
│   ├── 2_💊_Treatment_Plans.py
│   └── 3_📊_Health_Analytics.py
├── utils/
│   ├── ai_model.py                # AI model handler
│   ├── data_handler.py            # Data processing
│   └── visualizations.py          # Chart creation
└── data/
    └── sample_health_data.json
```

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io/
- Click "New app"
- Connect your GitHub repository
- Add secrets in Settings:
  - `HUGGINGFACE_TOKEN = "your_token"`
- Deploy!

### Option 2: Heroku

1. **Create Procfile**
```
web: sh setup.sh && streamlit run app.py
```

2. **Create setup.sh**
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. **Deploy**
```bash
heroku create your-app-name
git push heroku main
```

### Option 3: AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04)
2. **SSH into instance**
3. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

4. **Run with tmux**
```bash
tmux new -s healthai
streamlit run app.py --server.port 8501
```

### Option 4: Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

2. **Build and run**
```bash
docker build -t healthai .
docker run -p 8501:8501 healthai
```

## 🔒 Security & Privacy

- All AI processing uses secure APIs
- No patient data is stored permanently
- Session-based data management
- Environment variables for sensitive data
- HTTPS recommended for production

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for educational and informational purposes only.

- NOT a substitute for professional medical advice
- NOT for emergency medical situations
- Always consult healthcare professionals
- Do not make medical decisions based solely on AI output

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Issue: Model loading fails
**Solution**: Ensure you have a valid Hugging Face token in `.env`

### Issue: Import errors
**Solution**: Reinstall dependencies: `pip install -r requirements.txt --upgrade`

### Issue: Streamlit won't start
**Solution**: Check Python version (3.9+) and port availability

### Issue: AI responses are slow
**Solution**: Use smaller model or increase timeout settings

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation
- Review troubleshooting guide

## 🙏 Acknowledgments

- IBM for Granite models
- Hugging Face for model hosting
- Streamlit for the framework
- Open-source community

## 📊 Version History

- **v1.0.0** - Initial release
  - Patient chat functionality
  - Disease prediction
  - Treatment plans
  - Health analytics

---

**Made with ❤️ using IBM Granite AI**
