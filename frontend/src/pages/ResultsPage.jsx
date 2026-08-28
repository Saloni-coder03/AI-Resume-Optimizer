import React from "react";
import {
  Link,
  useLocation,
} from "react-router-dom";


function ResultsPage() {
  const location = useLocation();

  const result = location.state?.result;
  const filename = location.state?.filename;


  // If user opens /results directly
  if (!result) {
    return (
      <div style={styles.page}>

        <div style={styles.emptyContainer}>

          <div style={styles.emptyIcon}>
            📄
          </div>

          <h1>
            No Analysis Found
          </h1>

          <p style={styles.muted}>
            Please upload and analyze a resume first.
          </p>

          <Link
            to="/upload"
            style={styles.primaryButton}
          >
            Analyze Resume
          </Link>

        </div>

      </div>
    );
  }


  const matchScore =
    result.match_score || 0;

  const matchedSkills =
    result.matched_skills || [];

  const missingSkills =
    result.missing_skills || [];

  const recommendations =
    result.recommendations || [];

  const roadmap =
    result.roadmap || [];

  const resumeSkills =
    result.resume_skills || [];

  const jobSkills =
    result.job_skills || [];


  // Score message
  const getScoreMessage = () => {

    if (matchScore >= 80) {
      return "Excellent match! Your resume aligns strongly with this job.";
    }

    if (matchScore >= 60) {
      return "Good match. A few improvements could make your resume stronger.";
    }

    if (matchScore >= 40) {
      return "Moderate match. Consider adding more relevant skills.";
    }

    return "Low match. Your resume needs more alignment with this job description.";
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

        <div style={styles.navLinks}>

          <Link
            to="/"
            style={styles.navLink}
          >
            Home
          </Link>

          <Link
            to="/upload"
            style={styles.newAnalysisButton}
          >
            New Analysis
          </Link>

        </div>

      </nav>


      <main style={styles.container}>

        {/* Header */}

        <div style={styles.header}>

          <div style={styles.successBadge}>
            ✓ Analysis Complete
          </div>

          <h1 style={styles.heading}>
            Your Resume Results
          </h1>

          {filename && (
            <p style={styles.muted}>
              Resume analyzed: {filename}
            </p>
          )}

        </div>


        {/* Match Score */}

        <section style={styles.scoreCard}>

          <p style={styles.scoreLabel}>
            Job Match Score
          </p>

          <div style={styles.scoreCircle}>

            <span style={styles.score}>
              {Math.round(matchScore)}%
            </span>

          </div>

          <p style={styles.scoreMessage}>
            {getScoreMessage()}
          </p>

        </section>


        {/* Matched + Missing Skills */}

        <div style={styles.twoColumnGrid}>

          {/* Matched */}

          <section style={styles.card}>

            <h2 style={styles.matchedTitle}>
              ✓ Matched Skills
            </h2>

            <p style={styles.muted}>
              Skills found in both your resume and the job description.
            </p>

            {matchedSkills.length > 0 ? (

              <div style={styles.skillContainer}>

                {matchedSkills.map(
                  (skill, index) => (

                    <span
                      key={index}
                      style={styles.matchedSkill}
                    >
                      ✓ {skill}
                    </span>

                  )
                )}

              </div>

            ) : (

              <p style={styles.noData}>
                No matching skills were detected.
              </p>

            )}

          </section>


          {/* Missing */}

          <section style={styles.card}>

            <h2 style={styles.missingTitle}>
              ⚠ Missing Skills
            </h2>

            <p style={styles.muted}>
              Skills requested by the job but not detected in your resume.
            </p>

            {missingSkills.length > 0 ? (

              <div style={styles.skillContainer}>

                {missingSkills.map(
                  (skill, index) => (

                    <span
                      key={index}
                      style={styles.missingSkill}
                    >
                      {skill}
                    </span>

                  )
                )}

              </div>

            ) : (

              <p style={styles.noData}>
                Great! No missing skills were detected.
              </p>

            )}

          </section>

        </div>


        {/* Recommendations */}

        <section style={styles.card}>

          <h2 style={styles.cardHeading}>
            💡 Resume Recommendations
          </h2>

          <p style={styles.muted}>
            Use these suggestions to improve your resume.
          </p>


          {recommendations.length > 0 ? (

            <div style={styles.listContainer}>

              {recommendations.map(
                (recommendation, index) => (

                  <div
                    key={index}
                    style={styles.recommendationItem}
                  >

                    <div style={styles.numberCircle}>
                      {index + 1}
                    </div>

                    <div style={styles.itemText}>
                      {recommendation}
                    </div>

                  </div>

                )
              )}

            </div>

          ) : (

            <p style={styles.noData}>
              No recommendations available.
            </p>

          )}

        </section>


        {/* Learning Roadmap */}

        <section style={styles.card}>

          <h2 style={styles.cardHeading}>
            🚀 Learning Roadmap
          </h2>

          <p style={styles.muted}>
            Suggested learning steps based on your missing skills.
          </p>


          {roadmap.length > 0 ? (

            <div style={styles.roadmapContainer}>

              {roadmap.map(
                (step, index) => (

                  <div
                    key={index}
                    style={styles.roadmapItem}
                  >

                    <div style={styles.stepCircle}>
                      {index + 1}
                    </div>

                    <div>

                      <strong>
                        Step {index + 1}
                      </strong>

                      <p style={styles.roadmapText}>
                        {step}
                      </p>

                    </div>

                  </div>

                )
              )}

            </div>

          ) : (

            <p style={styles.noData}>
              No learning roadmap available.
            </p>

          )}

        </section>


        {/* All Detected Skills */}

        <div style={styles.twoColumnGrid}>

          {/* Resume Skills */}

          <section style={styles.card}>

            <h2 style={styles.cardHeading}>
              📄 Resume Skills
            </h2>

            <p style={styles.muted}>
              All skills detected in your resume.
            </p>


            {resumeSkills.length > 0 ? (

              <div style={styles.skillContainer}>

                {resumeSkills.map(
                  (skill, index) => (

                    <span
                      key={index}
                      style={styles.normalSkill}
                    >
                      {skill}
                    </span>

                  )
                )}

              </div>

            ) : (

              <p style={styles.noData}>
                No skills detected.
              </p>

            )}

          </section>


          {/* Job Skills */}

          <section style={styles.card}>

            <h2 style={styles.cardHeading}>
              💼 Job Skills
            </h2>

            <p style={styles.muted}>
              Skills detected from the job description.
            </p>


            {jobSkills.length > 0 ? (

              <div style={styles.skillContainer}>

                {jobSkills.map(
                  (skill, index) => (

                    <span
                      key={index}
                      style={styles.normalSkill}
                    >
                      {skill}
                    </span>

                  )
                )}

              </div>

            ) : (

              <p style={styles.noData}>
                No job skills detected.
              </p>

            )}

          </section>

        </div>


        {/* Bottom Buttons */}

        <div style={styles.actions}>

          <Link
            to="/upload"
            style={styles.primaryButton}
          >
            Analyze Another Resume
          </Link>

          <Link
            to="/"
            style={styles.secondaryButton}
          >
            Back to Home
          </Link>

        </div>

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


  navLinks: {
    display: "flex",
    gap: "20px",
    alignItems: "center",
  },


  navLink: {
    color: "#475569",
    textDecoration: "none",
    fontWeight: "bold",
  },


  newAnalysisButton: {
    backgroundColor: "#2563eb",
    color: "white",
    textDecoration: "none",
    padding: "10px 18px",
    borderRadius: "8px",
    fontWeight: "bold",
  },


  container: {
    maxWidth: "1050px",
    margin: "0 auto",
    padding: "50px 20px 80px",
  },


  header: {
    textAlign: "center",
    marginBottom: "35px",
  },


  successBadge: {
    display: "inline-block",
    backgroundColor: "#dcfce7",
    color: "#15803d",
    padding: "8px 16px",
    borderRadius: "20px",
    fontWeight: "bold",
    fontSize: "13px",
  },


  heading: {
    fontSize: "42px",
    margin: "15px 0 8px",
  },


  muted: {
    color: "#64748b",
    lineHeight: "1.6",
  },


  scoreCard: {
    backgroundColor: "white",
    borderRadius: "18px",
    padding: "40px",
    textAlign: "center",
    boxShadow:
      "0 4px 18px rgba(0,0,0,0.06)",
    marginBottom: "25px",
  },


  scoreLabel: {
    fontSize: "19px",
    fontWeight: "bold",
    marginTop: 0,
  },


  scoreCircle: {
    width: "150px",
    height: "150px",
    borderRadius: "50%",
    backgroundColor: "#eff6ff",
    border: "10px solid #2563eb",
    margin: "20px auto",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },


  score: {
    fontSize: "48px",
    color: "#2563eb",
    fontWeight: "bold",
  },


  scoreMessage: {
    color: "#475569",
    fontSize: "16px",
    marginBottom: 0,
  },


  twoColumnGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit, minmax(320px, 1fr))",
    gap: "25px",
    marginBottom: "25px",
  },


  card: {
    backgroundColor: "white",
    padding: "30px",
    borderRadius: "16px",
    boxShadow:
      "0 4px 18px rgba(0,0,0,0.06)",
    marginBottom: "25px",
  },


  cardHeading: {
    marginTop: 0,
  },


  matchedTitle: {
    color: "#16a34a",
    marginTop: 0,
  },


  missingTitle: {
    color: "#dc2626",
    marginTop: 0,
  },


  skillContainer: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap",
    marginTop: "20px",
  },


  matchedSkill: {
    backgroundColor: "#dcfce7",
    color: "#166534",
    padding: "8px 13px",
    borderRadius: "20px",
    fontSize: "14px",
    fontWeight: "bold",
  },


  missingSkill: {
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    padding: "8px 13px",
    borderRadius: "20px",
    fontSize: "14px",
    fontWeight: "bold",
  },


  normalSkill: {
    backgroundColor: "#eff6ff",
    color: "#1d4ed8",
    padding: "8px 13px",
    borderRadius: "20px",
    fontSize: "14px",
  },


  noData: {
    color: "#94a3b8",
    fontStyle: "italic",
  },


  listContainer: {
    marginTop: "20px",
  },


  recommendationItem: {
    display: "flex",
    gap: "15px",
    alignItems: "flex-start",
    backgroundColor: "#f8fafc",
    padding: "16px",
    borderRadius: "10px",
    marginBottom: "12px",
  },


  numberCircle: {
    minWidth: "34px",
    height: "34px",
    borderRadius: "50%",
    backgroundColor: "#dbeafe",
    color: "#2563eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "bold",
  },


  itemText: {
    lineHeight: "1.6",
    paddingTop: "5px",
  },


  roadmapContainer: {
    marginTop: "25px",
  },


  roadmapItem: {
    display: "flex",
    gap: "18px",
    alignItems: "flex-start",
    marginBottom: "25px",
  },


  stepCircle: {
    minWidth: "42px",
    height: "42px",
    borderRadius: "50%",
    backgroundColor: "#2563eb",
    color: "white",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontWeight: "bold",
  },


  roadmapText: {
    margin: "6px 0 0",
    color: "#64748b",
    lineHeight: "1.6",
  },


  actions: {
    display: "flex",
    justifyContent: "center",
    gap: "15px",
    flexWrap: "wrap",
    marginTop: "20px",
  },


  primaryButton: {
    backgroundColor: "#2563eb",
    color: "white",
    padding: "14px 24px",
    borderRadius: "9px",
    textDecoration: "none",
    fontWeight: "bold",
  },


  secondaryButton: {
    backgroundColor: "white",
    color: "#2563eb",
    padding: "14px 24px",
    borderRadius: "9px",
    border: "1px solid #2563eb",
    textDecoration: "none",
    fontWeight: "bold",
  },


  emptyContainer: {
    maxWidth: "500px",
    margin: "0 auto",
    paddingTop: "150px",
    textAlign: "center",
  },


  emptyIcon: {
    fontSize: "60px",
  },

};


export default ResultsPage;