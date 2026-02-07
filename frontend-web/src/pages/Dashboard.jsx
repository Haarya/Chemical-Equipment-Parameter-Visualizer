/**
 * Dashboard Page
 * 
 * Main dashboard displaying dataset analytics with charts, tables, and summary cards.
 * Includes sidebar for dataset history navigation.
 */

import React, { useState, useEffect } from 'react';
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [downloadingPDF, setDownloadingPDF] = useState(false);

  useEffect(() => {
    fetchDatasets();
  }, []);

  useEffect(() => {
    if (id) {
      fetchDatasetDetail(id);
    } else if (datasets.length > 0 && !selectedDataset) {
      // Auto-select most recent dataset
      fetchDatasetDetail(datasets[0].id);
    }
  }, [id, datasets, selectedDataset]);

  const fetchDatasets = async () => {
    try {
      const response = await api.get('/api/datasets/');
      // Handle both array and paginated response formats
      const data = response.data;
      if (Array.isArray(data)) {
        setDatasets(data);
      } else if (data && Array.isArray(data.results)) {
        setDatasets(data.results);
      } else {
        setDatasets([]);
      }
      setLoading(false);
    } catch (err) {
      setDatasets([]);
      setLoading(false);
    }
  };

  const fetchDatasetDetail = async (datasetId) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await api.get(`/api/datasets/${datasetId}/`);
      setSelectedDataset(response.data);
      setEquipmentData(response.data.equipment_records || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load dataset');
    } finally {
      setLoading(false);
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

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${selectedDataset.name.replace('.csv', '')}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download PDF report: ' + (err.response?.data?.detail || err.message));
    } finally {
      setDownloadingPDF(false);
    }
  };

  const handleUploadNew = () => {
    navigate('/upload');
  };

  if (loading && !selectedDataset) {
    return (
      <Layout>
        <div className="dashboard-loading">
          <span className="spinner"></span>
          <p>Loading dashboard...</p>
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
          <button onClick={() => fetchDatasets()} className="btn btn-primary">
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
            loading={loading}
          />

          {/* Charts Panel */}
          <ChartPanel 
            data={equipmentData}
            loading={loading}
          />

          {/* Data Table */}
          <div className="dashboard-section">
            <h2 className="section-title">Equipment Data</h2>
            <DataTable 
              data={equipmentData}
              loading={loading}
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
