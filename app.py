from flask import Flask, render_template, request
from src.rag import rag_chain

app = Flask(__name__)


@app.route("/")
def chatBot():
    return render_template("chatBot.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("Question:", msg)
    try:
        response = rag_chain.invoke({"input": msg})
        print("Response:", response["answer"])
        return str(response["answer"])
    except Exception as e:
        print("Error:", e)
        return "Sorry, I can't answer right now. Please try again in a moment."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



# from flask import Flask, render_template, jsonify, request
# from src.helper import download_hugging_face_embeddings
# from langchain_pinecone import PineconeVectorStore
# # from langchain_openai import OpenAI
# #from langchain_openai import ChatOpenAI
# # from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
# from langchain_classic.chains import create_retrieval_chain
# from langchain_classic.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.llms import CTransformers
# from langchain_classic.chains import RetrievalQA
# from dotenv import load_dotenv
# from src.prompt import *
# import os

# app = Flask(__name__)

# load_dotenv()

# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
# # OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
# # GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["GROQ_API_KEY"]  = GROQ_API_KEY
# # os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# # os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# embeddings = download_hugging_face_embeddings()

# #Initializing the Pinecone
# # pinecone.init(api_key=PINECONE_API_KEY,
# #               environment=PINECONE_API_ENV)

# index_name="echis-bot"

# #Loading the index
# docsearch=PineconeVectorStore.from_existing_index(
#     index_name = index_name, 
#     embedding = embeddings
#     )

# retriever = docsearch.as_retriever(search_type ="similarity", search_kwargs={"k": 3})
# llm = ChatGroq(
#     model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
#     temperature=0.4,
#     max_retries=3,
# )
# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-3.8-flash", 
# #     temperature=0.4,
# #     max_retries=5,
# #     )
# # llm = ChatOpenAI(
# #     model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
# #     temperature=0.4,
# #     max_tokens=500,
# # )
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )

# question_answer_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)
# # PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])


# @app.route("/")
# def chatBot():
#     return render_template('chatBot.html')

# @app.route("/get", methods=["GET", "POST"])
# def chat():
#     msg = request.form["msg"]
#     input = msg
#     print(input)
#     response = rag_chain.invoke({"input": msg})
#     print("Response : ", response["answer"])
#     return str(response["answer"])



# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port= 5000, debug= True)
