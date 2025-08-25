import streamlit as st

def chat(rag_method, chain):
    st.title("Chat with RAG")
    user_input = st.text_input("You: ", "")
    send_button = st.form_submit_button("Send")
    if send_button:
        response = rag_method(user_input, chain)
        st.text_area("RAG: ", value=response, height=300)