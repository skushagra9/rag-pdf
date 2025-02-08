from ollama import Client

client = Client(host='http://127.0.0.1:11434')

def generate_response_llm(context, query):
    # Crafting a detailed and explicit system message
    system_message = (
        "You are a highly skilled assistant trained to answer questions based on provided context. "
        "Your answers should be concise, clear, and directly based on the context you are given. "
        "If the context does not contain enough information to answer, reply with 'Sorry, I cannot provide an answer based on the given context.' "
        "Avoid hallucination, and ensure that the response is factually correct based on the context."
    )

    # Formulating the user message with better context presentation
    user_message = (
        f"Below is the context extracted from a document. Use the context to provide a precise answer to the question that follows.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\nAnswer:"
    )

    # Structure the messages with system and user prompts
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    print( messages)
    # Send the prompt to the LLM and fetch the response
    response = client.chat(
        model="llama3.2:1b",
        messages=messages
    )
    
    # Extracting the answer from the response
    answer = response.message.content.strip()
    return answer
