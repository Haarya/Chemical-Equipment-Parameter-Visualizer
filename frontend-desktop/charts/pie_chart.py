"""
Pie Chart Widget for Equipment Type Distribution
"""

from charts.base_chart import BaseChart
import matplotlib.pyplot as plt


class PieChart(BaseChart):
    """Pie chart for displaying equipment type distribution"""
    
    def __init__(self, parent=None, width=6, height=5, dpi=100):
        super().__init__(parent, width, height, dpi)
        self.current_data = None
        
    def configure_style(self):
        """Configure pie chart styling"""
        self.figure.patch.set_facecolor('#f8f9fa')
        self.axes.set_facecolor('#ffffff')
        # Pie charts don't need grid or spines
        
    def update_chart(self, type_distribution: dict):
        """
        Update pie chart with equipment type distribution data
        
        Args:
            type_distribution: Dictionary with equipment types as keys and counts as values
                             e.g., {"Pump": 5, "Reactor": 3, "Heat Exchanger": 7}
        """
        if not type_distribution or len(type_distribution) == 0:
            self.show_no_data_message()
            return
            
        self.current_data = type_distribution
        self.clear()
        
        # Prepare data
        labels = list(type_distribution.keys())
        sizes = list(type_distribution.values())
        
        # Define distinct colors matching the web frontend
        colors = [
            '#3b82f6',  # Blue
            '#10b981',  # Emerald
            '#fb923c',  # Orange
            '#a855f7',  # Purple
            '#ec4899',  # Pink
            '#0ea5e9',  # Sky
            '#f59e0b',  # Amber
            '#ef4444',  # Red
        ]
        
        # Create pie chart with percentage labels
        wedges, texts, autotexts = self.axes.pie(
            sizes,
            labels=labels,
            colors=colors[:len(labels)],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10}
        )
        
        # Style percentage labels
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        # Style labels
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        
        # Equal aspect ratio ensures pie is circular
        self.axes.axis('equal')
        
        # Add title
        self.axes.set_title(
            'Equipment Type Distribution',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        
        # Add legend with counts
        legend_labels = [f'{label}: {count}' for label, count in zip(labels, sizes)]
        self.axes.legend(
            legend_labels,
            loc='center left',
            bbox_to_anchor=(1, 0.5),
            fontsize=9
        )
        
        # Adjust layout to prevent legend cutoff
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
