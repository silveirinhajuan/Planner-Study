import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

class EstudosTracker:
    def __init__(self, db_path='estudos_tracker.db'):
        """Initialize database connection and create tables if not exist"""
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """Create database tables for tracking study sessions"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME,
                end_time DATETIME,
                subject TEXT,
                performance INTEGER,
                session_duration REAL,
                idle_time REAL
            )
        ''')
        self.conn.commit()

    def insert_study_session(self, start_time, end_time, subject, performance, idle_time):
        """Insert a new study session into the database"""
        duration = (end_time - start_time).total_seconds() / 3600  # duration in hours
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO study_sessions 
            (start_time, end_time, subject, performance, session_duration, idle_time) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (start_time, end_time, subject, performance, duration, idle_time))
        self.conn.commit()

    def get_study_sessions(self):
        """Retrieve all study sessions"""
        query = "SELECT * FROM study_sessions ORDER BY start_time"
        return pd.read_sql_query(query, self.conn)

    def calculate_metrics(self):
        """Generate comprehensive study metrics"""
        df = self.get_study_sessions()
        
        metrics = {
            'total_study_time': df['session_duration'].sum(),
            'total_sessions': len(df),
            'avg_daily_study_time': df.groupby(pd.to_datetime(df['start_time']).dt.date)['session_duration'].sum().mean(),
            'subject_time': df.groupby('subject')['session_duration'].sum(),
            'avg_performance_by_subject': df.groupby('subject')['performance'].mean(),
            'avg_performance': df['performance'].mean(),
            'consecutive_study_days': self.calculate_consecutive_study_days(df)
        }
        
        return metrics

    def calculate_consecutive_study_days(self, df):
        """Calculate maximum number of consecutive study days"""
        df['date'] = pd.to_datetime(df['start_time']).dt.date
        unique_dates = df['date'].unique()
        unique_dates.sort()
        
        max_consecutive = 0
        current_consecutive = 1
        
        for i in range(1, len(unique_dates)):
            if (unique_dates[i] - unique_dates[i-1]).days == 1:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1
        
        return max_consecutive

def main():
    st.title('🎓 Estudos ITA Tracker')
    tracker = EstudosTracker()

    # Sidebar for navigation
    menu = ["Registrar Sessão", "Métricas e Análises", "Histórico de Sessões"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Registrar Sessão":
        st.header("Registrar Nova Sessão de Estudo")
        
        # Study Session Input
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Hora de Início")
            subject = st.selectbox("Matéria", 
                ["Matemática", "Física", "Química", "Português", "Inglês", "Redação", "Correções", "Simulado"])
        
        with col2:
            end_time = st.time_input("Hora de Término", datetime.now().time())
            performance = st.slider("Rendimento da Sessão", 1, 10, 5)
        
        idle_time_input = st.number_input("Tempo Ocioso (minutos)", min_value=0.0, step=5.0)
        
        if st.button("Salvar Sessão"):
            # Combine date with time inputs
            today = datetime.now().date()
            start_datetime = datetime.combine(today, start_time)
            end_datetime = datetime.combine(today, end_time)
            
            # Handle time crossing midnight
            if end_datetime < start_datetime:
                end_datetime += timedelta(days=1)
            
            tracker.insert_study_session(
                start_datetime, 
                end_datetime, 
                subject, 
                performance, 
                idle_time_input/60  # convert to hours
            )
            st.success("Sessão registrada com sucesso!")

    elif choice == "Métricas e Análises":
        st.header("Análise de Desempenho")
        
        metrics = tracker.calculate_metrics()
        
        # Metrics Display
        col1, col2, col3 = st.columns(3)
        col1.metric("Tempo Total de Estudo", f"{metrics['total_study_time']:.2f} horas")
        col2.metric("Média Diária", f"{metrics['avg_daily_study_time']:.2f} horas")
        col3.metric("Dias Consecutivos", metrics['consecutive_study_days'])
        
        # Subject Time Pie Chart
        st.subheader("Tempo por Matéria")
        fig_subject_time = px.pie(
            values=metrics['subject_time'], 
            names=metrics['subject_time'].index, 
            title="Distribuição de Tempo de Estudo"
        )
        st.plotly_chart(fig_subject_time)
        
        # Performance Bar Chart
        st.subheader("Rendimento por Matéria")
        fig_performance = px.bar(
            x=metrics['avg_performance_by_subject'].index, 
            y=metrics['avg_performance_by_subject'].values,
            labels={'x': 'Matéria', 'y': 'Rendimento Médio'},
            title="Rendimento Médio por Matéria"
        )
        st.plotly_chart(fig_performance)

    elif choice == "Histórico de Sessões":
        st.header("Histórico Completo de Sessões")
        df = tracker.get_study_sessions()
        st.dataframe(df)

if __name__ == "__main__":
    main()