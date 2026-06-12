from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
import certifi
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.prompt import *
from werkzeug.utils import secure_filename
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split


app = Flask(__name__)
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()
tavily_tool = TavilySearchResults(k=3)
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["OPENROUTER_API_KEY"]=OPENROUTER_API_KEY

embeddings=download_hugging_face_embeddings()
index_name="medical-chatbot"
docsearch=PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name
)

retriever=docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
chatModel=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    model="openai/gpt-oss-120b:free",
    temperature=0.3,
    max_tokens=300)


prompt=ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human","{input}"),
    ]
)
question_answer_chain=create_stuff_documents_chain(chatModel, prompt)
rag_chain=create_retrieval_chain(retriever, question_answer_chain)
def rag_tool_func(query):
    result = rag_chain.invoke({"input": query})
    return result["answer"]

rag_tool = Tool(
    name="Medical Knowledge Base",
    func=rag_tool_func,
    description="Use this tool to answer questions about diseases, symptoms, treatments, and medicines from medical documents"
)
tools = [rag_tool, tavily_tool]
agent = initialize_agent(
    tools=tools,
    llm=chatModel,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

chat_history=[]

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    global retriever, rag_chain
    try:
        msg = request.form.get("message")
        file = request.files.get("file")
        print("User:", msg)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join("uploads", filename)
            file.save(file_path)
            print("File saved:", file_path)
            docs = load_pdf_files("uploads/")
            minimal_docs = filter_to_minimal_docs(docs)
            chunks = text_split(minimal_docs)
            print("Chunks created:", len(chunks))
            vectorstore = PineconeVectorStore.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    index_name=index_name
                )
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            return "📄 File uploaded! You can now ask questions about it."
        
        context_messages = chat_history[-3:]  # last 3 messages

        history_text = ""
        for h in context_messages:
            history_text += f"{h['role']}: {h['content']}\n"

        final_input = f"""
        Conversation:
        {history_text}

        Current question:
        {msg}
        """
        rag_response = rag_chain.invoke({"input": final_input})
        answer = rag_response["answer"]
        print("RAG Answer:", answer)
        if answer.strip() != "UNKNOWN":
            chat_history.append({"role": "user", "content": msg})
            chat_history.append({"role": "bot", "content": answer})
            return answer
        
        if answer.strip()=="UNKNOWN":
            medical_results = tavily_tool.invoke({
                "query": msg,
                "include_domains": [
                    "pubmed.ncbi.nlm.nih.gov",
                    "bmj.com",
                    "nmji.in",
                    "ijmr.org.in"
                ]
            })

            medical_context = "\n".join([
                res["content"] for res in medical_results
            ]) if medical_results else ""

            if medical_context.strip():
                print("Using medical sources")

            final_prompt = f"""
            Answer the question using trusted medical sources:
            
            If asked about a specific medicine,
            Give output in this format ONLY:
            Medicine: <name>
                • Use: ...
                • Benefit: ...
                • Side effects: ...
                • Warning: ...

            Keep it SHORT (max 5 bullet points).
            Rules:
            • No paragraphs
            • No tables
            • No long sentences
            • Max 5 lines

            Context:
            {medical_context}

            Question: {msg}
            """

            final_answer = chatModel.invoke(final_prompt).content
            print("Bot: ", final_answer)
            chat_history.append({"role": "user", "content": msg})
            chat_history.append({"role": "bot", "content": final_answer})
            return final_answer
        
        
        
        general_results = tavily_tool.invoke(msg)

        general_context = "\n".join([
            res["content"] for res in general_results
        ])
        final_prompt = f"""
        Answer using this web data.

        Keep answer SHORT and structured if asked about a medicine give the:
        • Use
        • Benefit
        • Side effects
        • Warning

        otherwise give general message

        Context:
        {general_context}

        Question: {msg}
        """

        final_answer = chatModel.invoke(final_prompt).content
        chat_history.append({"role": "user", "content": msg})
        chat_history.append({"role": "bot", "content": final_answer})
        return final_answer
        
    except Exception as e:
        print("ERROR:", e)
        return "⚠️ Server error"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)