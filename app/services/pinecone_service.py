import pinecone
from app.services.openai_service import get_embedding
import os
from pinecone import Pinecone, ServerlessSpec  # Add this import

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# Initialize Pinecone using the new method
pc = Pinecone(api_key=PINECONE_API_KEY)  # Replace the old init with this

EMBEDDING_DIMENSION = 1536

def embed_chunks_and_upload_to_pinecone(chunks, index_name):
    
    # delete the index if it already exists. 
    # as Pinecone's free plan only allows one index
    if index_name in pc.list_indexes().names():  # Update this line
        pc.delete_index(name=index_name)  # Update this line
    
    # create a new index in Pinecone
    pc.create_index(name=index_name,  # Update this line
                    dimension=EMBEDDING_DIMENSION, 
                    metric='cosine', 
                    spec=ServerlessSpec(
                        cloud='aws', 
                        region='us-east-1'
                    ))
    index = pc.Index(index_name)  # Update this line
    
    # embed each chunk and aggregate these embeddings
    embeddings_with_ids = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings_with_ids.append((str(i), embedding, chunk))
    
    # upload the embeddings and relevant texts for each chunk to the Pinecone index
    upserts = [(id, vec, {"chunk_text": text}) for id, vec, text in embeddings_with_ids]
    index.upsert(vectors=upserts)

def get_most_similar_chunks_for_query(query, index_name):
    question_embedding = get_embedding(query)
    index = pc.Index(index_name)  # Update this line
    query_results = index.query(question_embedding, top_k=3, include_metadata=True)
    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]
    return context_chunks
