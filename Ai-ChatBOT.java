from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the chatbot template
template = """
Hi, I am your mental health assistant. Consider me your friend and drop a question.

Here is the conversation history: {context}

You: {question}
AI:
"""

# Initialize the chatbot model
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome! I’m here to help. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Take care! I'm always here if you need me.")
            break
        
        result = chain.invoke({"context": context, "question": user_input})
        print("AI:", result)
        
        # Append conversation to maintain context
        context += f"\nYou: {user_input}\nAI: {result}"

if _name_ == "_main_":
    handle_conversation()
