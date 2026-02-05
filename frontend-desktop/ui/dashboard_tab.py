"""
Dashboard Tab for Chemical Equipment Visualizer Desktop Application
Combines all visualization components
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QComboBox, QLabel, QSplitter, QMessageBox,
                              QFileDialog, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from ui.summary_widget import SummaryWidget
from ui.data_table_widget import DataTableWidget
from charts.pie_chart import PieChart
from charts.bar_chart import BarChart
from charts.parameter_chart import ParameterChart
from services.api_service import APIService
import requests


class DashboardTab(QWidget):
    """Dashboard tab combining all visualization components"""
    
    dataset_changed = pyqtSignal(int)  # Emits dataset ID when selection changes
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.current_dataset_id = None
        self.current_dataset_data = None
        self.datasets_list = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Top control bar
        control_layout = QHBoxLayout()
        
        # Dataset selector
        dataset_label = QLabel("Dataset:")
        dataset_label_font = QFont()
        dataset_label_font.setBold(True)
        dataset_label.setFont(dataset_label_font)
        control_layout.addWidget(dataset_label)
        
        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(300)
        self.dataset_combo.addItem("No dataset selected", None)
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_selected)
        control_layout.addWidget(self.dataset_combo)
        
        control_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_data)
        control_layout.addWidget(self.refresh_btn)
        
        # Download PDF button
        self.pdf_btn = QPushButton("📄 Download PDF")
        self.pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
            QPushButton:disabled {
                background-color: #9e9e9e;
            }
        """)
        self.pdf_btn.setEnabled(False)
        self.pdf_btn.clicked.connect(self.download_pdf)
        control_layout.addWidget(self.pdf_btn)
        
        layout.addLayout(control_layout)
        
        # Main content with splitters
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setChildrenCollapsible(False)
        
        # Top section: Summary
        self.summary_widget = SummaryWidget()
        self.summary_widget.setMinimumHeight(120)
        self.summary_widget.setMaximumHeight(150)
        main_splitter.addWidget(self.summary_widget)
        
        # Middle section: Charts
        charts_widget = QWidget()
        charts_layout = QVBoxLayout()
        charts_layout.setSpacing(15)
        charts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Charts title
        charts_title = QLabel("Data Visualization")
        charts_title_font = QFont()
        charts_title_font.setPointSize(13)
        charts_title_font.setBold(True)
        charts_title.setFont(charts_title_font)
        charts_layout.addWidget(charts_title)
        
        # Charts row 1: Pie and Bar charts in horizontal layout
        charts_row1_widget = QWidget()
        charts_row1 = QHBoxLayout()
        charts_row1.setSpacing(10)
        
        # Pie chart container
        pie_container = QGroupBox("Equipment Type Distribution")
        pie_layout = QVBoxLayout()
        self.pie_chart = PieChart(width=5, height=4)
        self.pie_chart.setMinimumSize(400, 300)
        pie_layout.addWidget(self.pie_chart)
        pie_container.setLayout(pie_layout)
        charts_row1.addWidget(pie_container)
        
        # Bar chart container
        bar_container = QGroupBox("Average Parameters")
        bar_layout = QVBoxLayout()
        self.bar_chart = BarChart(width=5, height=4)
        self.bar_chart.setMinimumSize(400, 300)
        bar_layout.addWidget(self.bar_chart)
        bar_container.setLayout(bar_layout)
        charts_row1.addWidget(bar_container)
        
        charts_row1_widget.setLayout(charts_row1)
        charts_row1_widget.setMinimumHeight(350)
        charts_layout.addWidget(charts_row1_widget)
        
        # Charts row 2: Parameter chart with controls
        param_group = QGroupBox("Parameter Trends")
        param_layout = QVBoxLayout()
        
        # Parameter chart controls
        param_controls = QHBoxLayout()
        
        param_controls.addWidget(QLabel("Parameter:"))
        self.param_combo = QComboBox()
        self.param_combo.addItem("Flowrate", "flowrate")
        self.param_combo.addItem("Pressure", "pressure")
        self.param_combo.addItem("Temperature", "temperature")
        self.param_combo.currentIndexChanged.connect(self.update_parameter_chart)
        param_controls.addWidget(self.param_combo)
        
        param_controls.addWidget(QLabel("Equipment Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItem("All", "All")
        self.type_combo.currentIndexChanged.connect(self.update_parameter_chart)
        param_controls.addWidget(self.type_combo)
        
        param_controls.addStretch()
        param_layout.addLayout(param_controls)
        
        self.param_chart = ParameterChart(width=10, height=4)
        self.param_chart.setMinimumSize(800, 300)
        param_layout.addWidget(self.param_chart)
        
        param_group.setLayout(param_layout)
        param_group.setMinimumHeight(380)
        charts_layout.addWidget(param_group)
        
        charts_widget.setLayout(charts_layout)
        main_splitter.addWidget(charts_widget)
        
        # Bottom section: Data table
        table_widget = QWidget()
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        table_title = QLabel("Equipment Data Table")
        table_title_font = QFont()
        table_title_font.setPointSize(13)
        table_title_font.setBold(True)
        table_title.setFont(table_title_font)
        table_layout.addWidget(table_title)
        
        self.data_table = DataTableWidget()
        self.data_table.setMinimumHeight(200)
        table_layout.addWidget(self.data_table)
        
        table_widget.setLayout(table_layout)
        main_splitter.addWidget(table_widget)
        
        # Set initial splitter sizes (summary:charts:table)
        main_splitter.setSizes([140, 750, 250])
        main_splitter.setStretchFactor(0, 0)  # Summary doesn't stretch
        main_splitter.setStretchFactor(1, 3)  # Charts get most space
        main_splitter.setStretchFactor(2, 1)  # Table gets some space
        
        layout.addWidget(main_splitter)
        
        self.setLayout(layout)
        
    def load_datasets_list(self):
        """Load list of available datasets"""
        try:
            datasets = self.api_service.get_datasets()
            self.datasets_list = datasets
            
            # Update combo box
            self.dataset_combo.clear()
            self.dataset_combo.addItem("Select a dataset...", None)
            
            for dataset in datasets:
                display_text = f"{dataset['name']} ({dataset['total_records']} records)"
                self.dataset_combo.addItem(display_text, dataset['id'])
                
        except Exception as e:
            QMessageBox.warning(
                self,
                "Load Failed",
                f"Could not load datasets list:\n{str(e)}"
            )
            
    def on_dataset_selected(self, index):
        """Handle dataset selection"""
        dataset_id = self.dataset_combo.itemData(index)
        
        if dataset_id is None:
            self.clear_dashboard()
            return
            
        self.load_dataset(dataset_id)
        
    def load_dataset(self, dataset_id: int):
        """Load and display dataset"""
        try:
            # Fetch dataset details
            data = self.api_service.get_dataset_detail(dataset_id)
            
            self.current_dataset_id = dataset_id
            self.current_dataset_data = data
            
            # Update summary
            self.summary_widget.update_summary(data)
            
            # Update charts
            self.update_charts(data)
            
            # Update data table
            equipment_records = data.get('equipment_records', [])
            self.data_table.update_table(equipment_records)
            
            # Populate equipment type filter
            self.populate_type_filter(equipment_records)
            
            # Enable PDF button
            self.pdf_btn.setEnabled(True)
            
            # Emit signal
            self.dataset_changed.emit(dataset_id)
            
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self,
                "Connection Error",
                "Cannot connect to server. Please check if backend is running."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Load Failed",
                f"Could not load dataset:\n{str(e)}"
            )
            
    def update_charts(self, data: dict):
        """Update all charts with dataset data"""
        # Pie chart - type distribution
        type_distribution = data.get('type_distribution', {})
        self.pie_chart.update_chart(type_distribution)
        
        # Bar chart - averages
        self.bar_chart.update_chart(
            data.get('avg_flowrate', 0),
            data.get('avg_pressure', 0),
            data.get('avg_temperature', 0)
        )
        
        # Parameter chart
        self.update_parameter_chart()
        
    def update_parameter_chart(self):
        """Update parameter chart based on current selections"""
        if not self.current_dataset_data:
            return
            
        equipment_records = self.current_dataset_data.get('equipment_records', [])
        parameter = self.param_combo.currentData()
        equipment_type = self.type_combo.currentData()
        
        self.param_chart.update_chart(
            equipment_records,
            parameter=parameter,
            equipment_type=equipment_type
        )
        
    def populate_type_filter(self, equipment_records: list):
        """Populate equipment type filter"""
        # Get unique types
        types = set(eq.get('equipment_type', 'Unknown') for eq in equipment_records)
        
        # Update combo
        current_selection = self.type_combo.currentData()
        self.type_combo.clear()
        self.type_combo.addItem("All", "All")
        
        for eq_type in sorted(types):
            self.type_combo.addItem(eq_type, eq_type)
            
        # Restore selection if possible
        index = self.type_combo.findData(current_selection)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
            
    def refresh_data(self):
        """Refresh current dataset"""
        if self.current_dataset_id:
            self.load_dataset(self.current_dataset_id)
        else:
            self.load_datasets_list()
            
    def download_pdf(self):
        """Download PDF report for current dataset"""
        if not self.current_dataset_id:
            return
            
        # Ask user where to save
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"report_dataset_{self.current_dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
            
        try:
            success = self.api_service.download_pdf_report(
                self.current_dataset_id,
                file_path
            )
            
            if success:
                QMessageBox.information(
                    self,
                    "Download Complete",
                    f"PDF report saved to:\n{file_path}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Download Failed",
                f"Could not download PDF report:\n{str(e)}"
            )
            
    def clear_dashboard(self):
        """Clear all dashboard content"""
        self.current_dataset_id = None
        self.current_dataset_data = None
        self.summary_widget.clear_summary()
        self.pie_chart.show_no_data_message()
        self.bar_chart.show_no_data_message()
        self.param_chart.show_no_data_message()
        self.data_table.clear_table()
        self.pdf_btn.setEnabled(False)
