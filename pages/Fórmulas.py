import streamlit as st
import pandas as pd

def adicionar_formula(titulo, formula):
    with open('./formulas.csv', 'a') as file:
        file.write(f"{titulo},{formula}\n")    

def remover_formula(id):
    # Lê o arquivo CSV
    df = pd.read_csv('./formulas.csv')
    # Remove a linha correspondente ao ID
    df = df.drop(index=id)
    # Reescreve o arquivo CSV sem a linha removida
    df.to_csv('./formulas.csv', index=False, encoding='utf-8')

st.title(':nerd_face: Fórmulas :nerd_face:')
st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.form("Adicione Fórmulas"):
        titulo = st.text_input('Titulo')
        formula = st.text_input('Fórmula em LaTeX')
        # Every form must have a submit button.
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            adicionar_formula(titulo, formula)
            st.success(f"Fórmula '{titulo}' adicionada com sucesso!")
            st.balloons()

with col2:
    # Carrega o arquivo CSV
    df = pd.read_csv('./formulas.csv')
    # Exibe as fórmulas em um selectbox
    formula_selecionada = st.selectbox('Selecione a fórmula para excluir:', df['titulo'].tolist())
    # Obtém o ID da fórmula selecionada
    id_selecionado = df[df['titulo'] == formula_selecionada].index[0]
    # Botão para excluir a fórmula selecionada
    if st.button('Excluir fórmula'):
        remover_formula(id_selecionado)
        st.success(f"Fórmula '{formula_selecionada}' excluída com sucesso!")


            