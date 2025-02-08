# Admin Dashboard

![alt text](image.png)

## Features

The PdfUpload component allows users to upload a PDF file, store it in AWS S3, and trigger server-side processing.

### 🔹 Features:

    1. Drag & Drop Support (via react-dropzone)
    2. Pre-signed URL Upload to S3
    3. Server Processing Trigger after upload
    4. Real-time Status Updates

### 🔹 Flow:

    1. User uploads a PDF (drag & drop or browse).
    2. Generates a pre-signed URL from the server.
    3. Uploads PDF to S3 using axios.put().
    4. Triggers processing via an API request.
    5. Displays upload & processing status.

This ensures secure, efficient, and interactive file uploads. 🚀