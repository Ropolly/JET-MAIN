import axios from 'axios';

// API base URL
const API_URL = 'http://localhost:8000';

// Configure axios defaults
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401 errors
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't tried to refresh the token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          // No refresh token available, redirect to login
          window.location.href = '/login';
          return Promise.reject(error);
        }
        
        // Try to get a new token
        const response = await axios.post(`${API_URL}/api/token/refresh/`, {
          refresh: refreshToken
        });
        
        // Save the new token
        localStorage.setItem('token', response.data.access);
        
        // Update the authorization header
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
        
        // Retry the original request
        return axios(originalRequest);
      } catch (refreshError) {
        // Refresh token is invalid, redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// API services
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await axios.post(`${API_URL}/api/token/`, { username, password });
    return response.data;
  },
  
  verifyToken: async (token: string) => {
    const response = await axios.post(`${API_URL}/api/token/verify/`, { token });
    return response.data;
  },
  
  refreshToken: async (refresh: string) => {
    const response = await axios.post(`${API_URL}/api/token/refresh/`, { refresh });
    return response.data;
  },
  
  getUserProfile: async () => {
    const response = await axios.get(`${API_URL}/api/users/me/`);
    return response.data;
  }
};

export const patientAPI = {
  getAll: async (params = {}) => {
    const response = await axios.get(`${API_URL}/api/patients/`, { params });
    return response.data;
  },
  
  getById: async (id: string) => {
    const response = await axios.get(`${API_URL}/api/patients/${id}/`);
    return response.data;
  },
  
  create: async (data: any) => {
    const response = await axios.post(`${API_URL}/api/patients/`, data);
    return response.data;
  },
  
  update: async (id: string, data: any) => {
    const response = await axios.put(`${API_URL}/api/patients/${id}/`, data);
    return response.data;
  },
  
  delete: async (id: string) => {
    const response = await axios.delete(`${API_URL}/api/patients/${id}/`);
    return response.data;
  }
};

export const quoteAPI = {
  getAll: async (params = {}) => {
    const response = await axios.get(`${API_URL}/api/quotes/`, { params });
    return response.data;
  },
  
  getById: async (id: string) => {
    const response = await axios.get(`${API_URL}/api/quotes/${id}/`);
    return response.data;
  },
  
  create: async (data: any) => {
    const response = await axios.post(`${API_URL}/api/quotes/`, data);
    return response.data;
  },
  
  update: async (id: string, data: any) => {
    const response = await axios.put(`${API_URL}/api/quotes/${id}/`, data);
    return response.data;
  },
  
  delete: async (id: string) => {
    const response = await axios.delete(`${API_URL}/api/quotes/${id}/`);
    return response.data;
  }
};

export default {
  auth: authAPI,
  patients: patientAPI,
  quotes: quoteAPI
};
