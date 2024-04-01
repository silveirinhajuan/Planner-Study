import streamlit as st

def obter_tarefas():
    try:
        with open("tarefas.txt", "r", encoding='utf-8') as arquivo:
            tarefas = arquivo.readlines()
        return [tarefa.strip() for tarefa in tarefas]
    except FileNotFoundError:
        return []

def adicionar_tarefa(tarefa):
    with open("tarefas.txt", "a", encoding='utf-8') as arquivo:
        arquivo.write(f":eyes: {tarefa}\n")

def remover_tarefa(tarefa):
    tarefas = obter_tarefas()
    with open("tarefas.txt", "w") as arquivo:
        for t in tarefas:
            if t != tarefa:
                arquivo.write(f"{t}\n")

# Adiciona a lista de tarefas à barra lateral
st.title(":ledger: Afazeres")
nova_tarefa = st.text_input("Adicionar nova tarefa:")
if st.button("Adicionar"):
    adicionar_tarefa(nova_tarefa)
tarefas = obter_tarefas()
if tarefas:
    st.write("## Tarefas:")
    for i, tarefa in enumerate(tarefas):
        # Adiciona checkbox para marcar a tarefa como concluída
        concluido = st.checkbox(f"{i + 1}. {tarefa}")
        if concluido:
            # Remove a tarefa quando marcada como concluída
            remover_tarefa(tarefa)
else:
    st.write("Nenhuma tarefa adicionada ainda.")