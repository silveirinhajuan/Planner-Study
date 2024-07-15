import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import time
import random

import streamlit as st

st.set_page_config(
    page_title="Rotina Cavalesca",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# App de rotinas. feito de *juan* para *juan*!"
    }
)

# Obtenha a data e hora atual
agora = datetime.now()
diferenca = timedelta(hours=-3)
fuso_horario = timezone(diferenca)
agora = agora.astimezone(fuso_horario)
# Extraia os componentes da data e hora
dia = agora.day
ano = agora.year
mês = agora.month

def obter_saudacao():
    hora_atual = (datetime.now().astimezone(fuso_horario)).hour

    if 6 <= hora_atual < 12:
        return "Bom dia"
    elif 12 <= hora_atual < 18:
        return "Boa tarde"
    elif 18 <= hora_atual < 24:
        return "Boa noite"
    else:
        return "Boa madrugada"

sem = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")

# Crie uma instância de datetime com os componentes de data
data_atual = datetime(ano, mês, dia)
data_ITA = datetime(2024, 10, 13)
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

st.title(':stars: Sonhos :sparkles:')
#Sonhos
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

# Exibir Fórmula Aleatória
st.sidebar.subheader('Fórmula Aleatória')
if st.sidebar.button('Exibir'):
    formulas = pd.read_csv('./formulas.csv')
    random_formula = random.choice(formulas['formula'].tolist())
    st.sidebar.latex(random_formula)

while True:
    plot_hora.title(f":alarm_clock:{((datetime.now()).astimezone(fuso_horario)).strftime('%H:%M')}")
    time.sleep(0.1)
