import faiss
import json
import numpy as np
import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found! Set it in a .env file or environment variable.")
    st.stop()

# Initialize Groq API
client = Groq(api_key=api_key)

# Load FAISS index
faiss_index = faiss.read_index("college_faiss.index")

# Load structured data
with open("structured_data.json", "r", encoding="utf-8") as f:
    structured_data = json.load(f)

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Streamlit UI
st.title("🎓 KJC-Bot")
st.write("Ask me queries about Kristu Jayanti College!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Function to generate sentence embeddings
def get_embedding(text):
    """Generate sentence embedding using MiniLM."""
    return model.encode([text], convert_to_numpy=True)[0]

# FAISS Search
def search_faiss(query_text, k=3):
    """Convert query to embedding and search FAISS index."""
    query_vector = np.array(get_embedding(query_text)).reshape(1, -1)
    _, indices = faiss_index.search(query_vector, k)

    # Ensure valid indices
    return [structured_data[i] for i in indices[0] if 0 <= i < len(structured_data)]

# Response generation with structured prompts
def generate_response(question):
    """Retrieve relevant text and generate response using Groq."""
    retrieved_chunks = search_faiss(question)

    # Limit text to prevent exceeding token limits
    max_tokens = 4000  # Groq's TPM limit is 6000
    combined_text = " ".join([chunk['content'] for chunk in retrieved_chunks])[:max_tokens]

    prompt = f"""
            You are a professional and authoritative chatbot for Kristu Jayanti College, Autonomous (Bengaluru).  
            Your responses should be direct, informative, and strictly based on the retrieved data.  
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "system", "content": combined_text},
            {"role": "user", "content": question},
        ],
        temperature=0.5,
        top_p=1,
        stream=False,
    )

    return response.choices[0].message.content

# User Input
user_input = st.chat_input("Ask me about the college...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check if the user wants to end the chat
    exit_keywords = ["exit", "bye", "thank you", "thankyou"]
    if user_input.lower() in exit_keywords:
        bot_response = "Thank you for reaching out. For more queries, feel free to contact us at **info@kristujayanti.com**. Have a great day! 😊"
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.chat_message("assistant").markdown(bot_response)
        st.stop()

    # Get AI response
    bot_response = generate_response(user_input)

    # Display and store bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").markdown(bot_response)
