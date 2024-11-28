import ollama
import streamlit as st

st.title('Selene🧬')

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
if "model" not in st.session_state:
    st.session_state["model"] = ""

models = [model["model"] for model in ollama.list()["models"]]
st.session_state["model"] = st.selectbox("Choose your model", models)

def model_res_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]
    
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso te ajudar?"):
    st.session_state['messages'].append({"role":"user", "content": prompt})
    with st.chat_message("user", avatar="🤓"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})