/**
 * ParameterComparisonChart Component
 * 
 * Scatter/Line chart showing individual equipment parameters with filtering by equipment type.
 * Optimized for large datasets with smart visualization.
 */

import React, { useState, useMemo } from 'react';
import { Scatter, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const ParameterComparisonChart = ({ data = [] }) => {
  const [selectedType, setSelectedType] = useState('All');
  const [selectedParameter, setSelectedParameter] = useState('flowrate');

  // Get unique equipment types
  const equipmentTypes = useMemo(() => {
    if (!data || data.length === 0) return [];
    const types = [...new Set(data.map(item => item.equipment_type))];
    return ['All', ...types.sort()];
  }, [data]);

  // Filter data by selected type
  const filteredData = useMemo(() => {
    if (selectedType === 'All') return data;
    return data.filter(item => item.equipment_type === selectedType);
  }, [data, selectedType]);

  // Check if it's a large dataset
  const isLargeDataset = filteredData.length > 50;

  // Calculate statistics for large datasets
  const stats = useMemo(() => {
    if (filteredData.length === 0) return { avg: 0, min: 0, max: 0 };
    const values = filteredData.map(item => item[selectedParameter] || 0);
    return {
      avg: values.reduce((a, b) => a + b, 0) / values.length,
      min: Math.min(...values),
      max: Math.max(...values)
    };
  }, [filteredData, selectedParameter]);

  // Prepare chart data
  const chartData = useMemo(() => {
    const values = filteredData.map(item => item[selectedParameter] || 0);
    
    if (isLargeDataset) {
      // For large datasets, limit x-axis labels
      const step = Math.ceil(filteredData.length / 10);
      const labels = filteredData.map((item, index) => {
        if (index % step === 0 || index === filteredData.length - 1) {
          const name = item.equipment_name || `Eq-${index + 1}`;
          return name.length > 12 ? name.substring(0, 12) + '...' : name;
        }
        return '';
      });

      return {
        labels: labels,
        datasets: [{
          label: getParameterLabel(selectedParameter),
          data: values,
          borderColor: 'transparent',
          backgroundColor: getParameterColor(selectedParameter, 0.6),
          borderWidth: 0,
          pointRadius: 3,
          pointHoverRadius: 5,
          pointBackgroundColor: getParameterColor(selectedParameter, 0.7),
          pointBorderColor: '#fff',
          pointBorderWidth: 1,
          tension: 0,
          fill: false,
          showLine: false
        },
        // Add average line
        {
          label: 'Average',
          data: new Array(filteredData.length).fill(stats.avg),
          borderColor: getParameterColor(selectedParameter, 0.8),
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderDash: [5, 5],
          pointRadius: 0,
          fill: false,
          showLine: true
        }]
      };
    } else {
      // Original chart for small datasets
      const labels = filteredData.map((item, index) => item.equipment_name || `Equip-${index + 1}`);
      return {
        labels,
        datasets: [{
          label: getParameterLabel(selectedParameter),
          data: values,
          borderColor: getParameterColor(selectedParameter, 1),
          backgroundColor: getParameterColor(selectedParameter, 0.1),
          borderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: getParameterColor(selectedParameter, 1),
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          tension: 0.3,
          fill: true
        }]
      };
    }
  }, [filteredData, selectedParameter, isLargeDataset, stats.avg]);

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: isLargeDataset,
        position: 'top',
        labels: {
          usePointStyle: true,
          boxWidth: 8
        }
      },
      tooltip: {
        backgroundColor: 'rgba(31, 41, 55, 0.95)',
        titleFont: {
          size: 13,
          family: "'Georgia', serif"
        },
        bodyFont: {
          size: 12,
          family: "'Inter', sans-serif"
        },
        padding: 10,
        cornerRadius: 8,
        callbacks: {
          title: function(context) {
            const index = context[0].dataIndex;
            return filteredData[index]?.equipment_name || `Equipment ${index + 1}`;
          },
          label: function(context) {
            if (context.dataset.label === 'Average') {
              return `Average: ${context.parsed.y.toFixed(2)}`;
            }
            return `${getParameterLabel(selectedParameter)}: ${context.parsed.y.toFixed(2)}`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          font: {
            size: isLargeDataset ? 9 : 10,
            family: "'Inter', sans-serif"
          },
          color: '#6B7280',
          maxRotation: 45,
          minRotation: 45,
          autoSkip: isLargeDataset,
          maxTicksLimit: isLargeDataset ? 10 : undefined
        },
        title: {
          display: isLargeDataset,
          text: `Equipment (Total: ${filteredData.length})`,
          font: { size: 11 },
          color: '#6B7280'
        }
      },
      y: {
        beginAtZero: false,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false
        },
        ticks: {
          font: {
            size: 11,
            family: "'Inter', sans-serif"
          },
          color: '#6B7280',
          callback: function(value) {
            return value.toFixed(0);
          }
        },
        title: {
          display: true,
          text: getParameterLabel(selectedParameter),
          font: { size: 11 },
          color: '#6B7280'
        }
      }
    }
  }), [isLargeDataset, filteredData, selectedParameter]);

  function getParameterLabel(param) {
    const labels = {
      flowrate: 'Flowrate (m³/h)',
      pressure: 'Pressure (bar)',
      temperature: 'Temperature (°C)'
    };
    return labels[param] || param;
  }

  function getParameterColor(param, alpha = 1) {
    const colors = {
      flowrate: `rgba(59, 130, 246, ${alpha})`,  // Blue
      pressure: `rgba(249, 115, 22, ${alpha})`,  // Orange
      temperature: `rgba(239, 68, 68, ${alpha})` // Red
    };
    return colors[param] || `rgba(99, 102, 241, ${alpha})`;
  }

  if (!data || data.length === 0) {
    return (
      <div className="chart-empty">
        <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
          <path d="M10 50 L20 30 L30 35 L40 20 L50 25" stroke="var(--color-gray-300)" strokeWidth="2" fill="none"/>
          <circle cx="10" cy="50" r="3" fill="var(--color-gray-300)"/>
          <circle cx="20" cy="30" r="3" fill="var(--color-gray-300)"/>
          <circle cx="30" cy="35" r="3" fill="var(--color-gray-300)"/>
          <circle cx="40" cy="20" r="3" fill="var(--color-gray-300)"/>
          <circle cx="50" cy="25" r="3" fill="var(--color-gray-300)"/>
        </svg>
        <p>No data available</p>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <div className="chart-header">
        <h3 className="chart-title">Parameter Comparison</h3>
        <div className="chart-controls">
          <select
            value={selectedParameter}
            onChange={(e) => setSelectedParameter(e.target.value)}
            className="form-select"
          >
            <option value="flowrate">Flowrate</option>
            <option value="pressure">Pressure</option>
            <option value="temperature">Temperature</option>
          </select>
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="form-select"
          >
            {equipmentTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="chart-wrapper" style={{ height: '300px' }}>
        <Line data={chartData} options={options} />
      </div>
      <div className="chart-summary">
        <p>
          Showing {filteredData.length} equipment{filteredData.length !== 1 ? 's' : ''}
          {isLargeDataset && ` | Avg: ${stats.avg.toFixed(1)} | Range: ${stats.min.toFixed(1)} - ${stats.max.toFixed(1)}`}
        </p>
      </div>
    </div>
  );
};

export default ParameterComparisonChart;
