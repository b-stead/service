import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // Replace with your FastAPI backend URL
});

// Add a request interceptor to include the Bearer Token
// Add the false Bearer Token to all requests
api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzb21lcmFuZG9tc3RyaW5nIiwiaWF0IjoxNzU3MjcxMTExLCJleHAiOjE3ODg4MDcxMTF9.fZJVbVXv2U5rC9p0XaflBqx7bbpyMw-SQDEpQXAL8Ek`;
  return config;
});

export default api;