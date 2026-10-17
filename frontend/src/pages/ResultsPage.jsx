
import React from "react";
import { Link, useLocation } from "react-router-dom";

function ResultsPage() {
  const location = useLocation();

  const result = location.state?.result;
  const filename = location.state?.filename;

  // --------------------------------------------------
  // NO ANALYSIS FOUND
  // --------------------------------------------------

  if (!result) {
    return (
      <div style={styles.page}>
        <div style={styles.emptyContainer}>
          <div style={styles.emptyIcon}>📄</div>

          <h1>No Analysis Found</h1>

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

  // --------------------------------------------------
  // EXTRACT API RESPONSE
  // --------------------------------------------------

  const rawScore = Number(result.match_score);

  const matchScore = Number.isFinite(rawScore)
    ? Math.max(0, Math.min(100, rawScore))
    : 0;

  const matchedSkills = result.matched_skills || [];
  const missingSkills = result.missing_skills || [];

  const recommendations = result.recommendations || [];
  const roadmap = result.roadmap || [];

  const resumeSkills = result.resume_skills || [];
  const jobSkills = result.job_skills || [];

  // --------------------------------------------------
  // DYNAMIC SCORE COLORS
  // --------------------------------------------------

  const getScoreColor = (score) => {
    if (score >= 80) return "#16a34a";
    if (score >= 60) return "#2563eb";
    if (score >= 40) return "#d97706";
    return "#dc2626";
  };

  const getScoreBackground = (score) => {
    if (score >= 80) return "#dcfce7";
    if (score >= 60) return "#dbeafe";
    if (score >= 40) return "#fef3c7";
    return "#fee2e2";
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return "Excellent Match";
    if (score >= 60) return "Good Match";
    if (score >= 40) return "Moderate Match";
    return "Low Match";
  };

  const getScoreMessage = (score) => {
    if (score >= 80) {
      return "Excellent match! Your resume aligns strongly with this job.";
    }

    if (score >= 60) {
      return "Good match. A few improvements could make your resume stronger.";
    }

    if (score >= 40) {
      return "Moderate match. Consider adding more relevant skills.";
    }

    return "Low match. Your resume needs more alignment with this job description.";
  };

  const scoreColor = getScoreColor(matchScore);
  const scoreBackground = getScoreBackground(matchScore);

  // --------------------------------------------------
  // CIRCULAR PROGRESS CALCULATION
  // --------------------------------------------------

  const radius = 76;
  const circumference = 2 * Math.PI * radius;

  const progressOffset =
    circumference * (1 - matchScore / 100);

  return (
    <div style={styles.page}>

      {/* NAVBAR */}

      <nav style={styles.navbar}>
        <Link to="/" style={styles.logo}>
          AI Resume Optimizer
        </Link>

        <div style={styles.navLinks}>
          <Link to="/" style={styles.navLink}>
            Home
          </Link>

          <Link to="/dashboard" style={styles.navLink}>
            Dashboard
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

        {/* HEADER */}

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

        {/* ----------------------------------------
            DYNAMIC MATCH SCORE
        ---------------------------------------- */}

        <section style={styles.scoreCard}>

          <p style={styles.scoreLabel}>
            Job Match Score
          </p>

          <div
            style={styles.scoreCircleContainer}
            role="progressbar"
            aria-label="Resume job match score"
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={matchScore}
          >
            <svg
              width="200"
              height="200"
              viewBox="0 0 200 200"
              style={styles.progressSvg}
              aria-hidden="true"
            >
              {/* Background ring */}

              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="none"
                stroke="#e2e8f0"
                strokeWidth="15"
              />

              {/* Dynamic progress ring */}

              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="none"
                stroke={scoreColor}
                strokeWidth="15"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={progressOffset}
                transform="rotate(-90 100 100)"
                style={{
                  transition:
                    "stroke-dashoffset 0.6s ease, stroke 0.3s ease",
                }}
              />
            </svg>

            {/* Center percentage */}

            <div style={styles.scoreCenter}>
              <span
                style={{
                  ...styles.score,
                  color: scoreColor,
                }}
              >
                {Math.round(matchScore)}%
              </span>
            </div>
          </div>

          {/* Match quality badge */}

          <div
            style={{
              ...styles.scoreBadge,
              backgroundColor: scoreBackground,
              color: scoreColor,
            }}
          >
            {getScoreLabel(matchScore)}
          </div>

          <p style={styles.scoreMessage}>
            {getScoreMessage(matchScore)}
          </p>

          <p style={styles.scoreDisclaimer}>
            Estimated job match based on your resume and
            the provided job description.
          </p>
        </section>

        {/* ----------------------------------------
            MATCHED AND MISSING SKILLS
        ---------------------------------------- */}

        <div style={styles.twoColumnGrid}>

          {/* Matched Skills */}

          <section style={styles.card}>
            <h2 style={styles.matchedTitle}>
              ✓ Matched Skills
            </h2>

            <p style={styles.muted}>
              Skills found in both your resume and the job description.
            </p>

            {matchedSkills.length > 0 ? (
              <div style={styles.skillContainer}>
                {matchedSkills.map((skill, index) => (
                  <span
                    key={`${skill}-${index}`}
                    style={styles.matchedSkill}
                  >
                    ✓ {skill}
                  </span>
                ))}
              </div>
            ) : (
              <p style={styles.noData}>
                No matching skills were detected.
              </p>
            )}
          </section>

          {/* Missing Skills */}

          <section style={styles.card}>
            <h2 style={styles.missingTitle}>
              ⚠ Missing Skills
            </h2>

            <p style={styles.muted}>
              Skills requested by the job but not detected
              in your resume.
            </p>

            {missingSkills.length > 0 ? (
              <div style={styles.skillContainer}>
                {missingSkills.map((skill, index) => (
                  <span
                    key={`${skill}-${index}`}
                    style={styles.missingSkill}
                  >
                    {skill}
                  </span>
                ))}
              </div>
            ) : (
              <p style={styles.noData}>
                Great! No missing skills were detected.
              </p>
            )}
          </section>
        </div>

        {/* ----------------------------------------
            RECOMMENDATIONS
        ---------------------------------------- */}

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

        {/* ----------------------------------------
            LEARNING ROADMAP
        ---------------------------------------- */}

        <section style={styles.card}>
          <h2 style={styles.cardHeading}>
            🚀 Learning Roadmap
          </h2>

          <p style={styles.muted}>
            Suggested learning steps based on your missing skills.
          </p>

          {roadmap.length > 0 ? (
            <div style={styles.roadmapContainer}>
              {roadmap.map((step, index) => (
                <div
                  key={index}
                  style={styles.roadmapItem}
                >
                  <div style={styles.stepCircle}>
                    {index + 1}
                  </div>

                  <div style={styles.roadmapContent}>
                    <strong>
                      Step {index + 1}
                    </strong>

                    <p style={styles.roadmapText}>
                      {step}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p style={styles.noData}>
              No learning roadmap available.
            </p>
          )}
        </section>

        {/* ----------------------------------------
            ALL DETECTED SKILLS
        ---------------------------------------- */}

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
                {resumeSkills.map((skill, index) => (
                  <span
                    key={`${skill}-${index}`}
                    style={styles.normalSkill}
                  >
                    {skill}
                  </span>
                ))}
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
                {jobSkills.map((skill, index) => (
                  <span
                    key={`${skill}-${index}`}
                    style={styles.normalSkill}
                  >
                    {skill}
                  </span>
                ))}
              </div>
            ) : (
              <p style={styles.noData}>
                No job skills detected.
              </p>
            )}
          </section>
        </div>

        {/* ----------------------------------------
            ACTION BUTTONS
        ---------------------------------------- */}

        <div style={styles.actions}>
          <Link
            to="/upload"
            style={styles.primaryButton}
          >
            Analyze Another Resume
          </Link>

          <Link
            to="/dashboard"
            style={styles.secondaryButton}
          >
            View Dashboard
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
    gap: "16px",
    alignItems: "center",
    flexWrap: "wrap",
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
    padding: "40px 16px 80px",
  },

  header: {
    textAlign: "center",
    marginBottom: "35px",
    overflowWrap: "anywhere",
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
    fontSize: "clamp(28px, 5vw, 42px)",
    margin: "15px 0 8px",
  },

  muted: {
    color: "#64748b",
    lineHeight: "1.6",
  },

  // --------------------------------------------------
  // SCORE CARD
  // --------------------------------------------------

  scoreCard: {
    backgroundColor: "white",
    borderRadius: "18px",
    padding: "clamp(20px, 4vw, 40px)",
    textAlign: "center",
    boxShadow: "0 4px 18px rgba(0,0,0,0.06)",
    marginBottom: "25px",
  },

  scoreLabel: {
    fontSize: "19px",
    fontWeight: "bold",
    marginTop: 0,
  },

  scoreCircleContainer: {
    width: "200px",
    height: "200px",
    margin: "20px auto",
    position: "relative",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },

  progressSvg: {
    width: "200px",
    height: "200px",
    display: "block",
  },

  scoreCenter: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    pointerEvents: "none",
  },

  score: {
    fontSize: "44px",
    fontWeight: "bold",
  },

  scoreBadge: {
    display: "inline-block",
    padding: "8px 18px",
    borderRadius: "20px",
    fontWeight: "bold",
    fontSize: "14px",
    marginBottom: "12px",
  },

  scoreMessage: {
    color: "#475569",
    fontSize: "16px",
    lineHeight: "1.6",
    margin: "5px 0 0",
  },

  scoreDisclaimer: {
    color: "#94a3b8",
    fontSize: "12px",
    marginTop: "18px",
  },

  // --------------------------------------------------
  // RESULT CARDS
  // --------------------------------------------------

  twoColumnGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit, minmax(min(100%, 320px), 1fr))",
    gap: "25px",
    marginBottom: "25px",
  },

  card: {
    backgroundColor: "white",
    padding: "clamp(20px, 4vw, 30px)",
    borderRadius: "16px",
    boxShadow: "0 4px 18px rgba(0,0,0,0.06)",
    marginBottom: "25px",
    minWidth: 0,
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
    overflowWrap: "anywhere",
  },

  missingSkill: {
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    padding: "8px 13px",
    borderRadius: "20px",
    fontSize: "14px",
    fontWeight: "bold",
    overflowWrap: "anywhere",
  },

  normalSkill: {
    backgroundColor: "#eff6ff",
    color: "#1d4ed8",
    padding: "8px 13px",
    borderRadius: "20px",
    fontSize: "14px",
    overflowWrap: "anywhere",
  },

  noData: {
    color: "#94a3b8",
    fontStyle: "italic",
  },

  // --------------------------------------------------
  // RECOMMENDATIONS
  // --------------------------------------------------

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
    overflowWrap: "anywhere",
  },

  // --------------------------------------------------
  // ROADMAP
  // --------------------------------------------------

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

  roadmapContent: {
    minWidth: 0,
    flex: 1,
  },

  roadmapText: {
    margin: "6px 0 0",
    color: "#64748b",
    lineHeight: "1.6",
    overflowWrap: "anywhere",
  },

  // --------------------------------------------------
  // ACTION BUTTONS
  // --------------------------------------------------

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
    textAlign: "center",
  },

  secondaryButton: {
    backgroundColor: "white",
    color: "#2563eb",
    padding: "14px 24px",
    borderRadius: "9px",
    border: "1px solid #2563eb",
    textDecoration: "none",
    fontWeight: "bold",
    textAlign: "center",
  },

  // --------------------------------------------------
  // EMPTY STATE
  // --------------------------------------------------

  emptyContainer: {
    maxWidth: "500px",
    margin: "0 auto",
    padding: "120px 20px 40px",
    textAlign: "center",
  },

  emptyIcon: {
    fontSize: "60px",
  },
};

export default ResultsPage;
