"""
Data Table Widget for Chemical Equipment Visualizer Desktop Application
Displays equipment data in a sortable table
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QTableWidgetItem, QHeaderView, QLineEdit, QLabel,
                              QPushButton, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DataTableWidget(QWidget):
    """Widget for displaying equipment data in a table"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_data = []
        self.filtered_data = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Header with title and search
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Equipment Data Table")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Search box
        search_label = QLabel("Search:")
        header_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter by name or type...")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.filter_data)
        header_layout.addWidget(self.search_input)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'Equipment Name',
            'Type',
            'Flowrate (m³/h)',
            'Pressure (bar)',
            'Temperature (°C)'
        ])
        
        # Table styling
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(True)
        
        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Equipment Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Flowrate
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Pressure
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Temperature
        
        # Vertical header
        self.table.verticalHeader().setVisible(True)
        
        layout.addWidget(self.table)
        
        # Footer with row count
        self.footer_label = QLabel("No data loaded")
        self.footer_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.footer_label)
        
        self.setLayout(layout)
        
    def update_table(self, equipment_data: list):
        """
        Update table with equipment data
        
        Args:
            equipment_data: List of equipment dictionaries with keys:
                          'equipment_name', 'equipment_type', 'flowrate',
                          'pressure', 'temperature'
        """
        self.current_data = equipment_data
        self.filtered_data = equipment_data.copy()
        self.search_input.clear()
        self.populate_table(self.filtered_data)
        
    def populate_table(self, data: list):
        """Populate table with data"""
        # Disable sorting while populating
        self.table.setSortingEnabled(False)
        
        # Clear and set row count
        self.table.setRowCount(len(data))
        
        # Populate rows
        for row, equipment in enumerate(data):
            # Equipment Name
            name_item = QTableWidgetItem(str(equipment.get('equipment_name', '')))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(str(equipment.get('equipment_type', '')))
            type_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, type_item)
            
            # Flowrate
            flowrate = equipment.get('flowrate', 0)
            flowrate_item = QTableWidgetItem(f"{flowrate:.2f}")
            flowrate_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, flowrate_item)
            
            # Pressure
            pressure = equipment.get('pressure', 0)
            pressure_item = QTableWidgetItem(f"{pressure:.2f}")
            pressure_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, pressure_item)
            
            # Temperature
            temperature = equipment.get('temperature', 0)
            temperature_item = QTableWidgetItem(f"{temperature:.2f}")
            temperature_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, temperature_item)
        
        # Re-enable sorting
        self.table.setSortingEnabled(True)
        
        # Update footer
        total_count = len(self.current_data)
        showing_count = len(data)
        
        if total_count == showing_count:
            self.footer_label.setText(f"Showing {showing_count} equipment records")
        else:
            self.footer_label.setText(
                f"Showing {showing_count} of {total_count} equipment records (filtered)"
            )
        
    def filter_data(self):
        """Filter table data based on search input"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self.filtered_data = self.current_data.copy()
        else:
            self.filtered_data = [
                eq for eq in self.current_data
                if search_text in eq.get('equipment_name', '').lower() or
                   search_text in eq.get('equipment_type', '').lower()
            ]
        
        self.populate_table(self.filtered_data)
        
    def clear_table(self):
        """Clear all table data"""
        self.current_data = []
        self.filtered_data = []
        self.table.setRowCount(0)
        self.search_input.clear()
        self.footer_label.setText("No data loaded")
