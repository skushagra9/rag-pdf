import axios from "axios";
import { useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import { NEXT_PUBLIC_API } from "./utils/consts";

const PdfUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [uploadedData, setUploadedData] = useState([]);

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
      await axios.post(`${NEXT_PUBLIC_API}/s3/upload_pdf`, {
        s3_path: s3Path,
      });
      setMessage("PDF processed and stored successfully.");
    } catch (error) {
      console.log(error);

      throw new Error("Failed to process the PDF on the server.");
    }finally{
      getAllFiles();
    }
  };

  const getAllFiles = async () => {
    try {
      const { data } = await axios.get(`${NEXT_PUBLIC_API}/s3/uploaded`);
      setUploadedData(data.files);
    } catch (error) {
      console.log(error);
    }
  };

  const handleFileUpload = async (pdfFile: File) => {
    setIsLoading(true);
    setMessage(null);

    try {
      const { data } = await axios.post(
        `${NEXT_PUBLIC_API}/s3/generate-presigned-url`,
        {
          fileName: pdfFile.name,
          fileType: pdfFile.type,
        }
      );

      const { url } = data;
      await uploadToS3(pdfFile, url);

      const s3Path = `pdfs/${pdfFile.name}`;
      await processFile(s3Path);

      setFile(pdfFile);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  };

  const onDrop = (acceptedFiles: File[]) => {
    const pdfFile = acceptedFiles.find(
      (file) => file.type === "application/pdf"
    );
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

  useEffect(() => {
    getAllFiles();
  }, []);

  return (
    <div className="flex flex-col items-center p-6">
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
      {uploadedData.length > 0 && (
            <div className="mt-2 text-sm">
              <p>Uploaded files:</p>
              <ul>
                {uploadedData.map((fileName) => (
                  <li key={fileName}>{fileName}</li>
                ))}
              </ul>
            </div>
          )}
    </div>
  );
};

export default PdfUpload;
