import React, {
  useEffect,
  useState,
} from "react";

import {
  Link,
} from "react-router-dom";

import {
  getDashboardStats,
  getMatchHistory,
  deleteHistoryItem,
  clearMatchHistory,
} from "../api/apiService";


function Dashboard() {
  const [stats, setStats] = useState({
    total_analyses: 0,
    average_score: 0,
    best_score: 0,
  });

  const [history, setHistory] = useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const loadDashboard = async () => {

    try {
      setLoading(true);
      setError("");

      const [
        statsData,
        historyData,
      ] = await Promise.all([
        getDashboardStats(),
        getMatchHistory(),
      ]);

      setStats(statsData);
      setHistory(historyData);

    } catch (err) {

      console.error(
        "Dashboard error:",
        err
      );

      setError(
        "Unable to load dashboard."
      );

    } finally {

      setLoading(false);

    }
  };


  useEffect(() => {
    loadDashboard();
  }, []);


  const handleDelete =
    async (id) => {

      try {

        await deleteHistoryItem(id);

        await loadDashboard();

      } catch (err) {

        console.error(
          "Delete error:",
          err
        );

      }
    };


  const handleClearHistory =
    async () => {

      const confirmed =
        window.confirm(
          "Are you sure you want to clear all match history?"
        );

      if (!confirmed) {
        return;
      }

      try {

        await clearMatchHistory();

        await loadDashboard();

      } catch (err) {

        console.error(
          "Clear history error:",
          err
        );

      }
    };


  const formatDate = (value) => {

    const normalized =
      value.includes("T")
        ? value
        : `${value.replace(" ", "T")}Z`;

    return new Date(
      normalized
    ).toLocaleString();
  };


  return (
    <div style={styles.page}>

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
            style={styles.primaryNavButton}
          >
            New Analysis
          </Link>

        </div>

      </nav>


      <main style={styles.container}>

        <div style={styles.header}>

          <div>

            <h1 style={styles.heading}>
              Dashboard
            </h1>

            <p style={styles.subtitle}>
              Track your resume analyses and
              improvement progress.
            </p>

          </div>

          {history.length > 0 && (

            <button
              onClick={handleClearHistory}
              style={styles.clearButton}
            >
              Clear History
            </button>

          )}

        </div>


        {error && (
          <div style={styles.error}>
            {error}
          </div>
        )}


        <div style={styles.statsGrid}>

          <StatCard
            icon="📄"
            title="Total Analyses"
            value={stats.total_analyses}
          />

          <StatCard
            icon="📊"
            title="Average Score"
            value={`${stats.average_score}%`}
          />

          <StatCard
            icon="🏆"
            title="Best Score"
            value={`${stats.best_score}%`}
          />

        </div>


        <section style={styles.historyCard}>

          <div style={styles.historyHeader}>

            <div>

              <h2 style={styles.historyTitle}>
                Match History
              </h2>

              <p style={styles.subtitle}>
                Your most recent resume analyses.
              </p>

            </div>

          </div>


          {loading ? (

            <div style={styles.centerMessage}>
              Loading dashboard...
            </div>

          ) : history.length === 0 ? (

            <div style={styles.emptyState}>

              <div style={styles.emptyIcon}>
                📄
              </div>

              <h3>
                No analyses yet
              </h3>

              <p style={styles.subtitle}>
                Analyze your first resume to
                start building your history.
              </p>

              <Link
                to="/upload"
                style={styles.analyzeButton}
              >
                Analyze Resume
              </Link>

            </div>

          ) : (

            <div>

              {history.map((item) => (

                <div
                  key={item.id}
                  style={styles.historyItem}
                >

                  <div style={styles.historyMain}>

                    <div style={styles.fileIcon}>
                      📄
                    </div>


                    <div style={styles.historyInfo}>

                      <div style={styles.fileName}>
                        {item.filename}
                      </div>

                      <div style={styles.jobLabel}>
                        {item.job_label}
                      </div>

                      <div style={styles.date}>
                        {formatDate(
                          item.created_at
                        )}
                      </div>


                      <div style={styles.skillsRow}>

                        <span style={styles.matchText}>
                          {
                            item.matched_skills
                              .length
                          } matched
                        </span>

                        <span style={styles.missingText}>
                          {
                            item.missing_skills
                              .length
                          } missing
                        </span>

                      </div>

                    </div>

                  </div>


                  <div style={styles.historyActions}>

                    <div style={styles.score}>
                      {
                        Math.round(
                          item.match_score
                        )
                      }%
                    </div>

                    <button
                      onClick={() =>
                        handleDelete(
                          item.id
                        )
                      }
                      style={styles.deleteButton}
                    >
                      Delete
                    </button>

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>

    </div>
  );
}


function StatCard({
  icon,
  title,
  value,
}) {

  return (
    <div style={styles.statCard}>

      <div style={styles.statIcon}>
        {icon}
      </div>

      <div>

        <div style={styles.statTitle}>
          {title}
        </div>

        <div style={styles.statValue}>
          {value}
        </div>

      </div>

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
    gap: "20px",
  },


  navLink: {
    textDecoration: "none",
    color: "#475569",
    fontWeight: "bold",
  },


  primaryNavButton: {
    textDecoration: "none",
    backgroundColor: "#2563eb",
    color: "white",
    padding: "10px 18px",
    borderRadius: "8px",
    fontWeight: "bold",
  },


  container: {
    maxWidth: "1100px",
    margin: "0 auto",
    padding: "50px 20px 80px",
  },


  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
    marginBottom: "35px",
  },


  heading: {
    fontSize: "40px",
    margin: "0 0 8px",
  },


  subtitle: {
    color: "#64748b",
    lineHeight: "1.6",
    margin: 0,
  },


  statsGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px",
    marginBottom: "30px",
  },


  statCard: {
    backgroundColor: "white",
    padding: "25px",
    borderRadius: "15px",
    display: "flex",
    alignItems: "center",
    gap: "18px",
    boxShadow:
      "0 4px 18px rgba(0,0,0,0.05)",
  },


  statIcon: {
    fontSize: "35px",
  },


  statTitle: {
    color: "#64748b",
    fontSize: "14px",
  },


  statValue: {
    fontSize: "30px",
    fontWeight: "bold",
    marginTop: "5px",
  },


  historyCard: {
    backgroundColor: "white",
    borderRadius: "16px",
    padding: "30px",
    boxShadow:
      "0 4px 18px rgba(0,0,0,0.05)",
  },


  historyHeader: {
    marginBottom: "20px",
  },


  historyTitle: {
    margin: "0 0 6px",
  },


  historyItem: {
    padding: "20px 0",
    borderBottom:
      "1px solid #e2e8f0",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
  },


  historyMain: {
    display: "flex",
    alignItems: "flex-start",
    gap: "15px",
    flex: 1,
  },


  fileIcon: {
    fontSize: "30px",
  },


  historyInfo: {
    minWidth: 0,
  },


  fileName: {
    fontWeight: "bold",
    fontSize: "16px",
  },


  jobLabel: {
    color: "#475569",
    marginTop: "5px",
    overflow: "hidden",
    textOverflow: "ellipsis",
  },


  date: {
    color: "#94a3b8",
    fontSize: "12px",
    marginTop: "5px",
  },


  skillsRow: {
    display: "flex",
    gap: "12px",
    marginTop: "9px",
    fontSize: "13px",
  },


  matchText: {
    color: "#15803d",
  },


  missingText: {
    color: "#dc2626",
  },


  historyActions: {
    textAlign: "right",
  },


  score: {
    color: "#2563eb",
    fontSize: "28px",
    fontWeight: "bold",
    marginBottom: "8px",
  },


  deleteButton: {
    border: "none",
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    padding: "7px 12px",
    borderRadius: "7px",
    cursor: "pointer",
  },


  clearButton: {
    border: "1px solid #dc2626",
    backgroundColor: "white",
    color: "#dc2626",
    padding: "10px 15px",
    borderRadius: "8px",
    cursor: "pointer",
  },


  emptyState: {
    textAlign: "center",
    padding: "60px 20px",
  },


  emptyIcon: {
    fontSize: "55px",
  },


  analyzeButton: {
    display: "inline-block",
    marginTop: "20px",
    backgroundColor: "#2563eb",
    color: "white",
    textDecoration: "none",
    padding: "12px 22px",
    borderRadius: "8px",
    fontWeight: "bold",
  },


  centerMessage: {
    textAlign: "center",
    padding: "50px",
    color: "#64748b",
  },


  error: {
    backgroundColor: "#fee2e2",
    color: "#b91c1c",
    padding: "12px",
    borderRadius: "8px",
    marginBottom: "20px",
  },

};


export default Dashboard;