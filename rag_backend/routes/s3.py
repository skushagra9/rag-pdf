import io
import boto3
from fastapi import HTTPException
from pinecone import Pinecone, ServerlessSpec
import yaml
from modules import embedding_service
from classes.request_classes import PreSignedUrlRequest, UploadRequest
from config.config import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, PINECONE_API_KEY, PINECONE_DIMENSIONS, PINECONE_ENVIORNMENT, PINECONE_INDEX_NAME, S3_BUCKET_NAME
from services.pdf_parser import extract_text_from_pdf
from botocore.exceptions import NoCredentialsError
from fastapi import APIRouter

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

embedding_service = embedding_service.EmbeddingService(config['embedding_model'])
pc = Pinecone(api_key=PINECONE_API_KEY)
vector_store = pc.Index(PINECONE_INDEX_NAME)
router = APIRouter(prefix="/s3", tags=["S3-Configuration"])

@router.post("/generate-presigned-url/")
async def generate_presigned_url(presignedurlrequest:PreSignedUrlRequest):
    """Generate a pre-signed PUT URL for uploading a file to S3."""
    try:
        print(S3_BUCKET_NAME)
        if not S3_BUCKET_NAME:
            raise HTTPException(status_code=500, detail="S3 bucket name not configured.")

        object_key = f"pdfs/{presignedurlrequest.fileName}"

        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': S3_BUCKET_NAME,
                'Key': object_key,
                'ContentType': presignedurlrequest.fileType
            },
            ExpiresIn=900  # URL valid for 15 minutes
        )
        return {"url": presigned_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating pre-signed URL: {str(e)}")

@router.post("/upload_pdf/")
async def upload_pdf(uploadrequest: UploadRequest):
    """Fetch the uploaded PDF from S3 and process it in-memory."""
    print(uploadrequest, "received", "hello", S3_BUCKET_NAME)
    try:
        # Get the file from S3 as a stream
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=uploadrequest.s3_path)
        pdf_stream = response['Body'].read()
        pdf_file = io.BytesIO(pdf_stream)
        text = extract_text_from_pdf(pdf_file)


        embeddings, sentences = embedding_service.generate_embeddings(text)
        vectors_to_upsert = [
            (f"{uploadrequest.s3_path}-{i}", embeddings[i].tolist(), {"sentence": sentences[i]})
            for i in range(len(embeddings))
            ]
        vector_store.upsert(vectors=vectors_to_upsert)

        return {"message": "PDF processed and stored successfully."}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available.")
    except Exception as e:
        print("Failed here", e)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
