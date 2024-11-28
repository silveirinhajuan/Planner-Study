import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Verificar se o arquivo existe, se não, cria com cabeçalho
def inicializar_csv():
    if not os.path.exists('./formulas.csv'):
        with open('./formulas.csv', 'w', encoding="utf-8") as file:
            file.write("id,question,answer,date_added,next_appearance,tags\n")

def adicionar_formula(question, answer, tags):
    # Lê o arquivo CSV
    df = pd.read_csv('./formulas.csv')
    
    # Gera um novo ID automaticamente
    novo_id = df['id'].max() + 1 if len(df) > 0 else 1
    
    # Adiciona a nova fórmula
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    next_appearance = (datetime.now() + pd.Timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    nova_linha = f"{novo_id},{question},{answer},{date_added},{next_appearance},{tags}\n"
    
    with open('./formulas.csv', 'a', encoding="utf-8") as file:
        file.write(nova_linha)
    return True

def remover_formula(question):
    # Lê o arquivo CSV
    df = pd.read_csv('./formulas.csv')
    
    # Remove a linha correspondente à pergunta
    df = df[df['question'] != question]
    
    # Reescreve o arquivo CSV
    df.to_csv('./formulas.csv', index=False, encoding='utf-8')

# Inicializa o CSV se não existir
inicializar_csv()

st.title(':nerd_face: Fórmulas :nerd_face:')
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Adicionar Fórmula")
    with st.form("Adicione Fórmulas"):
        question = st.text_input('Título', help="Nome único para identificar a fórmula")
        answer = st.text_input('Fórmula em LaTeX', help="Digite a fórmula no formato LaTeX")
        tags = st.text_input('Tags', help="Adicione tags separadas por vírgulas")
        submitted = st.form_submit_button("Adicionar")
        
        if submitted:
            # Validações básicas
            if not question or not answer:
                st.error("Título e fórmula são obrigatórios!")
            else:
                # Tenta adicionar a fórmula
                adicionar_formula(question, answer, tags)
                st.success(f"Fórmula '{question}' adicionada com sucesso!")
                st.balloons()

with col2:
    st.subheader("Excluir Fórmula")
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv('./formulas.csv')
        
        # Verifica se há fórmulas
        if len(df) > 0:
            # Exibe as fórmulas em um selectbox
            formula_selecionada = st.selectbox(
                'Selecione a fórmula para excluir:', 
                df['question'].tolist()
            )
            
            # Preview da fórmula selecionada
            formula_preview = df[df['question'] == formula_selecionada]['answer'].values[0]
            st.markdown("**Preview da Fórmula:**")
            st.latex(formula_preview)
            
            # Botão para excluir a fórmula selecionada
            if st.button('Excluir fórmula'):
                remover_formula(formula_selecionada)
                st.success(f"Fórmula '{formula_selecionada}' excluída com sucesso!")
                st.experimental_rerun()
        else:
            st.info("Nenhuma fórmula cadastrada.")
    
    except Exception as e:
        st.error(f"Erro ao carregar fórmulas: {e}")

# Exibição das fórmulas
st.divider()
st.subheader("Fórmulas Cadastradas")

try:
    df = pd.read_csv('./formulas.csv')
    
    if len(df) > 0:
        # Use columns para distribuir as fórmulas
        num_columns = 3
        cols = st.columns(num_columns)
        
        for i, row in df.iterrows():
            col_index = i % num_columns
            with cols[col_index]:
                st.markdown(f"**{row['question']}**")
                st.latex(row['answer'])
                st.caption(f"Tags: {row['tags']}")
    else:
        st.info("Nenhuma fórmula cadastrada.")

except Exception as e:
    st.error(f"Erro ao exibir fórmulas: {e}")
