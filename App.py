from conversation_manager import ConversationManager 
import streamlit as st
import os

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("The OpenAI API key is not set.")
    st.stop()

st.title("Welcome to Sunil's Chatbot!")
st.write("Powered by OpenAI's gpt-3.5-turbo model.")

if "chat_instance" not in st.session_state:
    st.session_state.chat_instance = ConversationManager(api_key)

chat_instance = st.session_state.chat_instance

st.sidebar.header("Chatbot Settings")
max_tokens = st.sidebar.slider("Maximum Tokens per Message", min_value=10, max_value=500, value=150)
temp = st.sidebar.slider("Response Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.01)

if st.sidebar.button("Clear Chat History"):
    chat_instance.reset_conversation_history()
    st.session_state.conversation_history = chat_instance.conversation_history  

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = chat_instance.conversation_history

history = st.session_state.conversation_history

message = st.chat_input("Type your message here...")
if message:
    response = chat_instance.chat_completion(message, temperature=temp, max_tokens=max_tokens)

for message in history:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])
