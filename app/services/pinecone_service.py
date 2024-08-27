from pinecone import Pinecone, ServerlessSpec
from app.services.openai_service import get_embedding
from dotenv import load_dotenv
import os

# Load the Pinecone API key from an environment variable
load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# Create an instance of the Pinecone class
pc = Pinecone(api_key=PINECONE_API_KEY) 

EMBEDDING_DIMENSION = 384

def embed_chunks_and_upload_to_pinecone(chunks, index_name):
    
    # delete the index if it already exists. 
    # as Pinecone's free plan only allows one index
    if index_name in pc.list_indexes().names():
        pc.delete_index(name=index_name)
    
    # create a new index in Pinecone
    # the EMBEDDING_DIMENSION is based on what 
    # your embedding model outputs for all-MiniLM-L6-v2 it is 384
    pc.create_index(
        name=index_name,
        dimension=EMBEDDING_DIMENSION,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
            )  # Adjust according to your needs
    )
    
    # Access the created index
    index = pc.Index(index_name)
    
    # Embed each chunk and aggregate these embeddings
    embeddings_with_ids = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings_with_ids.append((str(i), embedding, chunk))
          
        
    # Prepare the data for upsertion
    upserts = [(id, vec, {"chunk_text": text}) for id, vec, text in embeddings_with_ids]
    
    # Upsert embeddings into Pinecone index
    index.upsert(vectors=upserts)