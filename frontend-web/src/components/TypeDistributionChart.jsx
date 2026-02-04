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
    
    // Vibrant distinct color palette
    const colors = [
      'rgba(59, 130, 246, 0.8)',  // Blue
      'rgba(16, 185, 129, 0.8)',  // Emerald
      'rgba(251, 146, 60, 0.8)',  // Orange
      'rgba(168, 85, 247, 0.8)',  // Purple
      'rgba(236, 72, 153, 0.8)',  // Pink
      'rgba(14, 165, 233, 0.8)',  // Sky
      'rgba(245, 158, 11, 0.8)',  // Amber
      'rgba(239, 68, 68, 0.8)',   // Red
    ];

    const borderColors = [
      'rgba(59, 130, 246, 1)',
      'rgba(16, 185, 129, 1)',
      'rgba(251, 146, 60, 1)',
      'rgba(168, 85, 247, 1)',
      'rgba(236, 72, 153, 1)',
      'rgba(14, 165, 233, 1)',
      'rgba(245, 158, 11, 1)',
      'rgba(239, 68, 68, 1)',
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
