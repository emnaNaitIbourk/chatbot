import streamlit as st
from openai import OpenAI

# Set up the page
st.set_page_config(page_title="AI_powered Chatbot", page_icon="🐋", layout="centered")
st.title("Chat Deepseek  🤖💡")
st.subheader("DeepSeek 🐋  Chatbot 💬🤖 prototype", divider="blue")

# Sidebar for temperature setting
st.sidebar.markdown("## Parameters")
st.sidebar.divider()
temp = st.sidebar.slider("Temperature", 0.0, 1.0, value=0.5)

# Create OpenAI client for DeepSeek using secrets
client = OpenAI(
     base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["DEEPSEEK_API_KEY"]
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
#function to save chat history
def render_chat_history_messages():
    print(st.session_state.chat_history)
    if len(st.session_state.chat_history)>0:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
render_chat_history_messages()


# Handle user input
if prompt := st.chat_input("Type your message here 💬..."):
    try:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "system", "content": "You are a helpful assistant."}] + st.session_state.chat_history,
            temperature=temp,
            stream=False  # important: stream must be False
        )

        assistant_reply = response.choices[0].message.content

        # Show assistant message
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        # Add assistant reply to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        st.error(f"🚨 Error: {e}")


    