
import axios from "axios";
import APP_CONFIG from "../config/appConfig";

// --------------------------------------------------
// API CONFIGURATION
// --------------------------------------------------

const API_BASE_URL = APP_CONFIG.API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    "Missing REACT_APP_API_BASE_URL. " +
      "Set it in frontend/.env.development " +
      "or the deployment environment."
  );
}

const api = axios.create({
  baseURL: API_BASE_URL.replace(/\/+$/, ""),
  timeout: 120000,
});

// --------------------------------------------------
// RESUME MATCHING
// --------------------------------------------------

export const analyzeResume = async (
  resumeFile,
  jobDescription
) => {
  const formData = new FormData();

  formData.append("file", resumeFile);
  formData.append("job_description", jobDescription);

  const response = await api.post(
    "/api/match",
    formData
  );

  return response.data;
};

// --------------------------------------------------
// RESUME UPLOAD
// --------------------------------------------------

export const uploadResume = async (resumeFile) => {
  const formData = new FormData();

  formData.append("file", resumeFile);

  const response = await api.post(
    "/api/resume/upload",
    formData
  );

  return response.data;
};

// --------------------------------------------------
// DASHBOARD STATISTICS
// --------------------------------------------------

export const getDashboardStats = async () => {
  const response = await api.get(
    "/api/dashboard/stats"
  );

  return response.data;
};

// --------------------------------------------------
// DASHBOARD ANALYSIS HISTORY
// --------------------------------------------------

export const getDashboardHistory = async () => {
  const response = await api.get(
    "/api/dashboard/history"
  );

  return response.data;
};
// Backward-compatible name used by Dashboard.jsx
export const getMatchHistory = getDashboardHistory;
// --------------------------------------------------
// DELETE A SINGLE HISTORY ITEM
// --------------------------------------------------

export const deleteHistoryItem = async (analysisId) => {
  const response = await api.delete(
    `/api/dashboard/history/${analysisId}`
  );

  return response.data;
};

// --------------------------------------------------
// CLEAR ALL MATCH HISTORY
// --------------------------------------------------

export const clearMatchHistory = async () => {
  const response = await api.delete(
    "/api/dashboard/history"
  );

  return response.data;
};
// --------------------------------------------------
// HEALTH CHECK
// --------------------------------------------------

export const checkBackendHealth = async () => {
  const response = await api.get("/health");

  return response.data;
};

export default api;
