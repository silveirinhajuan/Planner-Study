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
data = pd.read_csv('./csvs/segunda.csv', encoding='utf-8')
plot_hora = st.empty()

saudacao = obter_saudacao()

st.title(f"{saudacao}, Juan! :sunglasses:")
st.subheader(f'{dia_semanal} :stars:')


# Mostra os dados do DataFrame
st.write(data)

st.divider()

#Sonhos
st.title('Sonhos:stars:')
st.subheader(f':date: Faltam {(data_ITA - data_atual).days} dias para o ITA :first_place_medal:')

while True:
    plot_hora.title(f":alarm_clock:{(datetime.now()).strftime('%H:%M')}")
    time.sleep(0.1)
