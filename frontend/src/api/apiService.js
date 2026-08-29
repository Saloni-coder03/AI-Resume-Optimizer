import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  "http://127.0.0.1:8001";

export const analyzeResume = async (
  file,
  jobDescription
) => {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("job_description", jobDescription);

  const response = await axios.post(
    `${API_BASE_URL}/api/match`,
    formData
  );

  return response.data;
};