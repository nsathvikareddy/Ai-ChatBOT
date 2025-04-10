import streamlit as st
import ollama
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="AuraMind")

page_bg = '''
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506126613408-eca07ce68773");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .chat-container {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 15px;
        border-radius: 10px;
    }
</style>
'''
st.markdown(page_bg, unsafe_allow_html=True)

st.session_state.setdefault('conversation_history', [])

template = """
You are a mental health support chatbot. Your goal is to provide empathetic, thoughtful, and calming responses 
to help users with stress, anxiety, and emotional well-being. Use previous conversation history to improve 
your responses and maintain a comforting tone.

Here is the conversation history: {context}

User's Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def generate_response(user_input):
    """Generates a response using LangChain-based chatbot with memory"""
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state['conversation_history']])
    result = chain.invoke({"context": context, "question": user_input})
    
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    st.session_state['conversation_history'].append({"role": "assistant", "content": result})
    
    return result

def generate_affirmation():
    """Generates a positive affirmation"""
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def generate_meditation_guide():
    """Generates a 5-minute guided meditation script"""
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

st.title("🌿 AuraMind")

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")
st.markdown("</div>", unsafe_allow_html=True)

user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

col1, col2 = st.columns(2)

with col1:
    if st.button("💖 Give me a positive affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("🧘‍♂️ Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
