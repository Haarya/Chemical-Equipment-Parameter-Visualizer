/**
 * ChartPanel Component
 * 
 * Container component that renders all charts in a responsive grid layout.
 */

import React from 'react';
import TypeDistributionChart from './TypeDistributionChart';
import ParameterBarChart from './ParameterBarChart';
import ParameterComparisonChart from './ParameterComparisonChart';
import './ChartPanel.css';

const ChartPanel = ({ data = [], loading = false }) => {
  if (loading) {
    return (
      <div className="chart-panel">
        <div className="chart-grid">
          <div className="chart-item chart-item-skeleton"></div>
          <div className="chart-item chart-item-skeleton"></div>
          <div className="chart-item chart-item-skeleton chart-item-wide"></div>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="chart-panel">
        <div className="chart-panel-empty">
          <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
            {/* Chemistry Flask with Charts */}
            <path 
              d="M30 10 L30 25 L20 50 C18 55 20 60 25 60 L55 60 C60 60 62 55 60 50 L50 25 L50 10" 
              stroke="var(--color-gray-300)" 
              strokeWidth="2" 
              fill="none"
            />
            <line x1="30" y1="10" x2="50" y2="10" stroke="var(--color-gray-300)" strokeWidth="2"/>
            
            {/* Bar chart inside flask */}
            <rect x="28" y="40" width="4" height="12" fill="var(--color-gray-300)"/>
            <rect x="35" y="35" width="4" height="17" fill="var(--color-gray-300)"/>
            <rect x="42" y="38" width="4" height="14" fill="var(--color-gray-300)"/>
            <rect x="49" y="33" width="4" height="19" fill="var(--color-gray-300)"/>
          </svg>
          <p>No chart data available</p>
          <p className="chart-panel-empty-hint">Upload a CSV file to visualize your data</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-panel">
      <div className="chart-grid">
        <div className="chart-item">
          <TypeDistributionChart data={data} />
        </div>
        <div className="chart-item">
          <ParameterBarChart data={data} />
        </div>
        <div className="chart-item chart-item-wide">
          <ParameterComparisonChart data={data} />
        </div>
      </div>
    </div>
  );
};

export default ChartPanel;
