import React from "react";

function LandingPage() {
  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f8fafc",
        fontFamily: "Arial, sans-serif",
        color: "#1e293b",
      }}
    >
      <nav
        style={{
          height: "70px",
          padding: "0 8%",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          backgroundColor: "white",
          borderBottom: "1px solid #e2e8f0",
        }}
      >
        <h2 style={{ color: "#2563eb" }}>
          AI Resume Optimizer
        </h2>

        <a
          href="/upload"
          style={{
            textDecoration: "none",
            backgroundColor: "#2563eb",
            color: "white",
            padding: "10px 20px",
            borderRadius: "8px",
          }}
        >
          Get Started
        </a>
      </nav>

      <main
        style={{
          maxWidth: "900px",
          margin: "0 auto",
          textAlign: "center",
          padding: "100px 20px",
        }}
      >
        <div
          style={{
            display: "inline-block",
            backgroundColor: "#dbeafe",
            color: "#2563eb",
            padding: "8px 16px",
            borderRadius: "20px",
            fontWeight: "bold",
          }}
        >
          AI-Powered Resume Analysis
        </div>

        <h1
          style={{
            fontSize: "60px",
            margin: "30px 0 20px",
          }}
        >
          Make Your Resume
          <br />
          <span style={{ color: "#2563eb" }}>
            Job-Ready
          </span>
        </h1>

        <p
          style={{
            fontSize: "19px",
            lineHeight: "1.7",
            color: "#64748b",
            maxWidth: "700px",
            margin: "0 auto 35px",
          }}
        >
          Compare your resume with any job description and get an
          instant match score, missing skills, personalized
          recommendations, and a learning roadmap.
        </p>

        <a
          href="/upload"
          style={{
            display: "inline-block",
            textDecoration: "none",
            backgroundColor: "#2563eb",
            color: "white",
            padding: "15px 30px",
            borderRadius: "10px",
            fontSize: "17px",
            fontWeight: "bold",
          }}
        >
          Analyze My Resume →
        </a>

        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "25px",
            marginTop: "80px",
            flexWrap: "wrap",
          }}
        >
          <Feature
            icon="📄"
            title="Upload Resume"
            text="PDF or DOCX"
          />

          <Feature
            icon="🎯"
            title="Match Score"
            text="Measure job compatibility"
          />

          <Feature
            icon="🚀"
            title="Improve"
            text="Get actionable recommendations"
          />
        </div>
      </main>
    </div>
  );
}

function Feature({ icon, title, text }) {
  return (
    <div
      style={{
        width: "220px",
        padding: "25px",
        backgroundColor: "white",
        borderRadius: "12px",
        boxShadow: "0 4px 15px rgba(0,0,0,0.06)",
      }}
    >
      <div style={{ fontSize: "36px" }}>{icon}</div>

      <h3>{title}</h3>

      <p style={{ color: "#64748b" }}>
        {text}
      </p>
    </div>
  );
}

export default LandingPage;