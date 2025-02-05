from fastapi import FastAPI, UploadFile, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from modules.llm_model import generate_response_openai
from modules.pdf_parser import extract_text_from_pdf
from modules.embedding_service import EmbeddingService
from modules.vector_store import VectorStore
import openai
import yaml
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import boto3
import io
from botocore.exceptions import NoCredentialsError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Load configuration
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

openai.api_key = os.getenv("OPENAI_API_KEY")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
embedding_service = EmbeddingService(config['embedding_model'])
vector_store = VectorStore(dimension=384, index_file=config['faiss']['index_file'])
# Load vector store on startup
try:
    vector_store.load()
    logger.info("Vector store loaded successfully.")
    logger.info(f"Number of stored sentences: {len(vector_store.sentences)}")
except FileNotFoundError:
    logger.warning("No saved vector store found. Starting with an empty vector store.")


s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)
class QueryRequest(BaseModel):
    query: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.post("/upload_pdf/")
async def upload_pdf(s3_path: str = Form(...)):
    """Fetch the uploaded PDF from S3 and process it in-memory."""
    try:
        # Get the file from S3 as a stream
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_path)
        pdf_stream = response['Body'].read()
        pdf_file = io.BytesIO(pdf_stream)
        text = extract_text_from_pdf(pdf_file)

        embeddings, sentences = embedding_service.generate_embeddings(text)
        vector_store.add_embeddings(embeddings, sentences=sentences)

        # Save the vector store to disk
        vector_store.save()

        return {"message": "PDF processed and stored successfully."}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/query/")
async def query_endpoint(request: QueryRequest):
    """Query the stored vector database."""
    try:
        # Access the query string from the request
        query = request.query
        logger.info(f"Received query: {query}")  # Log the query        
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
        
        # Search for the top K similar entries
        distances, indices = vector_store.search(query_embedding, config['faiss']['top_k'])
        logger.info(f"Indices: {indices}")  # Log context


        if not indices.size or (indices[0] < 0).all():
            raise HTTPException(status_code=404, detail="No relevant results found for the query.")

        # Convert indices from NumPy array to list of integers
        indices = indices[0].tolist()

        # Retrieve the most relevant sentences
        context = "\n".join([vector_store.sentences[i] for i in indices])
        logger.info(f"Generated context: {context}")  # Log context
        # Generate a response using LLM
      
        # answer = generate_response_openai(context, query)
        print(answer)
        return {"answer": answer.strip()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    


@app.post("/generate-presigned-url/")
async def generate_presigned_url(fileName: str = Form(...), fileType: str = Form(...)):
    """Generate a pre-signed PUT URL for uploading a file to S3."""
    try:
        bucket_name = os.getenv('S3_BUCKET_NAME')
        if not bucket_name:
            raise HTTPException(status_code=500, detail="S3 bucket name not configured.")

        object_key = f"pdfs/{fileName}"

        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ContentType': fileType
            },
            ExpiresIn=900  # URL valid for 15 minutes
        )
        return {"url": presigned_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating pre-signed URL: {str(e)}")
