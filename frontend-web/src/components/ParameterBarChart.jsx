/**
 * ParameterBarChart Component
 * 
 * Bar chart comparing average Flowrate, Pressure, and Temperature.
 */

import React, { useMemo } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ParameterBarChart = ({ data = [] }) => {
  // Calculate averages
  const averages = useMemo(() => {
    if (!data || data.length === 0) {
      return { flowrate: 0, pressure: 0, temperature: 0 };
    }

    const totals = data.reduce((acc, item) => ({
      flowrate: acc.flowrate + (item.flowrate || 0),
      pressure: acc.pressure + (item.pressure || 0),
      temperature: acc.temperature + (item.temperature || 0)
    }), { flowrate: 0, pressure: 0, temperature: 0 });

    return {
      flowrate: totals.flowrate / data.length,
      pressure: totals.pressure / data.length,
      temperature: totals.temperature / data.length
    };
  }, [data]);

  const chartData = {
    labels: ['Flowrate (m³/h)', 'Pressure (bar)', 'Temperature (°C)'],
    datasets: [{
      label: 'Average Values',
      data: [averages.flowrate, averages.pressure, averages.temperature],
      backgroundColor: [
        'rgba(47, 92, 70, 0.7)',   // Forest green
        'rgba(60, 179, 113, 0.7)',  // Medium sea green
        'rgba(76, 175, 80, 0.7)',   // Light green
      ],
      borderColor: [
        'rgba(47, 92, 70, 1)',
        'rgba(60, 179, 113, 1)',
        'rgba(76, 175, 80, 1)',
      ],
      borderWidth: 2,
      borderRadius: 6,
      borderSkipped: false,
    }]
  };

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
          size: 14,
          family: "'Georgia', serif"
        },
        bodyFont: {
          size: 13,
          family: "'Inter', sans-serif"
        },
        padding: 12,
        cornerRadius: 8,
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed.y.toFixed(2);
            return `${label}: ${value}`;
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
            size: 12,
            family: "'Inter', sans-serif"
          },
          color: '#4B5563'
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

  if (!data || data.length === 0) {
    return (
      <div className="chart-empty">
        <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
          <rect x="10" y="40" width="10" height="10" fill="var(--color-gray-300)"/>
          <rect x="25" y="30" width="10" height="20" fill="var(--color-gray-300)"/>
          <rect x="40" y="20" width="10" height="30" fill="var(--color-gray-300)"/>
        </svg>
        <p>No data available</p>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <h3 className="chart-title">Average Parameters</h3>
      <div className="chart-wrapper" style={{ height: '300px' }}>
        <Bar data={chartData} options={options} />
      </div>
      <div className="chart-summary">
        <div className="summary-item">
          <span className="summary-label">Avg Flowrate:</span>
          <strong>{averages.flowrate.toFixed(2)} m³/h</strong>
        </div>
        <div className="summary-item">
          <span className="summary-label">Avg Pressure:</span>
          <strong>{averages.pressure.toFixed(2)} bar</strong>
        </div>
        <div className="summary-item">
          <span className="summary-label">Avg Temperature:</span>
          <strong>{averages.temperature.toFixed(2)} °C</strong>
        </div>
      </div>
    </div>
  );
};

export default ParameterBarChart;
