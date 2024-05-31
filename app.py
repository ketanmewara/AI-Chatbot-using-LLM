import streamlit as st
from langchain.llms import Ollama

st.title("AI ChatBot")
llm = Ollama(model="llama2:latest")

def main():
    # Initialize chat history
    if "messages" not in st.session_state.keys():
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # user input
    if prompt := st.chat_input("Write question here"):
        # Display user message in chat message
        st.chat_message("user").markdown(f"User: {prompt}")
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message
        with st.chat_message("assistant"):
            full_response = ''
            placeholder = st.empty()
            for chunks in llm.stream(prompt, num_predict=100):
                full_response += chunks
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
        # Add assistant response to chat history
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

if __name__ == "__main__":
    main()