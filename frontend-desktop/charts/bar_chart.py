"""
Bar Chart Widget for Average Parameters Comparison
"""

from charts.base_chart import BaseChart
import numpy as np


class BarChart(BaseChart):
    """Bar chart for comparing average parameters"""
    
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        super().__init__(parent, width, height, dpi)
        self.current_data = None
        
    def update_chart(self, avg_flowrate: float, avg_pressure: float, avg_temperature: float):
        """
        Update bar chart with average parameter values
        
        Args:
            avg_flowrate: Average flowrate value (m³/h)
            avg_pressure: Average pressure value (bar)
            avg_temperature: Average temperature value (°C)
        """
        self.current_data = {
            'flowrate': avg_flowrate,
            'pressure': avg_pressure,
            'temperature': avg_temperature
        }
        
        self.clear()
        
        # Prepare data
        parameters = ['Flowrate\n(m³/h)', 'Pressure\n(bar)', 'Temperature\n(°C)']
        values = [avg_flowrate, avg_pressure, avg_temperature]
        
        # Define colors matching the web frontend
        colors = ['#3b82f6', '#fb923c', '#ef4444']  # Blue, Orange, Red
        
        # Create bar positions
        x_pos = np.arange(len(parameters))
        
        # Create bars
        bars = self.axes.bar(
            x_pos,
            values,
            color=colors,
            alpha=0.8,
            edgecolor='white',
            linewidth=2
        )
        
        # Add value labels on top of bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            self.axes.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{value:.2f}',
                ha='center',
                va='bottom',
                fontsize=11,
                fontweight='bold'
            )
        
        # Customize axes
        self.axes.set_xlabel('Parameters', fontsize=12, fontweight='bold')
        self.axes.set_ylabel('Average Value', fontsize=12, fontweight='bold')
        self.axes.set_title(
            'Average Parameter Values',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        
        # Set x-axis labels
        self.axes.set_xticks(x_pos)
        self.axes.set_xticklabels(parameters, fontsize=10)
        
        # Add grid for better readability
        self.axes.grid(True, axis='y', alpha=0.3, linestyle='--')
        self.axes.set_axisbelow(True)
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Redraw
        self.draw()
        
    def show_no_data_message(self):
        """Display message when no data is available"""
        self.clear()
        self.axes.text(
            0.5, 0.5,
            'No data available',
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.axes.transAxes,
            fontsize=14,
            color='#999'
        )
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.draw()
