import axios from "axios";
import { useState } from "react";
import { useDropzone } from "react-dropzone";

const PdfUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const uploadToS3 = async (pdfFile: File, presignedUrl: string) => {
    try {
      await axios.put(presignedUrl, pdfFile, {
        headers: { "Content-Type": pdfFile.type },
      });
    } catch (error) {
      console.log(error);
      throw new Error("Failed to upload the file to S3.");
    }
  };

  const processFile = async (s3Path: string) => {
    try {
      const formData = new FormData();
      formData.append("s3_path", s3Path);
      await axios.post("http://localhost:8000/upload_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("PDF processed and stored successfully.");
    } catch (error) {
      console.log(error);

      throw new Error("Failed to process the PDF on the server.");
    }
  };

  const handleFileUpload = async (pdfFile: File) => {
    setIsLoading(true);
    setMessage(null);

    try {
      // Generate pre-signed URL
      const formData = new FormData();
      formData.append("fileName", pdfFile.name);
      formData.append("fileType", pdfFile.type);

      const { data } = await axios.post(
        "http://localhost:8000/generate-presigned-url",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      const { url } = data;

      // Upload file to S3
      await uploadToS3(pdfFile, url);

      // Process the uploaded file
      const s3Path = `pdfs/${pdfFile.name}`;
      await processFile(s3Path);

      setFile(pdfFile);
    } catch (error) {
      console.log(error);
      // setMessage(error || "An error occurred during the upload process.");
    } finally {
      setIsLoading(false);
    }
  };

  const onDrop = (acceptedFiles: File[]) => {
    const pdfFile = acceptedFiles.find((file) => file.type === "application/pdf");
    if (!pdfFile) {
      setMessage("Only PDF files are allowed!");
      return;
    }
    handleFileUpload(pdfFile);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
  });

  return (
    <div className="flex flex-col items-center p-6">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-md p-6 w-full max-w-lg text-center cursor-pointer transition ${
          isDragActive ? "border-blue-500 bg-blue-100" : "border-gray-300"
        }`}
      >
        <input {...getInputProps()} />
        {isLoading ? (
          <p>Uploading and processing your PDF file...</p>
        ) : file ? (
          <p>File "{file.name}" uploaded successfully!</p>
        ) : isDragActive ? (
          <p>Drop the PDF file here...</p>
        ) : (
          <p>Drag and drop your PDF file here, or click to browse.</p>
        )}
      </div>

      {/* Display the uploaded file details */}
      {file && (
        <div className="mt-4 w-full max-w-lg text-center">
          <h3 className="text-lg font-semibold mb-2">Uploaded File:</h3>
          <p className="text-gray-700">{file.name}</p>
        </div>
      )}

      {/* Status message */}
      {message && (
        <div
          className={`mt-4 w-full max-w-lg text-center p-3 rounded-md ${
            message.includes("success")
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
};

export default PdfUpload;
