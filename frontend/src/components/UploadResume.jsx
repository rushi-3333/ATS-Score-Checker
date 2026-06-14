import { useRef } from "react";
import "./UploadResume.css";

function UploadResume({ onUpload, loading }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (loading) return;
    const file = e.dataTransfer.files?.[0];
    if (file && file.type === "application/pdf") {
      onUpload(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div
      className={`upload-zone ${loading ? "disabled" : ""}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onClick={() => !loading && fileInputRef.current?.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
        hidden
        disabled={loading}
      />

      <div className="upload-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M12 16V4m0 0l-4 4m4-4l4 4" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2" strokeLinecap="round" />
        </svg>
      </div>

      <h3>Upload Your Resume</h3>
      <p>Drag & drop a PDF here, or click to browse</p>
      <span className="upload-hint">PDF only · Max recommended 5 MB</span>
    </div>
  );
}

export default UploadResume;
