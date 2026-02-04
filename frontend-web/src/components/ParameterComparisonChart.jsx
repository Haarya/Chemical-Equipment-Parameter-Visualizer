/**
 * ParameterComparisonChart Component
 * 
 * Line chart showing individual equipment parameters with filtering by equipment type.
 */

import React, { useState, useMemo } from 'react';
import { Line } from 'react-chartjs-2';
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

  // Prepare chart data
  const chartData = useMemo(() => {
    const labels = filteredData.map((item, index) => item.equipment_name || `Equip-${index + 1}`);
    const values = filteredData.map(item => item[selectedParameter] || 0);

    return {
      labels,
      datasets: [{
        label: getParameterLabel(selectedParameter),
        data: values,
        borderColor: 'rgba(99, 102, 241, 1)',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        borderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: 'rgba(99, 102, 241, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        tension: 0.3,
        fill: true
      }]
    };
  }, [filteredData, selectedParameter]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
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
          label: function(context) {
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
            size: 10,
            family: "'Inter', sans-serif"
          },
          color: '#6B7280',
          maxRotation: 45,
          minRotation: 45
        }
      },
      y: {
        beginAtZero: true,
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
        }
      }
    }
  };

  function getParameterLabel(param) {
    const labels = {
      flowrate: 'Flowrate (m³/h)',
      pressure: 'Pressure (bar)',
      temperature: 'Temperature (°C)'
    };
    return labels[param] || param;
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
        <p>Showing {filteredData.length} equipment{filteredData.length !== 1 ? 's' : ''}</p>
      </div>
    </div>
  );
};

export default ParameterComparisonChart;
