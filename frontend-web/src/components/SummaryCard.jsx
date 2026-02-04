/**
 * SummaryCard Component
 * 
 * Displays dataset summary statistics with metric cards.
 * Shows total equipment count and averages for Flowrate, Pressure, Temperature.
 */

import React from 'react';
import './SummaryCard.css';

const SummaryCard = ({ data = [], datasetInfo = null, loading = false }) => {
  // Calculate statistics
  const stats = React.useMemo(() => {
    if (!data || data.length === 0) {
      return {
        totalCount: 0,
        avgFlowrate: 0,
        avgPressure: 0,
        avgTemperature: 0
      };
    }

    const totals = data.reduce((acc, item) => ({
      flowrate: acc.flowrate + (item.flowrate || 0),
      pressure: acc.pressure + (item.pressure || 0),
      temperature: acc.temperature + (item.temperature || 0)
    }), { flowrate: 0, pressure: 0, temperature: 0 });

    return {
      totalCount: data.length,
      avgFlowrate: totals.flowrate / data.length,
      avgPressure: totals.pressure / data.length,
      avgTemperature: totals.temperature / data.length
    };
  }, [data]);

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="summary-cards">
        <div className="summary-card-loading">
          <span className="spinner"></span>
          <p>Loading summary...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="summary-cards">
      {/* Dataset Info Card */}
      {datasetInfo && (
        <div className="summary-card summary-card-info">
          <div className="summary-card-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect x="6" y="4" width="20" height="24" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
              <line x1="10" y1="10" x2="22" y2="10" stroke="currentColor" strokeWidth="2"/>
              <line x1="10" y1="15" x2="22" y2="15" stroke="currentColor" strokeWidth="2"/>
              <line x1="10" y1="20" x2="18" y2="20" stroke="currentColor" strokeWidth="2"/>
            </svg>
          </div>
          <div className="summary-card-content">
            <h4 className="summary-card-title">Dataset</h4>
            <p className="summary-card-value">{datasetInfo.name || 'Unknown'}</p>
            <p className="summary-card-subtitle">
              Uploaded {formatDate(datasetInfo.uploaded_at)}
            </p>
          </div>
        </div>
      )}

      {/* Total Equipment Card */}
      <div className="summary-card summary-card-count">
        <div className="summary-card-icon">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <path d="M12 6 L12 10 L8 18 C7 20 8 22 10 22 L22 22 C24 22 25 20 24 18 L20 10 L20 6" 
                  stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
            <line x1="12" y1="6" x2="20" y2="6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </div>
        <div className="summary-card-content">
          <h4 className="summary-card-title">Total Equipment</h4>
          <p className="summary-card-value">{stats.totalCount}</p>
          <p className="summary-card-subtitle">Items in dataset</p>
        </div>
      </div>

      {/* Average Flowrate Card */}
      <div className="summary-card summary-card-flowrate">
        <div className="summary-card-icon">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <path d="M8 16 Q12 10 16 16 T24 16" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round"/>
            <path d="M10 20 Q14 14 18 20 T26 20" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round"/>
            <circle cx="16" cy="16" r="1.5" fill="currentColor"/>
            <circle cx="8" cy="16" r="1.5" fill="currentColor"/>
            <circle cx="24" cy="16" r="1.5" fill="currentColor"/>
          </svg>
        </div>
        <div className="summary-card-content">
          <h4 className="summary-card-title">Avg Flowrate</h4>
          <p className="summary-card-value">{stats.avgFlowrate.toFixed(2)}</p>
          <p className="summary-card-subtitle">m³/h</p>
        </div>
      </div>

      {/* Average Pressure Card */}
      <div className="summary-card summary-card-pressure">
        <div className="summary-card-icon">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
            <path d="M16 16 L16 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <path d="M16 16 L22 20" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <circle cx="16" cy="16" r="2" fill="currentColor"/>
          </svg>
        </div>
        <div className="summary-card-content">
          <h4 className="summary-card-title">Avg Pressure</h4>
          <p className="summary-card-value">{stats.avgPressure.toFixed(2)}</p>
          <p className="summary-card-subtitle">bar</p>
        </div>
      </div>

      {/* Average Temperature Card */}
      <div className="summary-card summary-card-temperature">
        <div className="summary-card-icon">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect x="14" y="4" width="4" height="16" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
            <circle cx="16" cy="24" r="4" stroke="currentColor" strokeWidth="2" fill="currentColor"/>
            <line x1="16" y1="20" x2="16" y2="8" stroke="currentColor" strokeWidth="2"/>
          </svg>
        </div>
        <div className="summary-card-content">
          <h4 className="summary-card-title">Avg Temperature</h4>
          <p className="summary-card-value">{stats.avgTemperature.toFixed(2)}</p>
          <p className="summary-card-subtitle">°C</p>
        </div>
      </div>
    </div>
  );
};

export default SummaryCard;
