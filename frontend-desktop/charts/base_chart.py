"""
Base chart class for Matplotlib integration with PyQt5
"""

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class BaseChart(FigureCanvas):
    """Base class for all Matplotlib charts in PyQt5"""
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        """
        Initialize base chart
        
        Args:
            parent: Parent widget
            width: Figure width in inches
            height: Figure height in inches
            dpi: Dots per inch
        """
        # Create figure
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        
        # Initialize canvas
        super().__init__(self.figure)
        self.setParent(parent)
        
        # Configure default styling
        self.configure_style()
        
    def configure_style(self):
        """Configure default chart styling"""
        self.figure.patch.set_facecolor('#f8f9fa')
        self.axes.set_facecolor('#ffffff')
        self.axes.grid(True, alpha=0.3, linestyle='--')
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        
    def clear(self):
        """Clear the chart"""
        self.axes.clear()
        self.configure_style()
        
    def update_chart(self, data):
        """
        Update chart with new data (to be implemented by subclasses)
        
        Args:
            data: Data to plot
        """
        raise NotImplementedError("Subclasses must implement update_chart")
