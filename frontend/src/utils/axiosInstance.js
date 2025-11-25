import axios from 'axios';

// Create axios instance with base configuration
const axiosInstance = axios.create({
  baseURL: '/api',
  withCredentials: true,
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// Request interceptor to add auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // ✅ FIX: Check if we have a token before attempting refresh
    const token = localStorage.getItem('access');
    if (!token) {
      return Promise.reject(error); // No token, no refresh attempt
    }

    // If error is 401 and we haven't tried refreshing yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      
      // Don't try to refresh if this was a logout request
      if (originalRequest.url?.includes('/auth/logout')) {
        return Promise.reject(error);
      }

      // ✅ FIX: Don't try to refresh if this was the /me endpoint (initial auth check)
      if (originalRequest.url?.includes('/me')) {
        localStorage.removeItem('access');
        return Promise.reject(error);
      }

      if (isRefreshing) {
        // If already refreshing, add to queue
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => {
          return axiosInstance(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Attempt to refresh token
        const response = await axiosInstance.post('/refresh');
        
        const newToken = response.data.access;
        localStorage.setItem('access', newToken);
        
        // Process queued requests
        processQueue(null, newToken);
        
        // Retry original request
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // Refresh failed - clear everything
        processQueue(refreshError, null);
        localStorage.removeItem('access');
        
        // Clear any cookies by calling logout
        try {
          await axiosInstance.post('/auth/logout');
        } catch (e) {
          // Ignore logout errors
        }
        
        // Only redirect if this was NOT an API call (avoid redirecting during normal API calls)
        if (!originalRequest.url?.includes('/api/')) {
          if (window.location.pathname !== '/') {
            window.location.href = '/';
          } else {
            window.location.reload();
          }
        }
        
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;