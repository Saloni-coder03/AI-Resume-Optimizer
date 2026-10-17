
const APP_CONFIG = {
  APP_NAME: "AI Resume Optimizer",

  // The API URL is supplied by the React environment.
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL,

  // Resume upload rules
  MAX_FILE_SIZE_MB: 5,
  MAX_FILE_SIZE_BYTES: 5 * 1024 * 1024,
  ALLOWED_FILE_EXTENSIONS: [".pdf", ".docx"],

  // Score thresholds
  SCORE_THRESHOLDS: {
    EXCELLENT: 80,
    GOOD: 60,
    MODERATE: 40,
  },

  // Application routes
  ROUTES: {
    HOME: "/",
    UPLOAD: "/upload",
    RESULTS: "/results",
    DASHBOARD: "/dashboard",
  },
};

export default APP_CONFIG;
