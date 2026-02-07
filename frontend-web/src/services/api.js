/**
 * API Service for Chemical Equipment Parameter Visualizer
 * 
 * Centralized API configuration and methods for backend communication.
 * All API calls to Django backend go through this service.
 * 
 * SECURITY:
 * - Token-based authentication
 * - Automatic token attachment to requests
 * - Error handling and response parsing
 */

import axios from 'axios';

// Base URL for Django backend API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized - Token expired or invalid
    // Skip redirect for auth endpoints (login/register) to avoid loops
    const requestUrl = error.config?.url || '';
    const isAuthEndpoint = requestUrl.includes('/api/auth/');
    
    if (error.response && error.response.status === 401 && !isAuthEndpoint) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============================================
// AUTHENTICATION API CALLS
// ============================================

/**
 * Register a new user
 * @param {Object} userData - { username, email, password }
 * @returns {Promise} - { token, user }
 */
export const registerUser = async (userData) => {
  const response = await api.post('/api/auth/register/', userData);
  return response.data;
};

/**
 * Login user
 * @param {Object} credentials - { username, password }
 * @returns {Promise} - { token, user }
 */
export const loginUser = async (credentials) => {
  const response = await api.post('/api/auth/login/', credentials);
  return response.data;
};

/**
 * Logout user
 * @returns {Promise}
 */
export const logoutUser = async () => {
  const response = await api.post('/api/auth/logout/');
  return response.data;
};

/**
 * Get current user info
 * @returns {Promise} - { id, username, email }
 */
export const getUserInfo = async () => {
  const response = await api.get('/api/auth/user/');
  return response.data;
};

// ============================================
// DATASET API CALLS
// ============================================

/**
 * Upload CSV file
 * @param {File} file - CSV file object
 * @returns {Promise} - Dataset summary
 */
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

/**
 * Get list of all datasets (last 5)
 * @returns {Promise} - Array of datasets
 */
export const getDatasets = async () => {
  const response = await api.get('/api/datasets/');
  return response.data;
};

/**
 * Get full dataset details with equipment records
 * @param {number} datasetId - Dataset ID
 * @returns {Promise} - Full dataset object
 */
export const getDatasetDetail = async (datasetId) => {
  const response = await api.get(`/api/datasets/${datasetId}/`);
  return response.data;
};

/**
 * Get dataset summary statistics
 * @param {number} datasetId - Dataset ID
 * @returns {Promise} - Summary statistics
 */
export const getDatasetSummary = async (datasetId) => {
  const response = await api.get(`/api/datasets/${datasetId}/summary/`);
  return response.data;
};

/**
 * Download PDF report for a dataset
 * @param {number} datasetId - Dataset ID
 * @returns {Promise} - Blob object (PDF file)
 */
export const downloadPDFReport = async (datasetId) => {
  const response = await api.get(`/api/datasets/${datasetId}/report/pdf/`, {
    responseType: 'blob',
  });
  return response.data;
};

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Save authentication token to localStorage
 * @param {string} token - JWT token
 */
export const saveAuthToken = (token) => {
  localStorage.setItem('authToken', token);
};

/**
 * Get authentication token from localStorage
 * @returns {string|null} - Token or null
 */
export const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

/**
 * Remove authentication token from localStorage
 */
export const removeAuthToken = () => {
  localStorage.removeItem('authToken');
};

/**
 * Save user info to localStorage
 * @param {Object} user - User object
 */
export const saveUserInfo = (user) => {
  localStorage.setItem('user', JSON.stringify(user));
};

/**
 * Get user info from localStorage
 * @returns {Object|null} - User object or null
 */
export const getUserInfoFromStorage = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

/**
 * Remove user info from localStorage
 */
export const removeUserInfo = () => {
  localStorage.removeItem('user');
};

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  return !!getAuthToken();
};

// Export the configured axios instance for custom requests
export default api;
