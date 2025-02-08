from fastapi import HTTPException
from pinecone import Pinecone, ServerlessSpec
import yaml
from classes.request_classes import QueryRequest
from modules import embedding_service
from config.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from services.llm_response import generate_response_llm
from fastapi import APIRouter

# Load configuration
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

embedding_service = embedding_service.EmbeddingService(config['embedding_model'])
pc = Pinecone(api_key=PINECONE_API_KEY)
vector_store = pc.Index(PINECONE_INDEX_NAME)

router = APIRouter(prefix="/search", tags=["Vector-Search"])

@router.post("/query/")
async def query_endpoint(request: QueryRequest):
    """Query the stored vector database."""
    try:
        # Access the query string from the request
        query = request.query
        print(f"Received query: {query}")  # Log the query        
        # Generate query embedding
        trivial_queries = [
            "hello", "hi", "hey", "help", "what can I ask", "who are you", "what do you do",
            "how are you", "hello there", "hi there", "good morning", "good afternoon",
            "good evening", "what's up", "sup", "yo", "hola", "bonjour", "greetings",
            "can you help me", "tell me what you do", "what are you", "who am I talking to",
            "what can you do", "how can you help me", "what topics can I ask about", "hi bot"
        ]
        if query.lower() in trivial_queries:
            return {
                "answer": "Hello! You can ask questions about the topics stored in our database from the admin-dashboard"
            }


        # query_embedding = embedding_service.encode([query])  # Embedding the query
        # search_results = index.query(queries=query_embedding, top_k=5)
        
        # # Assuming search results are the most relevant documents
        # retrieved_docs = [res['metadata']['text'] for res in search_results['results'][0]['matches']]
        
        # # Generate response from the retrieved documents (you could use a language model here)
        # response = f"Here are the top results: {retrieved_docs}"
        # answer = generate_response_llm(response, query)
        
        query_embedding = embedding_service.generate_embeddings(query)[0]  # Extract first result

        search_results = vector_store.query(
            vector=query_embedding.tolist(),  # Convert to list
            top_k=5,
            include_metadata=True  # Ensure metadata is included in results
        )

        retrieved_sentences = [match["metadata"]["sentence"] for match in search_results["matches"]]
        print(retrieved_sentences)
        if not retrieved_sentences:
            return {"answer": "I'm sorry, but I couldn't find relevant information in the database."}
        formatted_context = "\n".join(retrieved_sentences)
        print("hello", formatted_context)
        answer = generate_response_llm(formatted_context, query)
        print(answer)
        return {"answer": answer.strip()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    
