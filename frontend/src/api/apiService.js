import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  "http://127.0.0.1:8000";

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
export const getDashboardStats =
  async () => {

    const response = await axios.get(
      `${API_BASE_URL}/api/dashboard/stats`
    );

    return response.data;
  };


export const getMatchHistory =
  async (limit = 20) => {

    const response = await axios.get(
      `${API_BASE_URL}/api/dashboard/history`,
      {
        params: {
          limit: limit,
        },
      }
    );

    return response.data;
  };


export const deleteHistoryItem =
  async (id) => {

    const response = await axios.delete(
      `${API_BASE_URL}/api/dashboard/history/${id}`
    );

    return response.data;
  };


export const clearMatchHistory =
  async () => {

    const response = await axios.delete(
      `${API_BASE_URL}/api/dashboard/history`
    );

    return response.data;
  };