import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import axios from 'axios';
import { authAPI } from '../services/api';

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

interface User {
  id: string; // UUID from backend
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  roles: string[];
  departments: string[];
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check if user is already logged in on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      const token = localStorage.getItem('token');
      const refreshToken = localStorage.getItem('refreshToken');
      
      if (token && refreshToken) {
        try {
          // Verify token is still valid
          await authAPI.verifyToken(token);
          
          // Set default auth header for all requests
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          // Fetch user profile
          const userData = await authAPI.getUserProfile();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (error) {
          // Try to refresh the token
          try {
            const refreshData = await authAPI.refreshToken(refreshToken);
            
            // Save new token
            localStorage.setItem('token', refreshData.access);
            axios.defaults.headers.common['Authorization'] = `Bearer ${refreshData.access}`;
            
            // Fetch user profile with new token
            const userData = await authAPI.getUserProfile();
            setUser(userData);
            setIsAuthenticated(true);
          } catch (refreshError) {
            // Refresh token is also invalid, logout
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            delete axios.defaults.headers.common['Authorization'];
          }
        }
      }
      
      setLoading(false);
    };

    checkAuthStatus();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      if (!username || !password) {
        throw new Error('Username and password are required');
      }

      // Get JWT token from backend
      const authData = await authAPI.login(username, password);
      const { access, refresh } = authData;
      
      // Save tokens to localStorage
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      // Set default auth header for all requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      // Fetch user profile
      const userData = await authAPI.getUserProfile();
      setUser(userData);
      setIsAuthenticated(true);
    } catch (error: any) {
      console.error('Login error:', error);
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        throw new Error(error.response.data.detail || 'Invalid credentials');
      } else if (error.request) {
        // The request was made but no response was received
        throw new Error('No response from server. Please try again later.');
      } else {
        // Something happened in setting up the request that triggered an Error
        throw new Error(error.message || 'An error occurred during login');
      }
    }
  };

  const logout = () => {
    // Remove tokens from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    
    // Remove auth header
    delete axios.defaults.headers.common['Authorization'];
    
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
