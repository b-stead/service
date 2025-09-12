import axios from "axios";

console.log("Bearer Token:", process.env.REACT_APP_BEARER_TOKEN);

const api = axios.create({
  baseURL: "/api/", // Replace with your FastAPI backend URL
});

// Add a request interceptor to include the Bearer Token
// Add the false Bearer Token to all requests
api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${process.env.REACT_APP_BEARER_TOKEN}`;
  console.log("Request Config:", config);
  return config;
});

export default api;