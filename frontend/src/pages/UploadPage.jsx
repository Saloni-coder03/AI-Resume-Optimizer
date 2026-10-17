
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import APP_CONFIG from "../config/appConfig";
import { analyzeResume } from "../api/apiService";

const MAX_FILE_SIZE = APP_CONFIG.MAX_FILE_SIZE_BYTES;

const ALLOWED_EXTENSIONS =
  APP_CONFIG.ALLOWED_FILE_EXTENSIONS.map((extension) =>
    extension.replace(/^\./, "").toLowerCase()
  );

function UploadPage() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const navigate = useNavigate();

  // --------------------------------------------------
  // VALIDATE AND STORE FILE
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
      setError(
        `Resume must be ${APP_CONFIG.MAX_FILE_SIZE_MB} MB or smaller.`
      );
      setResume(null);
      return;
    }

    setResume(file);
    setError("");
  };

  // --------------------------------------------------
  // FILE SELECTION
  // --------------------------------------------------

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    validateAndSetFile(file);

    // Allow selecting the same file again.
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
  // SUBMIT ANALYSIS
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

    if (resume.size > MAX_FILE_SIZE) {
      setError(
        `Resume must be ${APP_CONFIG.MAX_FILE_SIZE_MB} MB or smaller.`
      );
      return;
    }

    try {
      setLoading(true);
      setError("");

      const result = await analyzeResume(
        resume,
        jobDescription.trim()
      );

      navigate(APP_CONFIG.ROUTES.RESULTS, {
        state: {
          result,
          filename: resume.name,
        },
      });
    } catch (err) {
      console.error("Analysis error:", err);

      const detail = err.response?.data?.detail;

      let message =
        "Something went wrong while analyzing your resume.";

      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        message = detail[0]?.msg || message;
      } else if (!err.response) {
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
      <nav style={styles.navbar}>
        <Link
          to={APP_CONFIG.ROUTES.HOME}
          style={styles.logo}
        >
          {APP_CONFIG.APP_NAME}
        </Link>

        <div style={styles.navLinks}>
          <Link
            to={APP_CONFIG.ROUTES.HOME}
            style={styles.navLink}
          >
            Home
          </Link>

          <Link
            to={APP_CONFIG.ROUTES.DASHBOARD}
            style={styles.navLink}
          >
            Dashboard
          </Link>
        </div>
      </nav>

      <main style={styles.container}>
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
          {/* UPLOAD SECTION */}

          <section style={styles.card}>
            <div style={styles.sectionHeader}>
              <div style={styles.stepNumber}>1</div>

              <div>
                <h2 style={styles.sectionTitle}>
                  Upload Your Resume
                </h2>

                <p style={styles.sectionText}>
                  Select or drag and drop a PDF or DOCX resume.
                </p>
              </div>
            </div>

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
                  accept={APP_CONFIG.ALLOWED_FILE_EXTENSIONS.join(",")}
                  onChange={handleFileChange}
                  disabled={loading}
                  style={styles.hiddenInput}
                />
              </label>

              <p style={styles.helperText}>
                PDF and DOCX only • Maximum{" "}
                {APP_CONFIG.MAX_FILE_SIZE_MB} MB
              </p>
            </div>

            {resume && (
              <div style={styles.selectedFile}>
                <div style={styles.successIcon}>✓</div>

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

          {/* JOB DESCRIPTION SECTION */}

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
              placeholder="Paste the job description here..."
              disabled={loading}
              style={styles.textarea}
            />

            <div style={styles.characterCount}>
              {jobDescription.length} characters
            </div>
          </section>

          {error && (
            <div style={styles.errorBox} role="alert">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

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

          {loading && (
            <div style={styles.loadingBox}>
              <span style={styles.loader}>⏳</span>

              <div>
                <strong>Analyzing your resume...</strong>

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
    padding: "12px 5%",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "16px",
    backgroundColor: "#ffffff",
    borderBottom: "1px solid #e2e8f0",
  },

  logo: {
    color: "#2563eb",
    fontSize: "22px",
    fontWeight: "bold",
    textDecoration: "none",
  },

  navLinks: {
    display: "flex",
    alignItems: "center",
    gap: "18px",
    flexWrap: "wrap",
  },

  navLink: {
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
    lineHeight: 1.6,
    maxWidth: "650px",
    margin: "0 auto",
  },

  form: {
    display: "flex",
    flexDirection: "column",
    gap: "25px",
  },

  card: {
    backgroundColor: "#ffffff",
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
    color: "#ffffff",
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
    lineHeight: 1.5,
  },

  uploadBox: {
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
    color: "#ffffff",
    padding: "11px 22px",
    borderRadius: "8px",
    fontWeight: "bold",
    cursor: "pointer",
  },

  helperText: {
    color: "#94a3b8",
    fontSize: "12px",
    marginTop: "16px",
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
    color: "#ffffff",
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
    backgroundColor: "#ffffff",
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
    lineHeight: 1.6,
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
    alignItems: "center",
    gap: "10px",
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    padding: "14px",
    borderRadius: "9px",
  },

  analyzeButton: {
    width: "100%",
    border: "none",
    backgroundColor: "#2563eb",
    color: "#ffffff",
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
    display: "flex",
    gap: "15px",
    alignItems: "center",
    backgroundColor: "#eff6ff",
    border: "1px solid #bfdbfe",
    padding: "18px",
    borderRadius: "10px",
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
