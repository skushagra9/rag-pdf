# Admin Dashboard

![alt text](image.png)


### Setup Project


```sh
git clone https://github.com/skushagra9/rag-pdf
cd admin-ui
npm install 
cp .env.example .env
```


## Features

The PdfUpload component allows users to upload a PDF file, store it in AWS S3, and trigger server-side processing.

### 🔹 Features:

  - Drag & Drop Support (via react-dropzone)
  - Pre-signed URL Upload to S3
  - Server Processing Trigger after upload
  - Real-time Status Updates

Fill in the server url, by default which is running on port 8000

```sh 
npm run dev
```

### 🔹 Flow:

  - User uploads a PDF (drag & drop or browse).
  - Generates a pre-signed URL from the server.
  - Uploads PDF to S3 using axios.put().
  - Triggers processing via an API request.
  - Displays upload & processing status.

This ensures secure, efficient, and interactive file uploads. 🚀