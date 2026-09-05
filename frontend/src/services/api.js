import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const getDashboardStats = () => axios.get(`${API_URL}/dashboard`);
export const getTransactions = (params) => axios.get(`${API_URL}/transactions`, { params });
export const getTransaction = (id) => axios.get(`${API_URL}/transactions/${id}`);
export const predictTransaction = (data) => axios.post(`${API_URL}/predict`, data);
export const submitReview = (data) => axios.post(`${API_URL}/review`, data);
export const getModelMetrics = () => axios.get(`${API_URL}/model/metrics`);
export const uploadCSV = (formData) => axios.post(`${API_URL}/upload`, formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});
