"""
Parameter Chart Widget for Individual Equipment Parameter Comparison
"""

from charts.base_chart import BaseChart
import numpy as np


class ParameterChart(BaseChart):
    """Line/scatter chart for parameter comparison with filtering"""
    
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        super().__init__(parent, width, height, dpi)
        self.current_data = None
        self.current_parameter = 'flowrate'
        self.current_equipment_type = 'All'
        
    def update_chart(self, equipment_data: list, parameter: str = 'flowrate', 
                     equipment_type: str = 'All'):
        """
        Update chart with equipment parameter data
        
        Args:
            equipment_data: List of equipment dictionaries with keys:
                          'equipment_name', 'equipment_type', 'flowrate', 
                          'pressure', 'temperature'
            parameter: Parameter to display ('flowrate', 'pressure', or 'temperature')
            equipment_type: Filter by equipment type ('All' for no filter)
        """
        if not equipment_data or len(equipment_data) == 0:
            self.show_no_data_message()
            return
            
        self.current_data = equipment_data
        self.current_parameter = parameter
        self.current_equipment_type = equipment_type
        
        # Filter data by equipment type if specified
        if equipment_type != 'All':
            filtered_data = [
                eq for eq in equipment_data 
                if eq.get('equipment_type') == equipment_type
            ]
        else:
            filtered_data = equipment_data
            
        if not filtered_data:
            self.show_no_data_message(f"No data for {equipment_type}")
            return
        
        self.clear()
        
        # Prepare data
        equipment_names = [eq.get('equipment_name', f"Eq-{i}") 
                          for i, eq in enumerate(filtered_data)]
        
        # Get parameter values
        if parameter == 'flowrate':
            values = [eq.get('flowrate', 0) for eq in filtered_data]
            param_label = 'Flowrate (m³/h)'
            color = '#3b82f6'  # Blue
        elif parameter == 'pressure':
            values = [eq.get('pressure', 0) for eq in filtered_data]
            param_label = 'Pressure (bar)'
            color = '#fb923c'  # Orange
        else:  # temperature
            values = [eq.get('temperature', 0) for eq in filtered_data]
            param_label = 'Temperature (°C)'
            color = '#ef4444'  # Red
        
        # Create x-axis positions
        x_pos = np.arange(len(equipment_names))
        
        # Plot line chart with markers
        self.axes.plot(
            x_pos,
            values,
            color=color,
            linewidth=2,
            marker='o',
            markersize=8,
            markerfacecolor=color,
            markeredgecolor='white',
            markeredgewidth=2,
            label=param_label
        )
        
        # Add value labels on points
        for i, (x, y) in enumerate(zip(x_pos, values)):
            self.axes.annotate(
                f'{y:.1f}',
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),
                ha='center',
                fontsize=8,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor=color, alpha=0.8)
            )
        
        # Fill area under line
        self.axes.fill_between(
            x_pos,
            values,
            alpha=0.2,
            color=color
        )
        
        # Customize axes
        self.axes.set_xlabel('Equipment', fontsize=12, fontweight='bold')
        self.axes.set_ylabel(param_label, fontsize=12, fontweight='bold')
        
        # Create title
        title = f'{param_label} Comparison'
        if equipment_type != 'All':
            title += f' - {equipment_type}'
        self.axes.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Set x-axis labels
        self.axes.set_xticks(x_pos)
        self.axes.set_xticklabels(
            equipment_names,
            rotation=45,
            ha='right',
            fontsize=9
        )
        
        # Add legend
        self.axes.legend(loc='upper left', fontsize=10)
        
        # Add grid
        self.axes.grid(True, alpha=0.3, linestyle='--')
        self.axes.set_axisbelow(True)
        
        # Adjust layout to prevent label cutoff
        self.figure.tight_layout()
        
        # Redraw
        self.draw()
        
    def show_no_data_message(self, message: str = 'No data available'):
        """Display message when no data is available"""
        self.clear()
        self.axes.text(
            0.5, 0.5,
            message,
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.axes.transAxes,
            fontsize=14,
            color='#999'
        )
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.draw()
        
    def change_parameter(self, parameter: str):
        """Change the displayed parameter"""
        if self.current_data:
            self.update_chart(
                self.current_data,
                parameter,
                self.current_equipment_type
            )
            
    def change_equipment_type(self, equipment_type: str):
        """Change the equipment type filter"""
        if self.current_data:
            self.update_chart(
                self.current_data,
                self.current_parameter,
                equipment_type
            )
