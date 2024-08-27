import pinecone
from app.services.openai_service import get_embedding
import os
from pinecone import Pinecone, ServerlessSpec

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# Initialize Pinecone using the new method
pc = Pinecone(api_key=PINECONE_API_KEY)

EMBEDDING_DIMENSION = 1536

def embed_chunks_and_upload_to_pinecone(chunks, index_name):
    
    # delete the index if it already exists. 
    # as Pinecone's free plan only allows one index
    if index_name in pc.list_indexes().names():  # Use the client instance to list indexes
        pc.delete_index(name=index_name)  # Use the client instance to delete the index
    
    # create a new index in Pinecone
    pc.create_index(name=index_name,  # Use the client instance to create the index
                    dimension=EMBEDDING_DIMENSION, 
                    metric='cosine', 
                    spec=ServerlessSpec(
                        cloud='aws', 
                        region='us-east-1'
                    ))
    index = pc.Index(index_name)  # Get the index object using the client instance
    
    # embed each chunk and aggregate these embeddings
    embeddings_with_ids = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings_with_ids.append((str(i), embedding, chunk))
    
    # upload the embeddings and relevant texts for each chunk to the Pinecone index
    upserts = [(id, vec, {"chunk_text": text}) for id, vec, text in embeddings_with_ids]
    index.upsert(vectors=upserts)

#retrieving the most similar chunks to a query
def get_most_similar_chunks_for_query(query, index_name):
    # Convert user query to a vector
    question_embedding = get_embedding(query)
    index = pc.Index(index_name)
    
    # Query the Pinecone index using keyword arguments
    query_results = index.query(
        vector=question_embedding,  # Pass the vector as a keyword argument
        top_k=3,                   # Specify the number of top results to retrieve
        include_metadata=True      # Include metadata in the results
    )
    
    # Extract the actual text chunks from the metadata of the matched results
    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]
    return context_chunks

def delete_index(index_name):
    # Use the client instance to list and delete the index
    if index_name in pc.list_indexes().names():
        pc.delete_index(name=index_name)
