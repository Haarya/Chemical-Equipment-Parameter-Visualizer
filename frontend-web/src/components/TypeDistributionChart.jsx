/**
 * TypeDistributionChart Component
 * 
 * Doughnut chart displaying equipment type distribution with counts and percentages.
 */

import React, { useMemo } from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

const TypeDistributionChart = ({ data = [] }) => {
  // Calculate type distribution
  const typeDistribution = useMemo(() => {
    if (!data || data.length === 0) return {};

    const distribution = {};
    data.forEach(item => {
      const type = item.equipment_type || 'Unknown';
      distribution[type] = (distribution[type] || 0) + 1;
    });

    return distribution;
  }, [data]);

  const chartData = useMemo(() => {
    const types = Object.keys(typeDistribution);
    const counts = Object.values(typeDistribution);
    
    // Chemistry-themed color palette
    const colors = [
      'rgba(47, 92, 70, 0.8)',    // Forest green
      'rgba(34, 139, 34, 0.8)',   // Forest green (light)
      'rgba(60, 179, 113, 0.8)',  // Medium sea green
      'rgba(46, 125, 50, 0.8)',   // Green
      'rgba(27, 94, 32, 0.8)',    // Dark green
      'rgba(76, 175, 80, 0.8)',   // Light green
      'rgba(104, 159, 56, 0.8)',  // Lime green
      'rgba(51, 105, 30, 0.8)',   // Dark forest
    ];

    const borderColors = [
      'rgba(47, 92, 70, 1)',
      'rgba(34, 139, 34, 1)',
      'rgba(60, 179, 113, 1)',
      'rgba(46, 125, 50, 1)',
      'rgba(27, 94, 32, 1)',
      'rgba(76, 175, 80, 1)',
      'rgba(104, 159, 56, 1)',
      'rgba(51, 105, 30, 1)',
    ];

    return {
      labels: types,
      datasets: [{
        label: 'Equipment Count',
        data: counts,
        backgroundColor: colors.slice(0, types.length),
        borderColor: borderColors.slice(0, types.length),
        borderWidth: 2,
        hoverOffset: 8
      }]
    };
  }, [typeDistribution]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 15,
          font: {
            size: 13,
            family: "'Inter', sans-serif"
          },
          color: '#1F2937',
          usePointStyle: true,
          pointStyle: 'circle'
        }
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
        displayColors: true,
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value} (${percentage}%)`;
          }
        }
      }
    }
  };

  if (!data || data.length === 0) {
    return (
      <div className="chart-empty">
        <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
          <circle cx="30" cy="30" r="20" stroke="var(--color-gray-300)" strokeWidth="2" fill="none"/>
          <path d="M30 30 L30 10" stroke="var(--color-gray-300)" strokeWidth="2"/>
          <path d="M30 30 L45 40" stroke="var(--color-gray-300)" strokeWidth="2"/>
        </svg>
        <p>No data available</p>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <h3 className="chart-title">Equipment Type Distribution</h3>
      <div className="chart-wrapper" style={{ height: '300px' }}>
        <Doughnut data={chartData} options={options} />
      </div>
      <div className="chart-summary">
        <p>Total Types: <strong>{Object.keys(typeDistribution).length}</strong></p>
        <p>Total Equipment: <strong>{data.length}</strong></p>
      </div>
    </div>
  );
};

export default TypeDistributionChart;
