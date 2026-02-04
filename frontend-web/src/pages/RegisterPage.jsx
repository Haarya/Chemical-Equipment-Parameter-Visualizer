/**
 * Register Page Component - ChemViz Edition
 * 
 * Provides user registration interface with chemistry-themed design.
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './AuthPages.css';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const validateForm = () => {
    if (!formData.username.trim()) {
      setError('Username is required');
      return false;
    }

    if (formData.username.length < 3) {
      setError('Username must be at least 3 characters');
      return false;
    }

    if (formData.username.length > 150) {
      setError('Username must be less than 150 characters');
      return false;
    }

    if (!formData.email.trim()) {
      setError('Email is required');
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }

    if (!formData.password) {
      setError('Password is required');
      return false;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return false;
    }
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validate form
    if (!validateForm()) {
      return;
    }

    try {
      setIsLoading(true);

      // Call register method from AuthContext
      await register(formData.username, formData.email, formData.password);

      // Auto-login successful - redirect to dashboard
      navigate('/dashboard', { replace: true });
    } catch (err) {
      // Handle specific error messages from backend
      let errorMessage = err.message;
      
      // Parse backend error details if available
      if (typeof errorMessage === 'object') {
        errorMessage = JSON.stringify(errorMessage);
      }
      
      setError(errorMessage || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card card">
        <div className="auth-header">
          {/* Chemistry Flask Icon */}
          <svg 
            className="auth-icon" 
            width="80" 
            height="80" 
            viewBox="0 0 80 80" 
            fill="none"
          >
            <path 
              d="M30 10 L30 25 L20 50 C18 55 20 60 25 60 L55 60 C60 60 62 55 60 50 L50 25 L50 10" 
              stroke="var(--color-forest)" 
              strokeWidth="3" 
              strokeLinecap="round" 
              strokeLinejoin="round"
              fill="var(--color-sage)"
            />
            <line 
              x1="30" y1="10" x2="50" y2="10" 
              stroke="var(--color-forest)" 
              strokeWidth="3" 
              strokeLinecap="round"
            />
            <path 
              d="M25 45 Q40 42 55 45 L55 60 L25 60 Z" 
              fill="var(--color-forest)" 
              opacity="0.3"
            />
            <circle cx="32" cy="48" r="2" fill="var(--color-forest)" opacity="0.5"/>
            <circle cx="40" cy="50" r="1.5" fill="var(--color-forest)" opacity="0.5"/>
            <circle cx="48" cy="47" r="2" fill="var(--color-forest)" opacity="0.5"/>
          </svg>

          <h1 className="auth-title">Reactometrix</h1>
          <p className="auth-subtitle">Chemical Equipment Visualizer</p>
          <h2 className="auth-heading">Create Account</h2>
        </div>

        {error && (
          <div className="message message-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username" className="form-label">
              Username *
            </label>
            <input
              type="text"
              id="username"
              name="username"
              className="form-input"
              placeholder="Choose a username (min 3 characters)"
              value={formData.username}
              onChange={handleChange}
              disabled={isLoading}
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email *
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-input"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password *
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-input"
              placeholder="Choose a password (min 6 characters)"
              value={formData.password}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword" className="form-label">
              Confirm Password *
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              className="form-input"
              placeholder="Re-enter your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-lg"
            disabled={isLoading}
            style={{ width: '100%' }}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Creating account...
              </>
            ) : (
              'Register'
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p className="auth-link-text">
            Already have an account?{' '}
            <Link to="/login" className="auth-link">
              Login here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
