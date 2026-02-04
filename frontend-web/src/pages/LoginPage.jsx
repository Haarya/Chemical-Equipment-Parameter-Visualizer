/**
 * Login Page Component - ChemViz Edition
 * 
 * Provides user authentication interface with chemistry-themed design.
 */

import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './AuthPages.css';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!username.trim()) {
      setError('Username is required');
      return;
    }

    if (!password) {
      setError('Password is required');
      return;
    }

    try {
      setIsLoading(true);
      await login(username, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
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
          <h2 className="auth-heading">Login</h2>
        </div>

        {error && (
          <div className="message message-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username" className="form-label">
              Username
            </label>
            <input
              type="text"
              id="username"
              className="form-input"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="form-input"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
                Logging in...
              </>
            ) : (
              'Login'
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p className="auth-link-text">
            Don't have an account?{' '}
            <Link to="/register" className="auth-link">
              Register here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
