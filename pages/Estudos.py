import streamlit as st
from datetime import datetime, timedelta
import time
from datetime import datetime
import pandas as pd

st.title(":alarm_clock:Temporizador:alarm_clock:")

col1, col2, col3 = st.columns(3)
with col1:
    plot_hour = st.metric(label="hour", value=00)   
with col2:
    plot_minute = st.metric(label="Minuto", value=00)
with col3:
    plot_second = st.metric(label="Segundo", value=00)

def cronometro():
    second = 0
    minute = 0
    hour = 0
    while True:
        if second < 60:
            plot_second.metric(label="Segundo", value=second)
            second += 1
            time.sleep(1)
        elif minute < 60:
            second = 0
            minute += 1
            plot_second.metric(label="Segundo", value=second)
            plot_minute.metric(label="Minuto", value=minute)
            time.sleep(1)
        else:
            second = 0
            minute = 0
            hour += 1
            plot_second.metric(label="Segundo", value=second)
            plot_minute.metric(label="Minuto", value=minute)
            plot_hour.metric(label="Hour", value=hour)
            time.sleep(1)
            
def salvar_horario_inicio():
    horario_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("./horarios/horarios.csv", "a") as file:
        file.write(f'{horario_inicio},')
    

def salvar_horario_final():
    horario_final = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("./horarios/horarios.csv", 'a') as file:
        file.write(f'{horario_final}\n')  
    
         

with col1:                    
    if st.button("Estudando", type="primary"):
        salvar_horario_inicio()
        cronometro()
        
with col3:
    if st.button("Descansar"):
        salvar_horario_final()

st.divider()

#st.dataframe(df_estudo)

#lógica aqui

def horas():
    today = datetime.now().strftime('%Y-%m-%d')
    horas_hoje = 0
    horas_semanal = 0
    horas_mensal = 0
    horas_anual = 0

    # Carregar os dados do CSV
    dados_estudo_csv = pd.read_csv('./horarios/horarios.csv')

    # Criar o DataFrame
    df_estudo = pd.DataFrame(dados_estudo_csv)

    # Converter as colunas 'inicio' e 'termino' para datetime
    df_estudo['inicio'] = pd.to_datetime(df_estudo['inicio'])
    df_estudo['termino'] = pd.to_datetime(df_estudo['termino'])

    # Definir os intervalos de tempo
    start_semanal = datetime.now() - timedelta(days=7)
    start_mensal = datetime.now() - timedelta(days=30)
    start_anual = datetime.now() - timedelta(days=365)

    # Filtrar as linhas que correspondem ao dia atual
    df_hoje = df_estudo[df_estudo['inicio'].dt.strftime('%Y-%m-%d') == today]

    # Filtrar as linhas que correspondem aos últimos 7 dias
    df_semanal = df_estudo[df_estudo['inicio'] >= start_semanal]

    # Filtrar as linhas que correspondem aos últimos 30 dias
    df_mensal = df_estudo[df_estudo['inicio'] >= start_mensal]

    # Filtrar as linhas que correspondem aos últimos 365 dias
    df_anual = df_estudo[df_estudo['inicio'] >= start_anual]

    # Calcular o total de horas de estudo do dia
    for index, row in df_hoje.iterrows():
        horas_hoje += (row['termino'] - row['inicio']).total_seconds() / 3600

    # Calcular o total de horas de estudo da última semana
    for index, row in df_semanal.iterrows():
        horas_semanal += (row['termino'] - row['inicio']).total_seconds() / 3600

    # Calcular o total de horas de estudo do último mês
    for index, row in df_mensal.iterrows():
        horas_mensal += (row['termino'] - row['inicio']).total_seconds() / 3600

    # Calcular o total de horas de estudo do último ano
    for index, row in df_anual.iterrows():
        horas_anual += (row['termino'] - row['inicio']).total_seconds() / 3600

    return (horas_hoje, horas_semanal, horas_mensal, horas_anual, df_hoje, df_semanal, df_mensal, df_anual)
            


def delta():
    pass


horas_diaria = int(horas()[0])
delta_diario = 0

horas_semanais = int(horas()[1])
delta_semanal = 0

horas_mensais = int(horas()[2])
delta_mensal = 0

horas_anuais = int(horas()[3])
delta_anual = 0


st.metric(
    label='Hoje',
    value=f"{horas_diaria}h",
    delta=delta_diario,
)

# Função para calcular o tempo de estudo e descanso
def processar_dados(df):
    # Converter as colunas 'inicio' e 'termino' para datetime
    df['inicio'] = pd.to_datetime(df['inicio'])
    df['termino'] = pd.to_datetime(df['termino'])
    
    # Ordenar os dados por 'inicio'
    df = df.sort_values(by='inicio').reset_index(drop=True)
    
    # Calcular as horas de estudo e descanso
    df['horas_estudo'] = (df['termino'] - df['inicio']).dt.total_seconds() / 3600
    df['horas_descanso'] = df['inicio'].shift(-1) - df['termino']
    df['horas_descanso'] = df['horas_descanso'].dt.total_seconds() / 3600
    
    # Ajustar a última linha que não terá tempo de descanso calculado
    df.loc[df.index[-1], 'horas_descanso'] = 0

    return df

# Carregar os dados do CSV
df_estudo = pd.read_csv('./horarios/horarios.csv')

# Processar os dados para calcular tempo de estudo e descanso
df_processado = processar_dados(df_estudo)

# Imprimir o DataFrame processado para depuração
print(df_processado)

# Agrupar por dia e somar as horas de estudo e descanso
df_diario = df_processado.groupby(df_processado['inicio'].dt.date).agg({
    'horas_estudo': 'sum',
    'horas_descanso': 'sum'
}).reset_index()

# Renomear a coluna para 'dia' para facilitar a plotagem
df_diario.rename(columns={'inicio': 'dia'}, inplace=True)

# Imprimir o DataFrame diário para depuração
print(df_diario)

# Plotar os dados usando Streamlit
st.title('Horas de Estudo e Descanso Diárias')

# Plotar o gráfico de área
st.area_chart(df_diario.set_index('dia'))

col4, col5, col6, col7 = st.columns(4)

with col4:
    st.metric(
        label="Semanal", 
        value=f"{horas_semanais}h",
        delta=delta_semanal,
    )
    
with col5:
    st.metric(
        label="Mensal",
        value=f"{horas_mensais}h",
        delta=delta_mensal
    )
    
with col6:
    st.metric(
        label="Anual",
        value=f"{horas_anuais}h",
        delta=delta_anual        
    )

    