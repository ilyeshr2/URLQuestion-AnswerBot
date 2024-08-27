PROMPT_LIMIT = 3750


def chunk_text(text, chunk_size=200):
    # Split the text by sentences to avoid breaking in the middle of a sentence
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # Check if adding the next sentence exceeds the chunk size
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + '. '
        else:
            # If the chunk reaches the desired size, add it to the chunks list
            chunks.append(current_chunk)
            current_chunk = sentence + '. '
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def build_prompt(query, context_chunks):
    prompt_start = (
        "Answer the question based on the context below. If you don't know the answer based on the context provided below, just respond with 'I don't know' instead of making up an answer. Return just the answer to the question, don't add anything else. Don't start your response with the word 'Answer:'. Make sure your response is in markdown format\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    
    prompt = ""
    total_length = 0
    for i in range(len(context_chunks)):
        chunk = context_chunks[i]
        chunk_length = len(chunk)
        if total_length + chunk_length + len(prompt_start) + len(prompt_end) > PROMPT_LIMIT:
            prompt = prompt_start + "\n\n---\n\n".join(context_chunks[:i]) + prompt_end
            break
        total_length += chunk_length
        if i == len(context_chunks) - 1:
            prompt = prompt_start + "\n\n---\n\n".join(context_chunks) + prompt_end
    return prompt


def construct_messages_list(chat_history, prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Populate the messages array with the current chat history
    for message in chat_history:
        if message['isBot']:
            messages.append({"role": "system", "content": message["text"]})
        else:
            messages.append({"role": "user", "content": message["text"]})
    # Replace last message with the full prompt
    messages[-1]["content"] = prompt    
    
    return messages
