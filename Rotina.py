import streamlit as st
import pandas as pd
from datetime import datetime
import time

def obter_saudacao():
    hora_atual = datetime.now().hour

    if 6 <= hora_atual < 12:
        return "Bom dia"
    elif 12 <= hora_atual < 18:
        return "Boa tarde"
    elif 18 <= hora_atual < 24:
        return "Boa noite"
    else:
        return "Boa madrugada"

# Obtenha a data e hora atual
agora = datetime.now()

# Extraia os componentes da data e hora
dia = agora.day
ano = agora.year
mês = agora.month

sem = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")

# Crie uma instância de datetime com os componentes de data
data_atual = datetime(ano, mês, dia)
data_ITA = datetime(2024, 10, 8)
# Verifique que dia é hoje de acordo com o padrão de data em inglês ex:(2021/05/10)
num = data_atual.weekday()
dia_semanal = sem[num]

# Carrega os dados do arquivo CSV
data_day = pd.read_csv(f'./csvs/{dia_semanal.lower()}.csv', encoding='utf-8')
plot_hora = st.empty()

saudacao = obter_saudacao()

st.title(f"{saudacao}, Juan! :sunglasses:")
st.subheader(f':face_with_cowboy_hat: {dia_semanal} :face_with_cowboy_hat:')


# Mostra os dados do DataFrame do dia
st.write(data_day)

st.divider()

#Sonhos
st.title('Sonhos:stars:')
st.subheader(f':date: Faltam {(data_ITA - data_atual).days} dias para o ITA :first_place_medal:')

st.divider()

#Rotina Domingo
st.title('Rotina Domingo')
st.dataframe(pd.read_csv('./csvs/domingo.csv', encoding='utf-8'))

st.divider()

#Rotina Segunda
st.title('Rotina Segunda')
st.dataframe(pd.read_csv('./csvs/segunda.csv', encoding='utf-8'))

st.divider()

#Rotina Terça
st.title('Rotina Terça')
st.dataframe(pd.read_csv('./csvs/terça.csv', encoding='utf-8'))

st.divider()

#Rotina Quarta
st.title('Rotina Quarta')
st.dataframe(pd.read_csv('./csvs/quarta.csv', encoding='utf-8'))

st.divider()

#Rotina Quinta
st.title('Rotina Quinta')
st.dataframe(pd.read_csv('./csvs/quinta.csv', encoding='utf-8'))

st.divider()

#Rotina Sexta
st.title('Rotina Sexta')
st.dataframe(pd.read_csv('./csvs/sexta.csv', encoding='utf-8'))

st.divider()

#Rotina Sábado
st.title('Rotina Sábado')
st.dataframe(pd.read_csv('./csvs/sábado.csv', encoding='utf-8'))


while True:
    plot_hora.title(f":alarm_clock:{(datetime.now()).strftime('%H:%M')}")
    time.sleep(0.1)
