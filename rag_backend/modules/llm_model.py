import openai

# Generate a response using OpenAI
def generate_response_openai(context, query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Below is the context of a document:\n\n{context}\n\nBased on the context, answer the following question concisely:\n\nQuestion: {query}\nAnswer:"}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Replace with "gpt-4" or "gpt-3.5-turbo"
        messages=messages,
        max_tokens=150,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.3
    )
    answer = response.choices[0].message.content.strip()
    print(answer)
    return answer
