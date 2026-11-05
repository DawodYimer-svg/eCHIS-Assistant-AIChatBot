from src.helper import load_pdf, text_split, download_hugging_face_embeddings
# from pinecone.grpc import PineconeGRPC as pinecone
from pinecone import Pinecone as pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os

load_dotenv()

#PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
#PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
# print(PINECONE_API_KEY)
# print(PINECONE_API_ENV)

extracted_data = load_pdf("Data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()
#Initializing the Pinecone
#pinecone.init(api_key=PINECONE_API_KEY,
#              environment=PINECONE_API_ENV)
pc = pinecone(api_key = PINECONE_API_KEY)

index_name="echis-bot"

pc.create_index(
    name = index_name,
    dimension = 384,
    metric = "cosine",
    spec = ServerlessSpec(
        cloud ="aws",
        region ="us-east-1"
    )
)

#Creating Embeddings for Each of The Text Chunks & storing
docsearch=PineconeVectorStore.from_documents(
    documents = text_chunks,
    index_name=index_name,
    embedding = embeddings, 
    )
