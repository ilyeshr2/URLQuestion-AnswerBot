from . import api_blueprint
from flask import request, jsonify
from app.services import openai_service, pinecone_service, scraping_service
from app.utils.helper_functions import chunk_text

# Sample index name since we're only creating a single index
PINECONE_INDEX_NAME = 'index237'

@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
    url = request.json['url']
    url_text = scraping_service.scrape_website(url)
    chunks = chunk_text(url_text)
    pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return jsonify(response_json)

@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
  # handles embedding the user's question,
  # finding relevant context from the vector database,
  # building the prompt for the LLM,
  # and sending the prompt to the LLM's API to get an answer.
  pass