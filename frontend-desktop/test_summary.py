"""
Test script for Summary Widget
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from ui.summary_widget import SummaryWidget


def main():
    """Test the summary widget"""
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Summary Widget Test")
    window.setGeometry(100, 100, 1000, 300)
    
    # Create central widget
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    # Create summary widget
    summary = SummaryWidget()
    layout.addWidget(summary)
    
    # Add test buttons
    btn_layout = QVBoxLayout()
    
    def load_sample_data():
        """Load sample dataset"""
        dataset_data = {
            'name': 'sample_equipment_data.csv',
            'total_records': 30,
            'avg_flowrate': 156.33,
            'avg_pressure': 25.67,
            'avg_temperature': 185.42,
            'uploaded_at': '2026-02-04T10:30:00'
        }
        summary.update_summary(dataset_data)
    
    def load_from_list():
        """Calculate from equipment list"""
        equipment_list = [
            {'flowrate': 120, 'pressure': 15, 'temperature': 80},
            {'flowrate': 150, 'pressure': 18, 'temperature': 85},
            {'flowrate': 200, 'pressure': 35, 'temperature': 250},
            {'flowrate': 180, 'pressure': 32, 'temperature': 245},
            {'flowrate': 140, 'pressure': 12, 'temperature': 120},
        ]
        summary.update_from_equipment_list(equipment_list)
    
    def clear_data():
        """Clear all data"""
        summary.clear_summary()
    
    btn1 = QPushButton("Load Sample Dataset")
    btn1.clicked.connect(load_sample_data)
    btn_layout.addWidget(btn1)
    
    btn2 = QPushButton("Calculate from Equipment List")
    btn2.clicked.connect(load_from_list)
    btn_layout.addWidget(btn2)
    
    btn3 = QPushButton("Clear Data")
    btn3.clicked.connect(clear_data)
    btn_layout.addWidget(btn3)
    
    layout.addLayout(btn_layout)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    
    # Load initial sample data
    load_sample_data()
    
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
