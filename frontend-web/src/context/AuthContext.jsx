/**
 * Authentication Context for Chemical Equipment Parameter Visualizer
 * 
 * Manages global authentication state across the application.
 * Provides login, logout, and authentication check methods.
 * Persists authentication state across page refreshes.
 * 
 * Usage:
 * import { useAuth } from './context/AuthContext';
 * const { user, login, logout, isAuthenticated } = useAuth();
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  loginUser,
  registerUser,
  logoutUser,
  saveAuthToken,
  saveUserInfo,
  removeAuthToken,
  removeUserInfo,
  getAuthToken,
  getUserInfoFromStorage,
} from '../services/api';

// Create Auth Context
const AuthContext = createContext(null);

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const initializeAuth = () => {
      try {
        const token = getAuthToken();
        const storedUser = getUserInfoFromStorage();

        if (token && storedUser) {
          setUser(storedUser);
        }
      } catch (err) {
        // Clear invalid data
        removeAuthToken();
        removeUserInfo();
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  /**
   * Login user
   * @param {string} username 
   * @param {string} password 
   * @returns {Promise<Object>} User object
   */
  const login = async (username, password) => {
    try {
      setError(null);
      setLoading(true);

      // Call login API
      const response = await loginUser({ username, password });

      // Save token and user info
      saveAuthToken(response.token);
      saveUserInfo(response.user);
      setUser(response.user);

      return response.user;
    } catch (err) {
      const errorMessage = err.response?.data?.error || 
                          err.response?.data?.detail || 
                          'Login failed. Please check your credentials.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Register new user
   * @param {string} username 
   * @param {string} email 
   * @param {string} password 
   * @returns {Promise<Object>} User object
   */
  const register = async (username, email, password) => {
    try {
      setError(null);
      setLoading(true);

      // Call register API
      const response = await registerUser({ username, email, password });

      // Save token and user info (auto-login after registration)
      saveAuthToken(response.token);
      saveUserInfo(response.user);
      setUser(response.user);

      return response.user;
    } catch (err) {
      const errorMessage = err.response?.data?.error || 
                          err.response?.data?.detail ||
                          err.response?.data?.details ||
                          'Registration failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout user
   */
  const logout = async () => {
    try {
      setLoading(true);
      
      // Call logout API to invalidate token on server
      await logoutUser();
    } catch (err) {
      // Continue with logout even if API call fails
    } finally {
      // Clear local state and storage
      removeAuthToken();
      removeUserInfo();
      setUser(null);
      setError(null);
      setLoading(false);
    }
  };

  /**
   * Check if user is authenticated
   * @returns {boolean}
   */
  const isAuthenticated = () => {
    return !!user && !!getAuthToken();
  };

  /**
   * Clear error message
   */
  const clearError = () => {
    setError(null);
  };

  // Context value
  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
