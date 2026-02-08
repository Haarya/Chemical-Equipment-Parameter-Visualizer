/**
 * Dashboard Page
 * 
 * Main dashboard displaying dataset analytics with charts, tables, and summary cards.
 * Includes sidebar for dataset history navigation.
 */

import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import SummaryCard from '../components/SummaryCard';
import ChartPanel from '../components/ChartPanel';
import DataTable from '../components/DataTable';
import HistorySidebar from '../components/HistorySidebar';
import api from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [equipmentData, setEquipmentData] = useState([]);
  const [loadingList, setLoadingList] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [error, setError] = useState('');
  const [downloadingPDF, setDownloadingPDF] = useState(false);

  // Refs to prevent double-fetches and track mounted state
  const mountedRef = useRef(true);
  const currentDetailRequest = useRef(null);
  const initialLoadDone = useRef(false);

  // Cleanup on unmount
  useEffect(() => {
    return () => { mountedRef.current = false; };
  }, []);

  // Single effect: on mount, load datasets list (once)
  useEffect(() => {
    if (initialLoadDone.current) return;
    initialLoadDone.current = true;

    const loadDatasets = async () => {
      try {
        setLoadingList(true);
        const response = await api.get('/api/datasets/');
        if (!mountedRef.current) return;

        const data = response.data;
        let dataList = [];
        if (Array.isArray(data)) {
          dataList = data;
        } else if (data && Array.isArray(data.results)) {
          dataList = data.results;
        }
        setDatasets(dataList);

        // If no specific dataset in URL, auto-select first
        if (!id && dataList.length > 0) {
          loadDetail(String(dataList[0].id));
        }
      } catch (err) {
        if (mountedRef.current) setDatasets([]);
      } finally {
        if (mountedRef.current) setLoadingList(false);
      }
    };

    loadDatasets();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load dataset detail when URL id changes
  useEffect(() => {
    if (id) {
      loadDetail(id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const loadDetail = async (datasetId) => {
    // Cancel tracking of any previous request
    const requestId = Date.now();
    currentDetailRequest.current = requestId;

    try {
      setLoadingDetail(true);
      setError('');
      
      const response = await api.get(`/api/datasets/${datasetId}/`);

      // Only update state if this is still the latest request and component is mounted
      if (!mountedRef.current || currentDetailRequest.current !== requestId) return;

      setSelectedDataset(response.data);
      setEquipmentData(response.data.equipment_records || []);
    } catch (err) {
      if (!mountedRef.current || currentDetailRequest.current !== requestId) return;
      setError(err.response?.data?.detail || 'Failed to load dataset');
    } finally {
      if (mountedRef.current && currentDetailRequest.current === requestId) {
        setLoadingDetail(false);
      }
    }
  };

  const handleDatasetSelect = (dataset) => {
    if (dataset) {
      navigate(`/dataset/${dataset.id}`);
    }
  };

  const handleDownloadPDF = async () => {
    if (!selectedDataset) {
      alert('No dataset selected');
      return;
    }

    try {
      setDownloadingPDF(true);
      const response = await api.get(`/api/datasets/${selectedDataset.id}/report/pdf/`, {
        responseType: 'blob'
      });

      // Verify we got a PDF (not an error page)
      const contentType = response.headers['content-type'] || '';
      if (!contentType.includes('application/pdf')) {
        // Server returned a non-PDF response (possibly an error in HTML/JSON)
        const text = await response.data.text();
        try {
          const errorData = JSON.parse(text);
          throw new Error(errorData.detail || errorData.error || 'Server returned an unexpected response');
        } catch (parseErr) {
          if (parseErr.message !== 'Server returned an unexpected response') {
            throw new Error('Failed to generate PDF report');
          }
          throw parseErr;
        }
      }

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${selectedDataset.name.replace('.csv', '')}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      let errorMessage = err.message || 'Unknown error';
      // When responseType is 'blob', error response data is a Blob — parse it
      if (err.response?.data instanceof Blob) {
        try {
          const text = await err.response.data.text();
          const errorData = JSON.parse(text);
          errorMessage = errorData.detail || errorData.error || err.message;
        } catch {
          errorMessage = `Server error (${err.response?.status || 'unknown'})`;
        }
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      }
      alert('Failed to download PDF report: ' + errorMessage);
    } finally {
      setDownloadingPDF(false);
    }
  };

  const handleUploadNew = () => {
    navigate('/upload');
  };

  const isInitialLoading = loadingList && !selectedDataset && datasets.length === 0;

  if (isInitialLoading) {
    return (
      <Layout>
        <div className="dashboard-skeleton">
          <div className="dashboard-skeleton-header">
            <div className="skeleton-line skeleton-line-xl"></div>
            <div className="skeleton-line skeleton-line-lg"></div>
          </div>
          <div className="dashboard-skeleton-actions">
            <div className="skeleton-pill"></div>
            <div className="skeleton-pill"></div>
          </div>
          <div className="dashboard-skeleton-cards">
            {Array.from({ length: 5 }).map((_, index) => (
              <div key={index} className="skeleton-card"></div>
            ))}
          </div>
          <div className="dashboard-skeleton-charts">
            <div className="skeleton-panel"></div>
            <div className="skeleton-panel"></div>
            <div className="skeleton-panel skeleton-panel-wide"></div>
          </div>
          <div className="dashboard-skeleton-table">
            <div className="skeleton-line skeleton-line-md"></div>
            <div className="skeleton-table"></div>
          </div>
        </div>
      </Layout>
    );
  }

  if (error && !selectedDataset) {
    return (
      <Layout>
        <div className="dashboard-error">
          <div className="message message-error">
            {error}
          </div>
          <button onClick={() => window.location.reload()} className="btn btn-primary">
            Retry
          </button>
        </div>
      </Layout>
    );
  }

  if (!selectedDataset && datasets.length === 0) {
    return (
      <Layout>
        <div className="dashboard-empty">
          <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
            <path 
              d="M40 15 L40 35 L25 75 C22 82 25 90 32.5 90 L67.5 90 C75 90 78 82 75 75 L60 35 L60 15" 
              stroke="var(--color-forest)" 
              strokeWidth="3" 
              strokeLinecap="round" 
              strokeLinejoin="round"
              fill="var(--color-sage)"
            />
            <line x1="40" y1="15" x2="60" y2="15" stroke="var(--color-forest)" strokeWidth="3" strokeLinecap="round"/>
            <circle cx="45" cy="70" r="3" fill="var(--color-forest)" opacity="0.5"/>
            <circle cx="50" cy="75" r="2.5" fill="var(--color-forest)" opacity="0.5"/>
            <circle cx="55" cy="68" r="3" fill="var(--color-forest)" opacity="0.5"/>
          </svg>
          <h2>No Data Available</h2>
          <p>Upload your first CSV file to start analyzing chemical equipment data.</p>
          <button onClick={handleUploadNew} className="btn btn-primary btn-lg">
            Upload Dataset
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="dashboard-container">
        <div className="dashboard-main">
          {/* Dashboard Header */}
          <div className="dashboard-header">
            <div className="dashboard-header-content">
              <h1 className="dashboard-title">Dashboard</h1>
              <p className="dashboard-subtitle">
                Analyze and visualize chemical equipment parameters
              </p>
            </div>
            <div className="dashboard-actions">
              <button 
                onClick={handleDownloadPDF}
                disabled={downloadingPDF || !selectedDataset}
                className="btn btn-secondary"
              >
                {downloadingPDF ? (
                  <>
                    <span className="spinner"></span>
                    Generating...
                  </>
                ) : (
                  <>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="7 10 12 15 17 10"/>
                      <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                    Download PDF
                  </>
                )}
              </button>
              <button 
                onClick={handleUploadNew}
                className="btn btn-primary"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                Upload New
              </button>
            </div>
          </div>

          {/* Summary Cards */}
          <SummaryCard 
            data={equipmentData}
            datasetInfo={selectedDataset}
            loading={loadingDetail}
          />

          {/* Charts Panel */}
          <ChartPanel 
            data={equipmentData}
            loading={loadingDetail}
          />

          {/* Data Table */}
          <div className="dashboard-section">
            <h2 className="section-title">Equipment Data</h2>
            <DataTable 
              data={equipmentData}
              loading={loadingDetail}
            />
          </div>
        </div>

        {/* History Sidebar */}
        <HistorySidebar 
          onSelectDataset={handleDatasetSelect}
          selectedDatasetId={selectedDataset?.id}
          showDelete={true}
        />
      </div>
    </Layout>
  );
};

export default Dashboard;
