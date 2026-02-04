/**
 * HistorySidebar Component
 * 
 * Collapsible sidebar displaying recent dataset history.
 * Mobile-friendly with toggle functionality.
 */

import React, { useState } from 'react';
import HistoryList from './HistoryList';
import './HistorySidebar.css';

const HistorySidebar = ({ onSelectDataset, selectedDatasetId, showDelete = false }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Mobile Toggle Button */}
      <button 
        className="sidebar-toggle"
        onClick={toggleSidebar}
        aria-label="Toggle history sidebar"
      >
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
          <line x1="7" y1="7" x2="13" y2="7" stroke="currentColor" strokeWidth="2"/>
          <line x1="7" y1="10" x2="13" y2="10" stroke="currentColor" strokeWidth="2"/>
          <line x1="7" y1="13" x2="11" y2="13" stroke="currentColor" strokeWidth="2"/>
        </svg>
        <span>History</span>
      </button>

      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="sidebar-overlay"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar Container */}
      <aside className={`history-sidebar ${isOpen ? 'history-sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <h3 className="sidebar-title">Dataset History</h3>
          <button 
            className="sidebar-close"
            onClick={toggleSidebar}
            aria-label="Close sidebar"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <line x1="5" y1="5" x2="15" y2="15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              <line x1="15" y1="5" x2="5" y2="15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </button>
        </div>

        <div className="sidebar-content">
          <HistoryList 
            onSelectDataset={(dataset) => {
              onSelectDataset(dataset);
              // Close sidebar on mobile after selection
              if (window.innerWidth <= 768) {
                setIsOpen(false);
              }
            }}
            selectedDatasetId={selectedDatasetId}
            showDelete={showDelete}
          />
        </div>
      </aside>
    </>
  );
};

export default HistorySidebar;
