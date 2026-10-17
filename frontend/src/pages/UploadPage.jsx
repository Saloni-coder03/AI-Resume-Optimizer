
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { analyzeResume } from "../api/apiService";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
const ALLOWED_EXTENSIONS = ["pdf", "docx"];

function UploadPage() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const navigate = useNavigate();

  // --------------------------------------------------
  // FILE VALIDATION
  // --------------------------------------------------

  const validateAndSetFile = (file) => {
    if (!file || loading) return;

    const extension = file.name
      .split(".")
      .pop()
      .toLowerCase();

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      setError("Please upload only a PDF or DOCX file.");
      setResume(null);
      return;
    }

    if (file.size === 0) {
      setError("The selected file is empty.");
      setResume(null);
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError("Resume must be 5 MB or smaller.");
      setResume(null);
      return;
    }

    setResume(file);
    setError("");
  };

  // --------------------------------------------------
  // HANDLE FILE SELECTION
  // --------------------------------------------------

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    validateAndSetFile(file);

    // Allow the same file to be selected again.
    event.target.value = "";
  };

  // --------------------------------------------------
  // DRAG AND DROP
  // --------------------------------------------------

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!loading) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!event.currentTarget.contains(event.relatedTarget)) {
      setIsDragging(false);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();

    setIsDragging(false);

    if (loading) return;

    const files = event.dataTransfer.files;

    if (!files || files.length === 0) {
      return;
    }

    if (files.length > 1) {
      setError("Please upload only one resume at a time.");
      setResume(null);
      return;
    }

    validateAndSetFile(files[0]);
  };

  // --------------------------------------------------
  // ANALYZE RESUME
  // --------------------------------------------------

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (loading) return;

    if (!resume) {
      setError("Please upload your resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    // Final check before sending to backend.
    if (resume.size > MAX_FILE_SIZE) {
      setError("Resume must be 5 MB or smaller.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      // Send resume and job description to FastAPI.
      const result = await analyzeResume(
        resume,
        jobDescription
      );

      // Navigate to results with analysis data.
      navigate("/results", {
        state: {
          result: result,
          filename: resume.name,
        },
      });
    } catch (err) {
      console.error("Analysis error:", err);

      let message =
        "Something went wrong while analyzing your resume.";

      const detail = err.response?.data?.detail;

      if (typeof detail === "string") {
        message = detail;
      }

      if (Array.isArray(detail)) {
        message = detail[0]?.msg || message;
      }

      if (!err.response) {
        message =
          "Unable to connect to the backend. Make sure FastAPI is running.";
      }

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // RENDER
  // --------------------------------------------------

  return (
    <div style={styles.page}>
      {/* Navbar */}

      <nav style={styles.navbar}>
        <Link to="/" style={styles.logo}>
          AI Resume Optimizer
        </Link>

        <Link to="/" style={styles.homeLink}>
          Home
        </Link>
      </nav>

      <main style={styles.container}>
        {/* Header */}

        <div style={styles.header}>
          <div style={styles.badge}>
            AI-Powered Resume Analysis
          </div>

          <h1 style={styles.heading}>
            Analyze Your Resume
          </h1>

          <p style={styles.subtitle}>
            Upload your resume and paste the job description
            to discover how well your profile matches the role.
          </p>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          {/* Resume Upload */}

          <section style={styles.card}>
            <div style={styles.sectionHeader}>
              <div style={styles.stepNumber}>1</div>

              <div>
                <h2 style={styles.sectionTitle}>
                  Upload Your Resume
                </h2>

                <p style={styles.sectionText}>
                  Select or drag and drop a PDF or DOCX resume
                  from your computer.
                </p>
              </div>
            </div>

            {/* Drag-and-drop upload area */}

            <div
              style={{
                ...styles.uploadBox,
                ...(isDragging ? styles.draggingBox : {}),
                ...(loading ? styles.uploadDisabled : {}),
              }}
              onDragEnter={handleDragOver}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <div style={styles.uploadIcon}>📄</div>

              <h3 style={styles.uploadTitle}>
                {isDragging
                  ? "Drop Your Resume Here"
                  : "Upload Resume"}
              </h3>

              <p style={styles.uploadText}>
                Drag and drop your resume here, or browse files.
              </p>

              <label style={styles.browseButton}>
                Browse File

                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  disabled={loading}
                  style={styles.hiddenInput}
                />
              </label>

              <p style={styles.helperText}>
                Supported formats: PDF and DOCX
              </p>

              <p style={styles.helperText}>
                Maximum file size: 5 MB
              </p>
            </div>

            {/* Selected File */}

            {resume && (
              <div style={styles.selectedFile}>
                <div style={styles.successIcon}>
                  ✓
                </div>

                <div style={styles.selectedFileDetails}>
                  <div style={styles.fileName}>
                    {resume.name}
                  </div>

                  <div style={styles.fileInfo}>
                    {(resume.size / 1024).toFixed(1)} KB
                  </div>
                </div>

                <button
                  type="button"
                  style={styles.removeButton}
                  disabled={loading}
                  onClick={() => {
                    setResume(null);
                    setError("");
                  }}
                  aria-label="Remove selected resume"
                >
                  Remove
                </button>
              </div>
            )}
          </section>

          {/* Job Description */}

          <section style={styles.card}>
            <div style={styles.sectionHeader}>
              <div style={styles.stepNumber}>2</div>

              <div>
                <h2 style={styles.sectionTitle}>
                  Paste Job Description
                </h2>

                <p style={styles.sectionText}>
                  Paste the complete job description you are
                  applying for.
                </p>
              </div>
            </div>

            <textarea
              value={jobDescription}
              onChange={(event) =>
                setJobDescription(event.target.value)
              }
              placeholder={`Paste the job description here...

Example:

We are looking for a Software Developer with experience in Python, React, SQL, Docker and AWS.

Responsibilities:
- Develop web applications
- Build REST APIs
- Work with cloud technologies
- Collaborate with engineering teams`}
              disabled={loading}
              style={styles.textarea}
            />

            <div style={styles.characterCount}>
              {jobDescription.length} characters
            </div>
          </section>

          {/* Error Message */}

          {error && (
            <div style={styles.errorBox} role="alert">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* Analyze Button */}

          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.analyzeButton,
              ...(loading ? styles.disabledButton : {}),
            }}
          >
            {loading
              ? "Analyzing Resume..."
              : "Analyze Resume →"}
          </button>

          {/* Loading Message */}

          {loading && (
            <div style={styles.loadingBox}>
              <div style={styles.loader}>⏳</div>

              <div>
                <strong>
                  Analyzing your resume...
                </strong>

                <p style={styles.loadingText}>
                  Extracting skills and comparing them with
                  the job description.
                </p>
              </div>
            </div>
          )}
        </form>
      </main>
    </div>
  );
}

// --------------------------------------------------
// STYLES
// --------------------------------------------------

const styles = {
  page: {
    minHeight: "100vh",
    backgroundColor: "#f8fafc",
    fontFamily: "Arial, sans-serif",
    color: "#1e293b",
  },

  navbar: {
    minHeight: "70px",
    padding: "12px 8%",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "16px",
    flexWrap: "wrap",
    backgroundColor: "white",
    borderBottom: "1px solid #e2e8f0",
  },

  logo: {
    color: "#2563eb",
    fontSize: "22px",
    fontWeight: "bold",
    textDecoration: "none",
  },

  homeLink: {
    color: "#475569",
    textDecoration: "none",
    fontWeight: "bold",
  },

  container: {
    maxWidth: "850px",
    margin: "0 auto",
    padding: "55px 20px 80px",
  },

  header: {
    textAlign: "center",
    marginBottom: "40px",
  },

  badge: {
    display: "inline-block",
    backgroundColor: "#dbeafe",
    color: "#2563eb",
    padding: "7px 15px",
    borderRadius: "20px",
    fontSize: "13px",
    fontWeight: "bold",
    marginBottom: "15px",
  },

  heading: {
    fontSize: "clamp(28px, 5vw, 42px)",
    margin: "10px 0",
  },

  subtitle: {
    color: "#64748b",
    fontSize: "17px",
    lineHeight: "1.6",
    maxWidth: "650px",
    margin: "0 auto",
  },

  form: {
    display: "flex",
    flexDirection: "column",
    gap: "25px",
  },

  card: {
    backgroundColor: "white",
    padding: "clamp(18px, 4vw, 30px)",
    borderRadius: "16px",
    boxShadow: "0 4px 18px rgba(0,0,0,0.06)",
  },

  sectionHeader: {
    display: "flex",
    alignItems: "flex-start",
    gap: "15px",
    marginBottom: "25px",
  },

  stepNumber: {
    minWidth: "38px",
    height: "38px",
    borderRadius: "50%",
    backgroundColor: "#2563eb",
    color: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "bold",
  },

  sectionTitle: {
    margin: 0,
    fontSize: "21px",
  },

  sectionText: {
    margin: "6px 0 0",
    color: "#64748b",
    fontSize: "14px",
    lineHeight: "1.5",
  },

  uploadBox: {
    display: "block",
    textAlign: "center",
    border: "2px dashed #93c5fd",
    backgroundColor: "#f8fbff",
    borderRadius: "14px",
    padding: "40px 20px",
    transition: "all 0.2s ease",
  },

  draggingBox: {
    borderColor: "#2563eb",
    backgroundColor: "#dbeafe",
    boxShadow: "0 0 0 4px rgba(37,99,235,0.1)",
  },

  uploadDisabled: {
    opacity: 0.65,
    cursor: "not-allowed",
  },

  uploadIcon: {
    fontSize: "48px",
  },

  uploadTitle: {
    margin: "12px 0 5px",
  },

  uploadText: {
    color: "#64748b",
    marginBottom: "20px",
  },

  hiddenInput: {
    display: "none",
  },

  browseButton: {
    display: "inline-block",
    backgroundColor: "#2563eb",
    color: "white",
    padding: "11px 22px",
    borderRadius: "8px",
    fontWeight: "bold",
    cursor: "pointer",
  },

  helperText: {
    color: "#94a3b8",
    fontSize: "12px",
    marginTop: "12px",
  },

  selectedFile: {
    marginTop: "18px",
    padding: "14px",
    borderRadius: "10px",
    backgroundColor: "#f0fdf4",
    border: "1px solid #bbf7d0",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    flexWrap: "wrap",
  },

  successIcon: {
    width: "35px",
    height: "35px",
    borderRadius: "50%",
    backgroundColor: "#22c55e",
    color: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "bold",
  },

  selectedFileDetails: {
    flex: "1 1 160px",
    minWidth: 0,
    overflowWrap: "anywhere",
  },

  fileName: {
    fontWeight: "bold",
    color: "#166534",
  },

  fileInfo: {
    color: "#64748b",
    fontSize: "12px",
    marginTop: "3px",
  },

  removeButton: {
    backgroundColor: "white",
    border: "1px solid #fecaca",
    color: "#dc2626",
    borderRadius: "8px",
    padding: "8px 12px",
    cursor: "pointer",
  },

  textarea: {
    width: "100%",
    minHeight: "280px",
    padding: "17px",
    boxSizing: "border-box",
    border: "1px solid #cbd5e1",
    borderRadius: "10px",
    resize: "vertical",
    fontFamily: "Arial, sans-serif",
    fontSize: "15px",
    lineHeight: "1.6",
    outlineColor: "#2563eb",
  },

  characterCount: {
    textAlign: "right",
    color: "#94a3b8",
    fontSize: "12px",
    marginTop: "8px",
  },

  errorBox: {
    display: "flex",
    gap: "10px",
    alignItems: "center",
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    padding: "14px",
    borderRadius: "9px",
  },

  analyzeButton: {
    width: "100%",
    border: "none",
    backgroundColor: "#2563eb",
    color: "white",
    padding: "17px",
    borderRadius: "10px",
    fontSize: "17px",
    fontWeight: "bold",
    cursor: "pointer",
  },

  disabledButton: {
    backgroundColor: "#93c5fd",
    cursor: "not-allowed",
  },

  loadingBox: {
    backgroundColor: "#eff6ff",
    border: "1px solid #bfdbfe",
    padding: "18px",
    borderRadius: "10px",
    display: "flex",
    gap: "15px",
    alignItems: "center",
  },

  loader: {
    fontSize: "28px",
  },

  loadingText: {
    color: "#64748b",
    margin: "5px 0 0",
    fontSize: "14px",
  },
};

export default UploadPage;
