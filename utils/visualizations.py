import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

class HealthVisualizations:
    """Create health data visualizations"""
    
    @staticmethod
    def create_metric_trend_chart(df: pd.DataFrame, metric: str, title: str):
        """Create line chart for metric trends"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df[metric],
            mode='lines+markers',
            name=title,
            line=dict(color='#00b4d8', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title=title,
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_multi_metric_dashboard(df: pd.DataFrame):
        """Create dashboard with multiple metrics"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Heart Rate', 'Blood Pressure', 'Blood Glucose', 'Oxygen Saturation'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Heart Rate
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['heart_rate'], 
                      name='Heart Rate', line=dict(color='#ef476f')),
            row=1, col=1
        )
        
        # Blood Pressure
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['blood_pressure_systolic'], 
                      name='Systolic', line=dict(color='#06ffa5')),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['blood_pressure_diastolic'], 
                      name='Diastolic', line=dict(color='#118ab2')),
            row=1, col=2
        )
        
        # Blood Glucose
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['blood_glucose'], 
                      name='Glucose', line=dict(color='#ffd60a')),
            row=2, col=1
        )
        
        # Oxygen Saturation
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['oxygen_saturation'], 
                      name='O2 Sat', line=dict(color='#06ffa5')),
            row=2, col=2
        )
        
        fig.update_layout(
            height=700,
            showlegend=True,
            template='plotly_white',
            title_text="Health Metrics Dashboard",
            title_font_size=20
        )
        
        return fig
    
    @staticmethod
    def create_health_score_gauge(score: int):
        """Create gauge chart for health score"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Health Score", 'font': {'size': 24}},
            delta={'reference': 80, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 60], 'color': '#ffcccb'},
                    {'range': [60, 80], 'color': '#ffffcc'},
                    {'range': [80, 100], 'color': '#90EE90'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig
    
    @staticmethod
    def create_metric_distribution(df: pd.DataFrame, metric: str, title: str):
        """Create histogram for metric distribution"""
        fig = go.Figure(data=[go.Histogram(
            x=df[metric],
            nbinsx=20,
            marker_color='#00b4d8',
            opacity=0.7
        )])
        
        fig.update_layout(
            title=f"{title} Distribution",
            xaxis_title=title,
            yaxis_title="Frequency",
            template='plotly_white',
            height=350
        )
        
        return fig
    
    @staticmethod
    def create_correlation_heatmap(df: pd.DataFrame):
        """Create correlation heatmap for health metrics"""
        numeric_cols = ['heart_rate', 'blood_pressure_systolic', 
                       'blood_pressure_diastolic', 'blood_glucose', 
                       'temperature', 'oxygen_saturation']
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Health Metrics Correlation",
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_bp_scatter(df: pd.DataFrame):
        """Create scatter plot for blood pressure"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['blood_pressure_systolic'],
            y=df['blood_pressure_diastolic'],
            mode='markers',
            marker=dict(
                size=10,
                color=df.index,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Day")
            ),
            text=df['date'].dt.strftime('%Y-%m-%d'),
            hovertemplate='<b>Date:</b> %{text}<br>' +
                         '<b>Systolic:</b> %{x}<br>' +
                         '<b>Diastolic:</b> %{y}<br>'
        ))
        
        # Add normal range box
        fig.add_shape(
            type="rect",
            x0=90, y0=60, x1=120, y1=80,
            line=dict(color="green", width=2, dash="dash"),
            fillcolor="lightgreen",
            opacity=0.2
        )
        
        fig.update_layout(
            title="Blood Pressure Scatter Plot",
            xaxis_title="Systolic (mmHg)",
            yaxis_title="Diastolic (mmHg)",
            template='plotly_white',
            height=450
        )
        
        return fig