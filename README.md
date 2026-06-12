# 🩺 Medical AI Chatbot (RAG + Web + Memory)

An intelligent medical assistant chatbot built using **Flask + LangChain + Pinecone + OpenRouter**, capable of answering health-related queries using:

*  Custom medical documents (PDFs)
*  Medical research journals like PubMed, BMJ, NMJI, IJMR
*  Real-time web search (Tavily)
*  Conversational memory (context-aware responses)

# Features:
* 💬 Conversational chatbot with memory (last 2–3 messages context)
* 📎 Upload PDFs and query them (RAG)
* 🌐 Smart web fallback (medical → general search)
* 🏥 Priority search from trusted medical sources (PubMed, BMJ, etc.)
* ⚡ Fast and clean UI (chat-style interface)


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

# 🔄 Pipeline:
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

### 💬 2. Query Flow:
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

### 🧠 3. Memory:
* Stores last 2–3 messages
* Enables follow-up questions like:
  * "Which is better?"
  * "Can I take it?"


# 🛠️ Tech Stack

### Backend:
* Flask
* LangChain
* Pinecone (Vector DB)
* OpenRouter (LLM API)

### 🧠 AI / NLP:
* HuggingFace Embeddings
* RAG (Retrieval-Augmented Generation)
* Tavily (Web Search API)

### 🎨 Frontend:
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

# Demo: 
<img width="479" height="403" alt="1" src="https://github.com/user-attachments/assets/f2c7169b-b667-4e84-94d6-e5067bb99d25" />
<img width="353" height="398" alt="2" src="https://github.com/user-attachments/assets/c4ead9e3-a4ea-41a6-a154-87b3b3954a5c" />
<img width="295" height="170" alt="5" src="https://github.com/user-attachments/assets/9bb43c40-8431-416a-9972-9dd7ef1f5263" />
<img width="370" height="398" alt="6" src="https://github.com/user-attachments/assets/751e50ed-8ca5-488c-8e54-0aad8c9b1b0f" />
<img width="443" height="402" alt="7" src="https://github.com/user-attachments/assets/50d211ae-84b3-4cbe-91f7-5df9f9b8e360" />


# 🔮 Future Improvements

## 1. Prescription Upload (OCR)
* Integrate OCR (Tesseract / Google Vision)
* Extract text from handwritten prescriptions
* Convert to structured medical data

## 2. Privacy & Security
* Mask sensitive data like name, age, phone number etc. 
* Add encryption for uploaded files

## 3. Better Memory
* Session-based memory (per user)
* Long-term conversation storage


# 📌 Key Learnings
* RAG systems depend heavily on **retriever quality**
* Prompt engineering controls **output quality**
* Memory is essential for **real conversations**
* Medical AI requires **safety + accuracy balance**


# 🤝 Contributing:
Feel free to fork, improve, and contribute!
Consider giving it a star!
