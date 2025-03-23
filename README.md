# 🎓 KJC-BOT 🤖
A **RAG-based chatbot** for **Kristu Jayanti College** (my college 👉👈), built using **FAISS Vector DB** and **LLMs** to provide accurate and concise answers to the queries about the college. It utilizes **sentence embeddings** for efficient information retrieval and generates responses using **Groq’s Llama-3.3-70B model**.

## 🚀 Project Overview
This chatbot is designed to assist users by answering their queries about Kristu Jayanti College's academic programs, admission processes, and general college information. The chatbot is built using **Retrieval-Augmented Generation (RAG)**, where information is retrieved from a structured knowledge base and used to generate precise responses.
## 🏗 Implementation Details
### 1️⃣ Data Collection & Preprocessing 🗂️
- Scraped structured data containing details of **Computer Science UG & PG courses** and general college information. (as of now & will improve the scope of the data soon to cover the whole campus)
- Preprocessed data into a structured JSON format (`structured_data.json`).
## 2️⃣ Embeddings & Vector Database 📈
- Used **Sentence Transformers (all-MiniLM-L6-v2)** to generate high-quality text embeddings.
- Stored embeddings in **FAISS (Facebook AI Similarity Search)** for efficient nearest-neighbor retrieval.
### 3️⃣ Retrieval-Augmented Generation (RAG) 🧠
- The user's query is converted into an **embedding**.
- FAISS retrieves the **most relevant documents** from the stored knowledge base.
- Retrieved data is passed to **Groq’s Llama-3.3-70B model** to generate a structured response.
### 4️⃣ Streamlit UI for Chat Interface 💬
- Implemented an interactive chatbot interface using **Streamlit** for real-time query resolution.
- The chatbot provides confident and informative answers, avoiding vague responses.
## 🚀 Future Improvements
- ✅ Expand the dataset to cover all departments and college facilities.
- ✅ Enhance the chatbot UI with interactive elements in Streamlit.
- ✅ Optimize responses by fine-tuning prompt engineering for more natural conversations.
- ✅ Add multilingual support for broader accessibility. 🌍

⚠️ Data Availability : The dataset used for this chatbot (FAISS index, structured JSON data) has not been uploaded to this repository. Currently, the bot only contains information on CS UG & PG programs and some common information about the college. The data related files would be uploaded once the scope of the db is increased! In future updates, I'll upload the full scraped data and embeddings to enhance the chatbot’s coverage.

For any info, queries or contributions, feel free to reach out at **katasanikeerthanareddy@gmail.com** ! ✨ 
