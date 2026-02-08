/**
 * HistoryList Component
 * 
 * Displays the last 5 uploaded datasets with details.
 * Clickable items navigate to dataset detail view.
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './HistoryList.css';

const HistoryList = ({ onSelectDataset, selectedDatasetId, showDelete = false }) => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deletingId, setDeletingId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await api.get('/api/datasets/');
      // Handle both array and paginated response formats
      const data = response.data;
      if (Array.isArray(data)) {
        setDatasets(data);
      } else if (data && Array.isArray(data.results)) {
        setDatasets(data.results);
      } else {
        setDatasets([]);
        // Unexpected format - default to empty
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load datasets');
      setDatasets([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, name, e) => {
    e.stopPropagation();
    
    if (!window.confirm(`Delete dataset "${name}"?`)) {
      return;
    }

    setDeletingId(id);
    try {
      await api.delete(`/api/datasets/${id}/delete/`);
      setDatasets(prev => prev.filter(d => d.id !== id));
      
      // If deleted dataset was selected, clear selection
      if (selectedDatasetId === id && onSelectDataset) {
        onSelectDataset(null);
      }
    } catch (err) {
      setError('Failed to delete dataset: ' + (err.response?.data?.detail || err.message));
    } finally {
      setDeletingId(null);
    }
  };

  const handleDatasetClick = (dataset) => {
    if (onSelectDataset) {
      onSelectDataset(dataset);
    } else {
      // Fallback: go to dashboard (dataset selection is state-driven, not URL-driven)
      navigate('/dashboard');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="history-list">
        <div className="history-loading">
          <span className="spinner"></span>
          <p>Loading history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="history-list">
        <div className="message message-error">
          {error}
        </div>
        <button onClick={fetchDatasets} className="btn btn-secondary btn-sm">
          Retry
        </button>
      </div>
    );
  }

  if (datasets.length === 0) {
    return (
      <div className="history-list">
        <div className="history-empty">
          <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
            <rect x="15" y="10" width="30" height="40" rx="3" stroke="var(--color-gray-300)" strokeWidth="2" fill="none"/>
            <line x1="20" y1="18" x2="40" y2="18" stroke="var(--color-gray-300)" strokeWidth="2"/>
            <line x1="20" y1="25" x2="40" y2="25" stroke="var(--color-gray-300)" strokeWidth="2"/>
            <line x1="20" y1="32" x2="35" y2="32" stroke="var(--color-gray-300)" strokeWidth="2"/>
          </svg>
          <p>No datasets uploaded yet</p>
          <button onClick={() => navigate('/upload')} className="btn btn-primary btn-sm">
            Upload Dataset
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="history-list">
      <div className="history-header">
        <h3 className="history-title">Recent Datasets</h3>
        <button onClick={fetchDatasets} className="btn-refresh" title="Refresh">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="23 4 23 10 17 10"/>
            <polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
        </button>
      </div>

      <div className="history-items">
        {datasets.map((dataset) => (
          <div
            key={dataset.id}
            className={`history-item ${selectedDatasetId === dataset.id ? 'history-item-active' : ''}`}
            onClick={() => handleDatasetClick(dataset)}
          >
            <div className="history-item-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="4" y="3" width="16" height="18" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                <line x1="8" y1="8" x2="16" y2="8" stroke="currentColor" strokeWidth="2"/>
                <line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" strokeWidth="2"/>
                <line x1="8" y1="16" x2="13" y2="16" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>

            <div className="history-item-content">
              <h4 className="history-item-name">{dataset.name}</h4>
              <p className="history-item-meta">
                <span className="history-item-date">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <circle cx="6" cy="6" r="5" stroke="currentColor" strokeWidth="1" fill="none"/>
                    <path d="M6 3 L6 6 L8 8" stroke="currentColor" strokeWidth="1" strokeLinecap="round"/>
                  </svg>
                  {formatDate(dataset.uploaded_at)}
                </span>
                <span className="history-item-count">
                  {dataset.total_records} record{dataset.total_records !== 1 ? 's' : ''}
                </span>
              </p>
            </div>

            {showDelete && (
              <button
                className="history-item-delete"
                onClick={(e) => handleDelete(dataset.id, dataset.name, e)}
                title="Delete dataset"
                disabled={deletingId === dataset.id}
              >
                {deletingId === dataset.id ? (
                  <span className="spinner-small"></span>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    <line x1="10" y1="11" x2="10" y2="17"/>
                    <line x1="14" y1="11" x2="14" y2="17"/>
                  </svg>
                )}
              </button>
            )}
          </div>
        ))}
      </div>

      {datasets.length >= 5 && (
        <div className="history-footer">
          <p className="history-note">Showing last 5 datasets</p>
        </div>
      )}
    </div>
  );
};

export default HistoryList;
