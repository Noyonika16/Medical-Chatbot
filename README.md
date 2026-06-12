# 🩺 Medical AI Chatbot (RAG + Web + Memory)

An intelligent medical assistant chatbot built using **Flask + LangChain + Pinecone + OpenRouter**, capable of answering health-related queries using:

* 📄 Custom medical documents (PDFs)
* 🌐 Real-time web search (Tavily)
* 🧠 Conversational memory (context-aware responses)


# 🚀 Features

* 💬 Conversational chatbot with memory (last 2–3 messages context)
* 📎 Upload PDFs and query them (RAG)
* 🌐 Smart web fallback (medical → general search)
* 🏥 Priority search from trusted medical sources (PubMed, BMJ, etc.)
* ⚡ Fast and clean UI (chat-style interface)
* 🧠 Context-aware follow-up questions


# 🏗️ Project Structure

```
Medical-Chatbot/
│
├── app.py                
├── requirements.txt      
├── setup.py              
├── .env                   
│
├── src/
│   ├── __init__.py
│   ├── helper.py         
│   ├── prompt.py          
│
├── templates/
│   └── chat.html         
│
├── static/
│   └── style.css         
│
├── uploads/              
│
└── README.md
```


# 🧠 Architecture

```
User Input
   ↓
Frontend (HTML/CSS/JS)
   ↓
Flask Backend (app.py)
   ↓
-----------------------------------
| 1. RAG Pipeline (PDF Knowledge) |
| 2. Medical Web Search (Tavily)  |
| 3. General Web Fallback         |
-----------------------------------
   ↓
LLM (OpenRouter / GPT)
   ↓
Response → UI
```


# 🔄 Pipeline

### 🧾 1. Document Processing (RAG)

```
PDF → PyPDFLoader → Text
      ↓
Text → Chunking
      ↓
Embeddings (HuggingFace)
      ↓
Stored in Pinecone
```

### 💬 2. Query Flow

```
User Query
   ↓
Add chat history (context)
   ↓
RAG Retrieval
   ↓
IF relevant → answer
ELSE →
   ↓
Medical search (PubMed, BMJ)
   ↓
IF found → answer
ELSE →
   ↓
General web search
```


### 🧠 3. Memory

* Stores last 2–3 messages
* Enables follow-up questions like:

  * "Which is better?"
  * "Can I take it?"


# 🛠️ Tech Stack

### 🔙 Backend

* Flask
* LangChain
* Pinecone (Vector DB)
* OpenRouter (LLM API)

### 🧠 AI / NLP

* HuggingFace Embeddings
* RAG (Retrieval-Augmented Generation)
* Tavily (Web Search API)

### 🎨 Frontend

* HTML, CSS, JavaScript
* Chat UI with typing animation


# ⚙️ Setup & Installation

## 1. Clone Repo

```bash
git clone https://github.com/your-username/Medical-Chatbot.git
cd Medical-Chatbot
```

## 2. Create Environment

```bash
conda create -n medibot python=3.10
conda activate medibot
```


## 3. Install Dependencies

```bash
pip install -r requirements.txt
```


## 4. Add API Keys (.env)

```
PINECONE_API_KEY=your_key
OPENROUTER_API_KEY=your_key
TAVILY_API_KEY=your_key
```


## 5. Run App

```bash
python app.py
```

Open:

```
http://localhost:8080
```


# 🖼️ Demo

> Add screenshots here

* Chat UI
* File upload
* Medical responses



# 🔮 Future Improvements

## 🧾 1. Prescription Upload (OCR)

* Integrate OCR (Tesseract / Google Vision)
* Extract text from handwritten prescriptions
* Convert to structured medical data


## 🔐 2. Privacy & Security

* Mask sensitive data:
  * Name
  * Age
  * Phone number
* Avoid storing user data permanently
* Add encryption for uploaded files


## 🧠 3. Better Memory

* Session-based memory (per user)
* Long-term conversation storage


## 🧬 4. Medical Intelligence

* Extract:
  * Diseases
  * Medicines
  * Dosage
* Provide structured summaries


## 🌐 5. Advanced Retrieval

* Hybrid search (RAG + web + PubMed API)
* Confidence scoring
* Source citations


## 🎨 6. UI Improvements

* Chat history sidebar
* File preview
* Streaming responses


# 📌 Key Learnings

* RAG systems depend heavily on **retriever quality**
* Prompt engineering controls **output quality**
* Memory is essential for **real conversations**
* Medical AI requires **safety + accuracy balance**


# 🤝 Contributing

Feel free to fork, improve, and contribute!


# 📜 License

MIT License

# ⭐ Acknowledgements

* LangChain
* Pinecone
* OpenRouter
* Tavily API
