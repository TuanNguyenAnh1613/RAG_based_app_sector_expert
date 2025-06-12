import os
import requests
import streamlit as st

"""
    This RAG LLM chatbot frontend was built depending on the Streamlit Library.
    References: "https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps"
"""

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/query")
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent designed to answer questions about sector investment specializing Vietnam's economist.
        """
    )
st.title("Sector Investment Chatbot")
st.info(
    "Ask me questions about Vietnam's economist like macro trends, fiscal policy, monetary policy, foreign investment, trade, and market movement, etc. "
    
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])


if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
           

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text
        }
    )
