import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { analyzeResume } from "../api/apiService";


function UploadPage() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();


  // Handle resume selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    const extension = file.name
      .split(".")
      .pop()
      .toLowerCase();

    if (!["pdf", "docx"].includes(extension)) {
      setError(
        "Please upload only a PDF or DOCX file."
      );

      setResume(null);
      return;
    }

    setResume(file);
    setError("");
  };


  // Analyze resume
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!resume) {
      setError(
        "Please upload your resume."
      );

      return;
    }

    if (!jobDescription.trim()) {
      setError(
        "Please enter a job description."
      );

      return;
    }

    try {
      setLoading(true);
      setError("");

      // Send resume + job description to FastAPI
      const result = await analyzeResume(
        resume,
        jobDescription
      );

      console.log(
        "Analysis result:",
        result
      );

      // Send result to Results page
      navigate(
        "/results",
        {
          state: {
            result: result,
            filename: resume.name,
          },
        }
      );

    } catch (err) {
      console.error(
        "Analysis error:",
        err
      );

      let message =
        "Something went wrong while analyzing your resume.";

      const detail =
        err.response?.data?.detail;

      if (typeof detail === "string") {
        message = detail;
      }

      if (Array.isArray(detail)) {
        message =
          detail[0]?.msg ||
          message;
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


  return (
    <div style={styles.page}>

      {/* Navbar */}

      <nav style={styles.navbar}>

        <Link
          to="/"
          style={styles.logo}
        >
          AI Resume Optimizer
        </Link>

        <Link
          to="/"
          style={styles.homeLink}
        >
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


        <form
          onSubmit={handleSubmit}
          style={styles.form}
        >

          {/* Resume Upload */}

          <section style={styles.card}>

            <div style={styles.sectionHeader}>

              <div style={styles.stepNumber}>
                1
              </div>

              <div>

                <h2 style={styles.sectionTitle}>
                  Upload Your Resume
                </h2>

                <p style={styles.sectionText}>
                  Select a PDF or DOCX resume from your computer.
                </p>

              </div>

            </div>


            <label style={styles.uploadBox}>

              <div style={styles.uploadIcon}>
                📄
              </div>

              <h3 style={styles.uploadTitle}>
                Upload Resume
              </h3>

              <p style={styles.uploadText}>
                Click below to choose your file
              </p>


              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                disabled={loading}
                style={styles.hiddenInput}
              />


              <span style={styles.browseButton}>
                Browse File
              </span>


              <p style={styles.helperText}>
                Supported formats: PDF and DOCX
              </p>

            </label>


            {/* Selected file */}

            {resume && (

              <div style={styles.selectedFile}>

                <div style={styles.successIcon}>
                  ✓
                </div>

                <div>

                  <div style={styles.fileName}>
                    {resume.name}
                  </div>

                  <div style={styles.fileInfo}>
                    {(resume.size / 1024).toFixed(1)} KB
                  </div>

                </div>

              </div>

            )}

          </section>


          {/* Job Description */}

          <section style={styles.card}>

            <div style={styles.sectionHeader}>

              <div style={styles.stepNumber}>
                2
              </div>

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
                setJobDescription(
                  event.target.value
                )
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

            <div style={styles.errorBox}>

              <span>
                ⚠️
              </span>

              <span>
                {error}
              </span>

            </div>

          )}


          {/* Analyze Button */}

          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.analyzeButton,

              ...(loading
                ? styles.disabledButton
                : {}),
            }}
          >

            {loading
              ? "Analyzing Resume..."
              : "Analyze Resume →"}

          </button>


          {/* Loading Message */}

          {loading && (

            <div style={styles.loadingBox}>

              <div style={styles.loader}>
                ⏳
              </div>

              <div>

                <strong>
                  Analyzing your resume...
                </strong>

                <p style={styles.loadingText}>
                  Extracting skills and comparing them
                  with the job description.
                </p>

              </div>

            </div>

          )}

        </form>

      </main>

    </div>
  );
}


const styles = {

  page: {
    minHeight: "100vh",
    backgroundColor: "#f8fafc",
    fontFamily: "Arial, sans-serif",
    color: "#1e293b",
  },


  navbar: {
    height: "70px",
    padding: "0 8%",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
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
    fontSize: "42px",
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
    padding: "30px",
    borderRadius: "16px",
    boxShadow:
      "0 4px 18px rgba(0,0,0,0.06)",
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
    cursor: "pointer",
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


  fileName: {
    fontWeight: "bold",
    color: "#166534",
  },


  fileInfo: {
    color: "#64748b",
    fontSize: "12px",
    marginTop: "3px",
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