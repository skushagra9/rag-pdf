from fastapi import FastAPI, UploadFile, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
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
        
        # Use a file-like object (BytesIO) to avoid saving locally
        pdf_file = io.BytesIO(pdf_stream)
        text = extract_text_from_pdf(pdf_file)  # Pass the file-like object

        # Generate embeddings
        embeddings, sentences = embedding_service.generate_embeddings(text)
        vector_store.add_embeddings(embeddings, sentences=sentences)

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
        
        # Generate query embedding
        query_embedding, _ = embedding_service.generate_embeddings(query)
        
        # Search for the top K similar entries
        distances, indices = vector_store.search(query_embedding, config['faiss']['top_k'])

        # Convert indices from NumPy array to list of integers
        indices = indices[0].tolist()

        # Retrieve the most relevant sentences
        context = "\n".join([vector_store.sentences[i] for i in indices])

        # Generate a response using LLM
        prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        return {"answer": response["choices"][0]["text"].strip()}
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
