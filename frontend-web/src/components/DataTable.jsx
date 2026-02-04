/**
 * DataTable Component
 * 
 * Displays equipment data in a sortable, paginated table with search functionality.
 * Features: column sorting, pagination (10 rows/page), search/filter.
 */

import React, { useState, useMemo } from 'react';
import './DataTable.css';

const DataTable = ({ data = [], loading = false }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const rowsPerPage = 10;

  // Filter data based on search term
  const filteredData = useMemo(() => {
    if (!searchTerm) return data;
    
    const term = searchTerm.toLowerCase();
    return data.filter(item => 
      item.equipment_name?.toLowerCase().includes(term) ||
      item.equipment_type?.toLowerCase().includes(term) ||
      item.flowrate?.toString().includes(term) ||
      item.pressure?.toString().includes(term) ||
      item.temperature?.toString().includes(term)
    );
  }, [data, searchTerm]);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData;

    const sorted = [...filteredData].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      // Handle numeric comparison
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
      }

      // Handle string comparison
      const aStr = String(aValue || '').toLowerCase();
      const bStr = String(bValue || '').toLowerCase();
      
      if (aStr < bStr) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aStr > bStr) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });

    return sorted;
  }, [filteredData, sortConfig]);

  // Paginate data
  const totalPages = Math.ceil(sortedData.length / rowsPerPage);
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * rowsPerPage;
    return sortedData.slice(startIndex, startIndex + rowsPerPage);
  }, [sortedData, currentPage]);

  // Handle sort
  const handleSort = (key) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
    setCurrentPage(1); // Reset to first page when sorting
  };

  // Handle search
  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1); // Reset to first page when searching
  };

  // Handle page change
  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  // Render sort icon
  const renderSortIcon = (columnKey) => {
    if (sortConfig.key !== columnKey) {
      return (
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="sort-icon">
          <path d="M6 3 L9 6 L3 6 Z" fill="currentColor" opacity="0.3"/>
          <path d="M6 9 L3 6 L9 6 Z" fill="currentColor" opacity="0.3"/>
        </svg>
      );
    }

    return sortConfig.direction === 'asc' ? (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="sort-icon active">
        <path d="M6 3 L9 6 L3 6 Z" fill="currentColor"/>
      </svg>
    ) : (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="sort-icon active">
        <path d="M6 9 L3 6 L9 6 Z" fill="currentColor"/>
      </svg>
    );
  };

  if (loading) {
    return (
      <div className="data-table-container">
        <div className="data-table-loading">
          <span className="spinner"></span>
          <p>Loading equipment data...</p>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="data-table-container">
        <div className="data-table-empty">
          <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
            <rect x="10" y="10" width="40" height="40" rx="4" stroke="var(--color-gray-300)" strokeWidth="2" fill="none"/>
            <line x1="10" y1="20" x2="50" y2="20" stroke="var(--color-gray-300)" strokeWidth="2"/>
            <line x1="10" y1="30" x2="50" y2="30" stroke="var(--color-gray-300)" strokeWidth="2"/>
            <line x1="10" y1="40" x2="50" y2="40" stroke="var(--color-gray-300)" strokeWidth="2"/>
          </svg>
          <p>No equipment data available</p>
          <p className="data-table-empty-hint">Upload a CSV file to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="data-table-container">
      {/* Search Bar */}
      <div className="data-table-header">
        <div className="data-table-search">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="search-icon">
            <circle cx="7" cy="7" r="5" stroke="currentColor" strokeWidth="1.5" fill="none"/>
            <line x1="11" y1="11" x2="15" y2="15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          <input
            type="text"
            placeholder="Search equipment..."
            value={searchTerm}
            onChange={handleSearch}
            className="form-input"
          />
        </div>
        <div className="data-table-count">
          Showing {paginatedData.length} of {sortedData.length} equipment{sortedData.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Table */}
      <div className="data-table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('equipment_name')} className="sortable">
                Equipment Name {renderSortIcon('equipment_name')}
              </th>
              <th onClick={() => handleSort('equipment_type')} className="sortable">
                Type {renderSortIcon('equipment_type')}
              </th>
              <th onClick={() => handleSort('flowrate')} className="sortable">
                Flowrate (m³/h) {renderSortIcon('flowrate')}
              </th>
              <th onClick={() => handleSort('pressure')} className="sortable">
                Pressure (bar) {renderSortIcon('pressure')}
              </th>
              <th onClick={() => handleSort('temperature')} className="sortable">
                Temperature (°C) {renderSortIcon('temperature')}
              </th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((item, index) => (
              <tr key={item.id || index}>
                <td className="equipment-name">{item.equipment_name}</td>
                <td className="equipment-type">{item.equipment_type}</td>
                <td className="numeric">{item.flowrate?.toFixed(2)}</td>
                <td className="numeric">{item.pressure?.toFixed(2)}</td>
                <td className="numeric">{item.temperature?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="data-table-pagination">
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className="btn btn-secondary btn-sm pagination-btn"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M10 4 L6 8 L10 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Previous
          </button>

          <div className="pagination-info">
            Page {currentPage} of {totalPages}
          </div>

          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="btn btn-secondary btn-sm pagination-btn"
          >
            Next
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M6 4 L10 8 L6 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

export default DataTable;
