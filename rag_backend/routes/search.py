from fastapi import HTTPException
import yaml
from classes.request_classes import QueryRequest
from modules import embedding_service, vector_store
from services.llm_response import generate_response_llm
from fastapi import APIRouter

# Load configuration
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

embedding_service = embedding_service.EmbeddingService(config['embedding_model'])
vector_store = vector_store.VectorStore(dimension=384, index_file=config['faiss']['index_file'])

try:
    vector_store.load()
    print("Vector store loaded successfully.")
    print(f"Number of stored sentences: {len(vector_store.sentences)}")
except FileNotFoundError:
    print("No saved vector store found. Starting with an empty vector store.")


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
                "answer": "Hello! You can ask questions about the topics stored in our database. For example, 'What is AI?' or 'Explain blockchain.'"
            }


        query_embedding, _ = embedding_service.generate_embeddings(query)
        
        distances, indices = vector_store.search(query_embedding, config['faiss']['top_k'])
        print(f"Indices: {indices}")  # Log context


        if not indices.size or (indices[0] < 0).all():
            raise HTTPException(status_code=404, detail="No relevant results found for the query.")

        indices = indices[0].tolist()

        context = "\n".join([vector_store.sentences[i] for i in indices])
        print(f"Generated context: {context}")  # Log context
      
        answer = generate_response_llm(context, query)
        print(answer)
        return {"answer": answer.strip()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    
