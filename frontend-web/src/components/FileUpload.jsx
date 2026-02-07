/**
 * FileUpload Component - Chemistry Lab Edition
 * 
 * Professional CSV upload with chemistry-themed design
 * Inline SVG illustrations of lab equipment
 */

import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadCSV } from '../services/api';
import './FileUpload.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [uploadProgress, setUploadProgress] = useState(0);
  
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const MAX_FILE_SIZE = 50 * 1024 * 1024;

  const validateFile = (file) => {
    if (!file) {
      setMessage({ type: 'error', text: 'Please select a file' });
      return false;
    }

    const fileName = file.name.toLowerCase();
    if (!fileName.endsWith('.csv')) {
      setMessage({ 
        type: 'error', 
        text: 'Invalid file type. Please select a CSV file (.csv)' 
      });
      return false;
    }

    if (file.size > MAX_FILE_SIZE) {
      setMessage({ 
        type: 'error', 
        text: `File too large. Maximum size is ${MAX_FILE_SIZE / (1024 * 1024)}MB` 
      });
      return false;
    }

    if (file.size === 0) {
      setMessage({ type: 'error', text: 'File is empty' });
      return false;
    }

    return true;
  };

  const handleFileSelect = (file) => {
    setMessage({ type: '', text: '' });
    
    if (validateFile(file)) {
      setSelectedFile(file);
      setMessage({ 
        type: 'info', 
        text: `Selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)` 
      });
    } else {
      setSelectedFile(null);
    }
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleDropZoneClick = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage({ type: 'error', text: 'Please select a file first' });
      return;
    }

    setIsUploading(true);
    setMessage({ type: '', text: '' });
    setUploadProgress(0);

    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 200);

    try {
      const response = await uploadCSV(selectedFile);
      
      clearInterval(progressInterval);
      setUploadProgress(100);

      setMessage({ 
        type: 'success', 
        text: `Success! Uploaded ${response.dataset.total_records} records. Redirecting...` 
      });

      if (onUploadSuccess) {
        onUploadSuccess(response);
      }

      setTimeout(() => {
        navigate(`/dataset/${response.dataset.id}`);
      }, 2000);

    } catch (error) {
      clearInterval(progressInterval);
      setUploadProgress(0);
      
      let errorMessage = 'Upload failed. Please try again.';

      if (error.response?.status === 401) {
        errorMessage = 'Please log in to upload a dataset.';
      }
      
      if (error.response?.data) {
        const errorData = error.response.data;
        if (errorData.error) {
          errorMessage = errorData.error;
        } else if (errorData.details) {
          errorMessage = errorData.details;
        }
      } else if (error.message) {
        errorMessage = error.message;
      }

      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setIsUploading(false);
    }
  };

  const handleRemoveFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    setMessage({ type: '', text: '' });
    setUploadProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="file-upload-wrapper">
      <div className="file-upload-card card">
        <div className="card-header">
          <h2 className="card-title">Upload Equipment Data</h2>
          <p className="card-subtitle">Upload your CSV file containing chemical equipment parameters</p>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
          aria-label="File upload input"
        />

        <div
          className={`drop-zone ${isDragging ? 'is-dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleDropZoneClick}
        >
          <div className="upload-illustration">
            <svg 
              className="flask-icon" 
              width="120" 
              height="120" 
              viewBox="0 0 120 120" 
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path 
                d="M45 15 L45 40 L30 75 C28 80 30 85 35 85 L85 85 C90 85 92 80 90 75 L75 40 L75 15" 
                stroke="var(--color-forest)" 
                strokeWidth="3" 
                strokeLinecap="round" 
                strokeLinejoin="round"
                fill="var(--color-sage)"
                className="flask-body"
              />
              <line 
                x1="45" y1="15" x2="75" y2="15" 
                stroke="var(--color-forest)" 
                strokeWidth="3" 
                strokeLinecap="round"
              />
              <path 
                d="M35 70 Q60 65 85 70 L85 85 L35 85 Z" 
                fill="var(--color-forest)" 
                opacity="0.3"
                className="flask-liquid"
              />
              <circle cx="45" cy="70" r="3" fill="var(--color-forest)" opacity="0.4" className="bubble bubble-1"/>
              <circle cx="60" cy="75" r="2" fill="var(--color-forest)" opacity="0.4" className="bubble bubble-2"/>
              <circle cx="70" cy="68" r="2.5" fill="var(--color-forest)" opacity="0.4" className="bubble bubble-3"/>
              <g className="upload-arrow">
                <path 
                  d="M60 50 L60 30 M50 40 L60 30 L70 40" 
                  stroke="var(--color-forest)" 
                  strokeWidth="3" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                  opacity="0.6"
                />
              </g>
            </svg>
          </div>

          <div className="drop-zone-text">
            {selectedFile ? (
              <>
                <h3 className="drop-zone-title">File Ready</h3>
                <p className="drop-zone-subtitle">Click to select a different file</p>
              </>
            ) : isDragging ? (
              <>
                <h3 className="drop-zone-title">Drop it here!</h3>
                <p className="drop-zone-subtitle">Release to upload your CSV</p>
              </>
            ) : (
              <>
                <h3 className="drop-zone-title">Drag & Drop CSV File</h3>
                <p className="drop-zone-subtitle">or click to browse your files</p>
              </>
            )}
          </div>
        </div>

        {selectedFile && (
          <div className="file-preview-card">
            <div className="file-icon-wrapper">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <path 
                  d="M10 5 L25 5 L30 10 L30 35 L10 35 Z" 
                  stroke="var(--color-forest)" 
                  strokeWidth="2"
                  fill="var(--color-sage)"
                />
                <path d="M25 5 L25 10 L30 10" stroke="var(--color-forest)" strokeWidth="2" fill="none"/>
                <text x="20" y="25" fontSize="8" fill="var(--color-forest)" textAnchor="middle" fontWeight="bold">CSV</text>
              </svg>
            </div>
            <div className="file-info">
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">{(selectedFile.size / 1024).toFixed(2)} KB</p>
            </div>
            <button
              type="button"
              className="btn-remove-file"
              onClick={handleRemoveFile}
              aria-label="Remove file"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M4 4 L16 16 M16 4 L4 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
        )}

        {isUploading && (
          <div className="upload-progress-section">
            <div className="progress-container">
              <div className="progress-label">
                <span>Analyzing Data</span>
                <span className="progress-percentage">{uploadProgress}%</span>
              </div>
              <div className="progress-bar-wrapper">
                <div 
                  className="progress-bar-fill" 
                  style={{ width: `${uploadProgress}%` }}
                >
                  <div className="progress-liquid"></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {message.text && (
          <div className={`message message-${message.type}`}>
            {message.text}
          </div>
        )}

        <button
          className="btn btn-primary btn-lg upload-action-btn"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
        >
          {isUploading ? (
            <>
              <span className="spinner"></span>
              Processing...
            </>
          ) : (
            'Upload & Analyze Data'
          )}
        </button>

        <div className="requirements-section">
          <h4 className="requirements-title">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style={{ verticalAlign: 'middle', marginRight: '8px' }}>
              <circle cx="10" cy="10" r="8" stroke="var(--color-forest)" strokeWidth="2" fill="none"/>
              <path d="M10 6 L10 10 L13 13" stroke="var(--color-forest)" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            File Requirements
          </h4>
          <ul className="requirements-list">
            <li><strong>Format:</strong> CSV files only</li>
            <li><strong>Size Limit:</strong> Maximum 10 MB</li>
            <li><strong>Row Limit:</strong> Up to 10,000 records</li>
            <li><strong>Required Columns:</strong> Equipment Name, Type, Flowrate, Pressure, Temperature</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
