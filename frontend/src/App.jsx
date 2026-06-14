import { useState } from "react";
import UploadResume from "./components/UploadResume";
import ScoreCard from "./components/ScoreCard";
import ResumeTips from "./components/ResumeTips";
import { SITE } from "./config/site";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [fileName, setFileName] = useState("");

  const handleUpload = async (file) => {
    setLoading(true);
    setError("");
    setResult(null);
    setFileName(file.name);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to analyze resume.");
      }

      setResult(data.data);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          {/* <p className="author-name">{SITE.authorName}</p> */}
          <h1>{SITE.title}</h1>
          <p className="header-subtitle">{SITE.subtitle}</p>
        </div>
      </header>

      <main className="main">
        <UploadResume onUpload={handleUpload} loading={loading} />

        {error && <div className="error-banner">{error}</div>}

        {loading && (
          <div className="loading-card">
            <div className="spinner" />
            <p>Analyzing your resume...</p>
            <span>This may take a moment. Please wait.</span>
          </div>
        )}

        {!result && !loading && <ResumeTips title="Tips for a Stronger Resume" />}

        {result && !loading && (
          <ScoreCard result={result} fileName={fileName} />
        )}
      </main>

      <footer className="footer">
        <p className="footer-copy">
          © {SITE.copyrightYear} . All rights reserved.
        </p>
        <p className="footer-note">
          Built to help job seekers improve resume visibility with ATS-friendly formatting and content.
        </p>
      </footer>
    </div>
  );
}

export default App;
