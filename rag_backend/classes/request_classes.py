from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    
class PreSignedUrlRequest(BaseModel):
    fileName: str
    fileType: str
    
class UploadRequest(BaseModel):
    s3_path: str