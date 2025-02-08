# Python Rag Backend System

## Setup
```sh
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  

# Pull the Llama model
ollama pull llama3.2:1b

# Run the model
ollama run llama3.2:1b
```

```sh
git clone https://github.com/skushagra9/rag-pdf
cd rag-backend
pip install -r requirements.txt 
cp .env.example .env
```

Fill in the enviornment details

```sh 
uvicorn app:app --reload
```


## Features

### **1. PDF Upload and Processing (S3 Integration)**

#### **Pre-Signed URL Generation (`/s3/generate-presigned-url/`)**
- Generates a **pre-signed PUT URL** to allow users to upload PDFs to S3.
- The signed URL expires in **15 minutes (900 seconds)**.
- Uses **boto3** to interact with **AWS S3**.

#### **PDF Processing (`/s3/upload_pdf/`)**
- Fetches the uploaded PDF from S3 **in-memory**.
- Extracts text from the PDF using `extract_text_from_pdf`.
- Generates **embeddings** from the extracted text.
- Stores these embeddings in **Pinecone vector database** for future retrieval.
- Uses a **sentence-wise approach**, meaning each sentence is stored with its embedding.

---

### **2. Vector Search (Retrieval Component)**

#### **Query Endpoint (`/search/query/`)**
- Accepts user queries to search the **stored knowledge base**.
- Uses **trivial query filtering** to handle greetings & common questions (e.g., `"hi"`, `"who are you?"`).
- Converts the query into **embeddings**.
- Searches for the **most relevant stored embeddings** in **Pinecone** (`top_k=5`).
- Retrieves **matching sentences** from the stored embeddings.
- If no results are found, returns:  
  `"I'm sorry, but I couldn't find relevant information in the database."`
- Uses an **LLM (`generate_response_llm`)** to generate responses from the retrieved context.

---

### **3. Embedding Service (Vectorization)**

- Uses an **embedding model** (loaded from `config.yaml`) to generate:
  - **Embeddings for PDF text** (during upload).
  - **Embeddings for user queries** (during search).
- Stores and retrieves **sentence-level embeddings** from **Pinecone**.

---

### **4. Infrastructure & Tech Stack**
- **AWS S3** → File storage.
- **Pinecone** → Storing and retrieving vector embeddings.
- **FastAPI** → API handling.
- **boto3** → AWS interactions.
- **yaml** → Configuration management.
- **Custom Modules**:
  - `embedding_service` → Embedding generation.
  - `llm_response` → LLM response generation.

## IMPROVEMENTS and Enhancements

## 1. Storing Knowledge Segments Efficiently  

### Why?  
Large documents need to be fragmented properly to enable better retrieval.

### Solution  
- Store knowledge segments efficiently.  
- Further fragment them and create embeddings using **HNSW (Hierarchical Navigable Small World)** indexing for optimized similarity search.  
- Select **top N** matches and link them back to the original knowledge segment.  
- Use only **unique matched segments** to avoid redundant information.  

### Outcome  
- Improved retrieval speed  
- Better accuracy  
- Optimized storage  


---

## 2. Using DeepEval to Evaluate Metrics

### Why?  
Ensuring the quality and accuracy of retrieved knowledge is crucial.

### Solution  
Implement **DeepEval** to evaluate RAG pipeline metrics such as:  
- Retrieval accuracy  
- Relevancy  
- Answer correctness  

### Outcome  
- Continuous evaluation and benchmarking to improve retrieval quality.  

---

## 3. Adding Task Queue for PDF Processing

### Why?  
Processing large PDFs synchronously can block the system and slow down performance.

### Solution  
Implement a task queue (Celery/Redis) to handle PDF processing asynchronously. This ensures that large documents are processed in the background without affecting system responsiveness.

### Outcome  
- Faster response times  
- Better system stability  

## 4. Dockerizing the python-services and splitting into micro-architecture to deploy to kubernetes