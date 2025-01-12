from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import openai
# Load a local model and tokenizer
model_name = "gpt2"  # Replace with the model of your choice
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Generate a response using the local model
def generate_response_local(context, query):
    
    prompt = f"""
    Below is the context of a document:

    {context}

    Based on the context, answer the following question concisely:

    Question: {query}
    Answer:
    """    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=200,
        num_return_sequences=1,
        # temperature=0.7,
        # top_p=0.9
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

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
