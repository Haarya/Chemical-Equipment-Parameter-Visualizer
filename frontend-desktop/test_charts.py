"""
Test script for Matplotlib chart widgets
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget
from charts.pie_chart import PieChart
from charts.bar_chart import BarChart
from charts.parameter_chart import ParameterChart


def main():
    """Test the chart widgets"""
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Chart Widgets Test")
    window.setGeometry(100, 100, 1200, 800)
    
    # Create central widget with tabs
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    tabs = QTabWidget()
    
    # Tab 1: Pie Chart
    pie_widget = QWidget()
    pie_layout = QVBoxLayout()
    pie_chart = PieChart(pie_widget)
    
    # Sample data for pie chart
    type_distribution = {
        'Pump': 8,
        'Reactor': 5,
        'Heat Exchanger': 7,
        'Compressor': 3,
        'Distillation Column': 2,
        'Storage Tank': 5
    }
    pie_chart.update_chart(type_distribution)
    pie_layout.addWidget(pie_chart)
    pie_widget.setLayout(pie_layout)
    tabs.addTab(pie_widget, "Pie Chart")
    
    # Tab 2: Bar Chart
    bar_widget = QWidget()
    bar_layout = QVBoxLayout()
    bar_chart = BarChart(bar_widget)
    
    # Sample data for bar chart
    bar_chart.update_chart(
        avg_flowrate=156.33,
        avg_pressure=25.67,
        avg_temperature=185.42
    )
    bar_layout.addWidget(bar_chart)
    bar_widget.setLayout(bar_layout)
    tabs.addTab(bar_widget, "Bar Chart")
    
    # Tab 3: Parameter Chart
    param_widget = QWidget()
    param_layout = QVBoxLayout()
    param_chart = ParameterChart(param_widget)
    
    # Sample data for parameter chart
    equipment_data = [
        {'equipment_name': 'P-101', 'equipment_type': 'Pump', 'flowrate': 120, 'pressure': 15, 'temperature': 80},
        {'equipment_name': 'P-102', 'equipment_type': 'Pump', 'flowrate': 150, 'pressure': 18, 'temperature': 85},
        {'equipment_name': 'R-201', 'equipment_type': 'Reactor', 'flowrate': 200, 'pressure': 35, 'temperature': 250},
        {'equipment_name': 'R-202', 'equipment_type': 'Reactor', 'flowrate': 180, 'pressure': 32, 'temperature': 245},
        {'equipment_name': 'E-301', 'equipment_type': 'Heat Exchanger', 'flowrate': 140, 'pressure': 12, 'temperature': 120},
        {'equipment_name': 'E-302', 'equipment_type': 'Heat Exchanger', 'flowrate': 135, 'pressure': 11, 'temperature': 115},
        {'equipment_name': 'C-401', 'equipment_type': 'Compressor', 'flowrate': 250, 'pressure': 45, 'temperature': 95},
    ]
    param_chart.update_chart(equipment_data, parameter='flowrate', equipment_type='All')
    param_layout.addWidget(param_chart)
    param_widget.setLayout(param_layout)
    tabs.addTab(param_widget, "Parameter Chart")
    
    layout.addWidget(tabs)
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
