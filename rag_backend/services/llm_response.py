from ollama import Client

client = Client(host='http://127.0.0.1:11434')
def generate_response_llm(context, query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Below is the context of a document:\n\n{context}\n\nBased on the context, answer the following question concisely:\n\nQuestion: {query}\nAnswer:"}
    ]

    response = client.chat(
        model="llama3.2:1b",
        messages=messages
        )
    
    answer = response.message.content
    return answer
