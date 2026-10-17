import React from "react";

import {
  Link,
} from "react-router-dom";


function LandingPage() {
  return (
    <div style={styles.page}>

      {/* --------------------------------
          NAVBAR
      -------------------------------- */}

      <nav style={styles.navbar}>

        <Link
          to="/"
          style={styles.logo}
        >
          AI Resume Optimizer
        </Link>


        <div style={styles.navLinks}>

          <Link
            to="/dashboard"
            style={styles.dashboardLink}
          >
            Dashboard
          </Link>


          <Link
            to="/upload"
            style={styles.getStartedButton}
          >
            Get Started
          </Link>

        </div>

      </nav>


      {/* --------------------------------
          HERO
      -------------------------------- */}

      <main style={styles.hero}>

        <div style={styles.badge}>
          AI-Powered Resume Analysis
        </div>


        <h1 style={styles.heading}>

          Make Your Resume

          <br />

          <span style={styles.highlight}>
            Job-Ready
          </span>

        </h1>


        <p style={styles.description}>

          Compare your resume with any job
          description and discover how well
          your profile matches the role.

          Get an instant match score,
          identify missing skills,
          receive personalized recommendations,
          and follow a learning roadmap.

        </p>


        {/* MAIN BUTTONS */}

        <div style={styles.heroButtons}>

          <Link
            to="/upload"
            style={styles.mainButton}
          >
            Analyze My Resume →
          </Link>


          <Link
            to="/dashboard"
            style={styles.secondaryButton}
          >
            View Dashboard
          </Link>

        </div>


        {/* --------------------------------
            FEATURES
        -------------------------------- */}

        <div style={styles.features}>

          <Feature
            icon="📄"
            title="Upload Resume"
            text="Upload your resume in PDF or DOCX format."
          />


          <Feature
            icon="🎯"
            title="Match Score"
            text="Measure how closely your resume matches the job."
          />


          <Feature
            icon="💡"
            title="Recommendations"
            text="Get actionable resume improvement suggestions."
          />


          <Feature
            icon="🚀"
            title="Learning Roadmap"
            text="Discover which skills you should learn next."
          />

        </div>

      </main>


      {/* --------------------------------
          FOOTER
      -------------------------------- */}

      <footer style={styles.footer}>

        AI Resume Optimizer © 2026

      </footer>

    </div>
  );
}


function Feature({
  icon,
  title,
  text,
}) {

  return (
    <div style={styles.featureCard}>

      <div style={styles.featureIcon}>
        {icon}
      </div>

      <h3 style={styles.featureTitle}>
        {title}
      </h3>

      <p style={styles.featureText}>
        {text}
      </p>

    </div>
  );
}


const styles = {

  page: {
    minHeight: "100vh",
    backgroundColor: "#f8fafc",
    color: "#1e293b",
    fontFamily: "Arial, sans-serif",
  },


  /* NAVBAR */

  navbar: {
    height: "70px",
    padding: "0 8%",
    backgroundColor: "white",
    borderBottom:
      "1px solid #e2e8f0",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
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
    gap: "22px",
  },


  dashboardLink: {
    color: "#475569",
    textDecoration: "none",
    fontWeight: "bold",
  },


  getStartedButton: {
    backgroundColor: "#2563eb",
    color: "white",
    padding: "10px 20px",
    borderRadius: "8px",
    textDecoration: "none",
    fontWeight: "bold",
  },


  /* HERO */

  hero: {
    maxWidth: "1050px",
    margin: "0 auto",
    textAlign: "center",
    padding: "90px 20px 100px",
  },


  badge: {
    display: "inline-block",
    backgroundColor: "#dbeafe",
    color: "#2563eb",
    padding: "8px 16px",
    borderRadius: "20px",
    fontSize: "14px",
    fontWeight: "bold",
  },


  heading: {
    fontSize: "60px",
    lineHeight: "1.1",
    margin: "28px 0 22px",
  },


  highlight: {
    color: "#2563eb",
  },


  description: {
    maxWidth: "750px",
    margin: "0 auto",
    color: "#64748b",
    fontSize: "18px",
    lineHeight: "1.8",
  },


  heroButtons: {
    marginTop: "35px",
    display: "flex",
    justifyContent: "center",
    gap: "15px",
    flexWrap: "wrap",
  },


  mainButton: {
    backgroundColor: "#2563eb",
    color: "white",
    padding: "15px 28px",
    borderRadius: "10px",
    textDecoration: "none",
    fontSize: "17px",
    fontWeight: "bold",
  },


  secondaryButton: {
    backgroundColor: "white",
    color: "#2563eb",
    padding: "15px 28px",
    borderRadius: "10px",
    border:
      "1px solid #2563eb",
    textDecoration: "none",
    fontSize: "17px",
    fontWeight: "bold",
  },


  /* FEATURES */

  features: {
    marginTop: "80px",
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit, minmax(210px, 1fr))",
    gap: "22px",
  },


  featureCard: {
    backgroundColor: "white",
    padding: "28px 22px",
    borderRadius: "14px",
    boxShadow:
      "0 4px 18px rgba(0,0,0,0.05)",
  },


  featureIcon: {
    fontSize: "40px",
    marginBottom: "12px",
  },


  featureTitle: {
    margin: "0 0 10px",
  },


  featureText: {
    color: "#64748b",
    lineHeight: "1.6",
    fontSize: "14px",
    margin: 0,
  },


  /* FOOTER */

  footer: {
    textAlign: "center",
    padding: "25px",
    color: "#64748b",
    backgroundColor: "white",
    borderTop:
      "1px solid #e2e8f0",
  },

};


export default LandingPage;