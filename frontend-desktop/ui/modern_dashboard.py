"""
ChemViz Pro - Modern Dashboard
Card-based layout with proper chart integration
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QFrame, QComboBox, QScrollArea, QSizePolicy, QMessageBox,
    QFileDialog, QSpacerItem
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from ui.styles import LIGHT_COLORS, CHART_COLORS
from ui.data_table_widget import DataTableWidget
from services.api_service import APIService

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Set up logging
logger = logging.getLogger(__name__)


class Card(QFrame):
    """Reusable card component with shadow and rounded corners"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setStyleSheet(f"""
            QFrame#Card {{
                background-color: {LIGHT_COLORS['surface']};
                border: 1px solid {LIGHT_COLORS['border_light']};
                border-radius: 12px;
            }}
        """)


class SummaryCard(QFrame):
    """Modern summary statistic card"""
    
    def __init__(self, icon: str, title: str, value: str, unit: str, accent: str = "blue", parent=None):
        super().__init__(parent)
        self.setObjectName("SummaryCard")
        self.accent = accent
        self.accent_colors = {
            'blue': LIGHT_COLORS['accent_blue'],
            'green': LIGHT_COLORS['primary'],
            'orange': LIGHT_COLORS['accent_orange'],
            'red': LIGHT_COLORS['accent_red'],
        }
        self.accent_color = self.accent_colors.get(self.accent, LIGHT_COLORS['accent_blue'])
        self.init_ui(icon, title, value, unit)
        
    def init_ui(self, icon: str, title: str, value: str, unit: str):
        self.setMinimumWidth(200)
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT_COLORS['surface']};
                border: none;
                border-left: 4px solid {self.accent_color};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Icon and title row
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        
        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        self.icon_label.setFixedWidth(28)
        self.icon_label.setFixedHeight(24)
        top_layout.addWidget(self.icon_label)
        
        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet(f"""
            font-size: 10px;
            font-weight: bold;
            color: {LIGHT_COLORS['text_secondary']};
            letter-spacing: 0.5px;
            border: none;
            background: transparent;
        """)
        self.title_label.setFixedHeight(20)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # Value - large, bold number
        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.value_label.setFixedHeight(50)
        self.value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 900;
            color: {self.accent_color};
            border: none;
            background: transparent;
            padding: 0px;
            margin: 0px;
        """)
        layout.addWidget(self.value_label)
        
        # Unit - small text below
        self.unit_label = QLabel(unit)
        self.unit_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.unit_label.setFixedHeight(18)
        self.unit_label.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 500;
            color: {LIGHT_COLORS['text_secondary']};
            border: none;
            background: transparent;
            padding: 0px;
            margin: 0px;
        """)
        layout.addWidget(self.unit_label)
    
    def update_value(self, value: str, unit: str = None):
        self.value_label.setText(value)
        if unit:
            self.unit_label.setText(unit)


class ModernPieChart(FigureCanvas):
    """Modern styled pie chart"""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.fig.set_facecolor(LIGHT_COLORS['surface'])
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def update_chart(self, data: dict):
        """Update pie chart with new data"""
        self.ax.clear()
        
        if not data:
            self.ax.text(0.5, 0.5, 'No data available', 
                        ha='center', va='center', fontsize=12, color=LIGHT_COLORS['text_secondary'])
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.axis('off')
            self.draw()
            return
        
        labels = list(data.keys())
        sizes = list(data.values())
        chart_colors = CHART_COLORS[:len(labels)]
        
        # Create pie chart
        wedges, texts, autotexts = self.ax.pie(
            sizes, 
            labels=labels,
            autopct='%1.1f%%',
            colors=chart_colors,
            startangle=90,
            wedgeprops={'linewidth': 2, 'edgecolor': 'white'}
        )
        
        # Style the text
        for text in texts:
            text.set_fontsize(10)
            text.set_color(LIGHT_COLORS['text'])
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        self.ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', 
                          color=LIGHT_COLORS['text'], pad=15)
        
        self.fig.tight_layout()
        self.draw()


class ModernBarChart(FigureCanvas):
    """Modern styled bar chart"""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.fig.set_facecolor(LIGHT_COLORS['surface'])
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def update_chart(self, flowrate: float, pressure: float, temperature: float):
        """Update bar chart with average parameters"""
        self.ax.clear()
        self.ax.set_facecolor(LIGHT_COLORS['surface'])
        
        categories = ['Flowrate\n(m³/h)', 'Pressure\n(bar)', 'Temperature\n(°C)']
        values = [flowrate, pressure, temperature]
        colors = [LIGHT_COLORS['accent_blue'], LIGHT_COLORS['accent_orange'], LIGHT_COLORS['accent_red']]
        
        bars = self.ax.bar(categories, values, color=colors, width=0.6, edgecolor='white', linewidth=2)
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            self.ax.annotate(f'{val:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 5),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           fontsize=11, fontweight='bold',
                           color=LIGHT_COLORS['text'])
        
        self.ax.set_title('Average Parameter Values', fontsize=14, fontweight='bold',
                          color=LIGHT_COLORS['text'], pad=15)
        self.ax.set_ylabel('Value', fontsize=10, color=LIGHT_COLORS['text_secondary'])
        
        # Style axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(LIGHT_COLORS['border'])
        self.ax.spines['bottom'].set_color(LIGHT_COLORS['border'])
        self.ax.tick_params(colors=LIGHT_COLORS['text_secondary'])
        
        # Grid
        self.ax.yaxis.grid(True, linestyle='--', alpha=0.3, color=LIGHT_COLORS['border'])
        self.ax.set_axisbelow(True)
        
        self.fig.tight_layout()
        self.draw()


class ModernLineChart(FigureCanvas):
    """Modern styled line chart for parameter trends"""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.fig.set_facecolor(LIGHT_COLORS['surface'])
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.total_count = 0
        
    def update_chart(self, equipment_data: list, parameter: str = 'flowrate', equipment_type: str = 'All'):
        """Update line chart with equipment parameter data"""
        self.ax.clear()
        self.ax.set_facecolor(LIGHT_COLORS['surface'])
        
        if not equipment_data:
            self.ax.text(0.5, 0.5, 'No data available',
                        ha='center', va='center', fontsize=12, color=LIGHT_COLORS['text_secondary'])
            self.total_count = 0
            self.draw()
            return
        
        # Filter by equipment type
        if equipment_type and equipment_type != 'All':
            filtered_data = [e for e in equipment_data if e.get('equipment_type') == equipment_type]
        else:
            filtered_data = equipment_data
        
        if not filtered_data:
            self.ax.text(0.5, 0.5, 'No data for selected filter',
                        ha='center', va='center', fontsize=12, color=LIGHT_COLORS['text_secondary'])
            self.total_count = 0
            self.draw()
            return
        
        self.total_count = len(filtered_data)
        
        # Extract data
        names = [e.get('equipment_name', f'Eq-{i}') for i, e in enumerate(filtered_data)]
        values = [e.get(parameter, 0) for e in filtered_data]
        
        # Determine chart style based on data size
        is_large_dataset = len(filtered_data) > 50
        
        # Plot
        x = range(len(names))
        color = LIGHT_COLORS['accent_blue'] if parameter == 'flowrate' else \
                LIGHT_COLORS['accent_orange'] if parameter == 'pressure' else LIGHT_COLORS['accent_red']
        
        if is_large_dataset:
            # For large datasets, use scatter plot without lines for better performance
            self.ax.scatter(x, values, s=20, alpha=0.7, color=color, edgecolors='white', linewidth=0.5)
            
            # Add trend line (moving average) for large datasets
            if len(values) > 10:
                import numpy as np
                window = min(20, len(values) // 10)
                if window > 1:
                    moving_avg = np.convolve(values, np.ones(window)/window, mode='valid')
                    x_smooth = range(window//2, len(values) - window//2 + 1)
                    self.ax.plot(x_smooth, moving_avg, linewidth=2, color=color, alpha=0.8, label='Trend')
            
            # Add horizontal lines for statistics
            import numpy as np
            mean_val = np.mean(values)
            self.ax.axhline(y=mean_val, color=color, linestyle='--', alpha=0.5, linewidth=1.5)
            self.ax.text(len(x) * 0.02, mean_val, f'Avg: {mean_val:.1f}', 
                        fontsize=9, color=color, va='bottom', fontweight='bold')
        else:
            # For small datasets, use the original line chart style
            line, = self.ax.plot(x, values, marker='o', linewidth=2.5, markersize=8,
                                color=color, markerfacecolor='white', markeredgewidth=2)
            
            # Fill under line
            self.ax.fill_between(x, values, alpha=0.1, color=color)
            
            # Add value labels only for small datasets
            for i, (xi, val) in enumerate(zip(x, values)):
                self.ax.annotate(f'{val:.1f}', (xi, val), textcoords="offset points",
                               xytext=(0, 10), ha='center', fontsize=8, color=LIGHT_COLORS['text'])
        
        # Labels
        param_labels = {'flowrate': 'Flowrate (m³/h)', 'pressure': 'Pressure (bar)', 'temperature': 'Temperature (°C)'}
        title = f'{param_labels.get(parameter, parameter)} Comparison'
        if equipment_type and equipment_type != 'All':
            title += f' - {equipment_type}'
        self.ax.set_title(title, fontsize=14, fontweight='bold', color=LIGHT_COLORS['text'], pad=15)
        self.ax.set_ylabel(param_labels.get(parameter, parameter), fontsize=10, color=LIGHT_COLORS['text_secondary'])
        
        # X-axis handling based on data size
        if is_large_dataset:
            # For large datasets, show fewer x-axis labels
            self.ax.set_xlabel(f'Equipment Index (Total: {len(filtered_data)})', fontsize=10, color=LIGHT_COLORS['text_secondary'])
            
            # Show only a few tick labels
            num_ticks = min(10, len(x))
            tick_positions = [int(i * (len(x) - 1) / (num_ticks - 1)) for i in range(num_ticks)] if num_ticks > 1 else [0]
            self.ax.set_xticks(tick_positions)
            tick_labels = [names[i][:15] + '...' if len(names[i]) > 15 else names[i] for i in tick_positions]
            self.ax.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=8)
        else:
            self.ax.set_xlabel('Equipment', fontsize=10, color=LIGHT_COLORS['text_secondary'])
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        
        # Style axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(LIGHT_COLORS['border'])
        self.ax.spines['bottom'].set_color(LIGHT_COLORS['border'])
        self.ax.tick_params(colors=LIGHT_COLORS['text_secondary'])
        
        # Grid
        self.ax.yaxis.grid(True, linestyle='--', alpha=0.3, color=LIGHT_COLORS['border'])
        self.ax.set_axisbelow(True)
        
        # Set reasonable y-axis limits with padding
        import numpy as np
        if values:
            y_min, y_max = min(values), max(values)
            y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 1
            self.ax.set_ylim(y_min - y_padding, y_max + y_padding)
        
        self.fig.tight_layout()
        self.draw()


class ModernDashboard(QWidget):
    """Modern card-based dashboard layout"""
    
    dataset_changed = pyqtSignal(int)
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.current_dataset_id = None
        self.current_dataset_data = None
        self.datasets_list = []
        self.init_ui()
        
    def init_ui(self):
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header row
        header_layout = QHBoxLayout()
        
        title = QLabel("Dashboard")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {LIGHT_COLORS['text']};
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Dataset selector
        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(280)
        self.dataset_combo.addItem("Select a dataset...")
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_selected)
        header_layout.addWidget(self.dataset_combo)
        
        # Refresh button - with explicit styling
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_COLORS['primary_hover']};
            }}
        """)
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        # Download PDF button - with explicit styling
        self.pdf_btn = QPushButton("Download PDF")
        self.pdf_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_COLORS['accent_red']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #DC2626;
            }}
            QPushButton:disabled {{
                background-color: #9CA3AF;
            }}
        """)
        self.pdf_btn.setEnabled(False)
        self.pdf_btn.clicked.connect(self.download_pdf)
        header_layout.addWidget(self.pdf_btn)
        
        layout.addLayout(header_layout)
        
        # Dataset info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet(f"color: {LIGHT_COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(self.info_label)
        
        # Summary cards row
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        self.total_card = SummaryCard("📊", "Total Equipment", "0", "equipment", "blue")
        summary_layout.addWidget(self.total_card)
        
        self.flowrate_card = SummaryCard("💧", "Avg Flowrate", "0.00", "m³/h", "green")
        summary_layout.addWidget(self.flowrate_card)
        
        self.pressure_card = SummaryCard("⚡", "Avg Pressure", "0.00", "bar", "orange")
        summary_layout.addWidget(self.pressure_card)
        
        self.temp_card = SummaryCard("🌡️", "Avg Temperature", "0.00", "°C", "red")
        summary_layout.addWidget(self.temp_card)
        
        layout.addLayout(summary_layout)
        
        # Charts section title
        charts_title = QLabel("📈 Data Visualization")
        charts_title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {LIGHT_COLORS['text']};
            padding-top: 10px;
        """)
        layout.addWidget(charts_title)
        
        # Charts row 1: Pie and Bar
        charts_row1 = QHBoxLayout()
        charts_row1.setSpacing(15)
        
        # Pie chart card
        pie_card = Card()
        pie_layout = QVBoxLayout(pie_card)
        pie_layout.setContentsMargins(15, 15, 15, 15)
        self.pie_chart = ModernPieChart()
        self.pie_chart.setMinimumHeight(350)
        pie_layout.addWidget(self.pie_chart)
        charts_row1.addWidget(pie_card)
        
        # Bar chart card
        bar_card = Card()
        bar_layout = QVBoxLayout(bar_card)
        bar_layout.setContentsMargins(15, 15, 15, 15)
        self.bar_chart = ModernBarChart()
        self.bar_chart.setMinimumHeight(350)
        bar_layout.addWidget(self.bar_chart)
        charts_row1.addWidget(bar_card)
        
        layout.addLayout(charts_row1)
        
        # Line chart card
        line_card = Card()
        line_layout = QVBoxLayout(line_card)
        line_layout.setContentsMargins(15, 15, 15, 15)
        
        # Controls for line chart
        line_controls = QHBoxLayout()
        line_controls.addWidget(QLabel("Parameter:"))
        
        self.param_combo = QComboBox()
        self.param_combo.addItems(["Flowrate", "Pressure", "Temperature"])
        self.param_combo.currentTextChanged.connect(self.update_line_chart)
        line_controls.addWidget(self.param_combo)
        
        line_controls.addWidget(QLabel("Equipment Type:"))
        
        self.type_combo = QComboBox()
        self.type_combo.addItem("All")
        self.type_combo.currentTextChanged.connect(self.update_line_chart)
        line_controls.addWidget(self.type_combo)
        
        line_controls.addStretch()
        line_layout.addLayout(line_controls)
        
        self.line_chart = ModernLineChart()
        self.line_chart.setMinimumHeight(300)
        line_layout.addWidget(self.line_chart)
        
        # Status label for line chart
        self.line_chart_status = QLabel("")
        self.line_chart_status.setAlignment(Qt.AlignCenter)
        self.line_chart_status.setStyleSheet(f"""
            color: {LIGHT_COLORS['text_secondary']};
            font-size: 12px;
            padding: 5px;
        """)
        line_layout.addWidget(self.line_chart_status)
        
        layout.addWidget(line_card)
        
        # Data table section
        table_title = QLabel("📋 Equipment Data Table")
        table_title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {LIGHT_COLORS['text']};
            padding-top: 10px;
        """)
        layout.addWidget(table_title)
        
        # Table card
        table_card = Card()
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        self.data_table = DataTableWidget()
        self.data_table.setMinimumHeight(300)
        table_layout.addWidget(self.data_table)
        
        layout.addWidget(table_card)
        
        # Add stretch at end
        layout.addStretch()
        
        scroll.setWidget(content)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def load_datasets_list(self):
        """Load available datasets"""
        try:
            datasets = self.api_service.get_datasets()
            self.datasets_list = datasets
            
            self.dataset_combo.clear()
            self.dataset_combo.addItem("Select a dataset...")
            
            for ds in datasets:
                text = f"{ds['name']} ({ds['total_records']} records)"
                self.dataset_combo.addItem(text, ds['id'])
                
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
    
    def on_dataset_selected(self, index):
        """Handle dataset selection"""
        dataset_id = self.dataset_combo.itemData(index)
        if dataset_id:
            self.load_dataset(dataset_id)
    
    def load_dataset(self, dataset_id: int):
        """Load and display dataset"""
        try:
            data = self.api_service.get_dataset_detail(dataset_id)
            self.current_dataset_id = dataset_id
            self.current_dataset_data = data
            
            # Update info label
            self.info_label.setText(f"Dataset: {data.get('name', 'Unknown')} | "
                                   f"Uploaded: {data.get('uploaded_at', 'Unknown')[:10]}")
            
            # Update summary cards
            self.total_card.update_value(str(data.get('total_records', 0)))
            self.flowrate_card.update_value(f"{data.get('avg_flowrate', 0):.2f}")
            self.pressure_card.update_value(f"{data.get('avg_pressure', 0):.2f}")
            self.temp_card.update_value(f"{data.get('avg_temperature', 0):.2f}")
            
            # Update charts
            type_dist = data.get('type_distribution', {})
            self.pie_chart.update_chart(type_dist)
            
            self.bar_chart.update_chart(
                data.get('avg_flowrate', 0),
                data.get('avg_pressure', 0),
                data.get('avg_temperature', 0)
            )
            
            # Update type filter
            self.type_combo.clear()
            self.type_combo.addItem("All")
            for eq_type in type_dist.keys():
                self.type_combo.addItem(eq_type)
            
            # Update line chart
            # API returns 'equipment_records', not 'equipment'
            equipment = data.get('equipment_records', [])
            self.line_chart.update_chart(equipment, 'flowrate', 'All')
            
            # Update table
            self.data_table.update_table(equipment)
            
            # Enable PDF button
            self.pdf_btn.setEnabled(True)
            
            # Update combo to reflect selection
            for i in range(self.dataset_combo.count()):
                if self.dataset_combo.itemData(i) == dataset_id:
                    self.dataset_combo.setCurrentIndex(i)
                    break
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load dataset:\n{str(e)}")
    
    def update_line_chart(self):
        """Update line chart with current filter settings"""
        if not self.current_dataset_data:
            self.line_chart_status.setText("")
            return
        
        param_map = {"Flowrate": "flowrate", "Pressure": "pressure", "Temperature": "temperature"}
        param = param_map.get(self.param_combo.currentText(), "flowrate")
        eq_type = self.type_combo.currentText()
        
        # API returns 'equipment_records', not 'equipment'
        equipment = self.current_dataset_data.get('equipment_records', [])
        self.line_chart.update_chart(equipment, param, eq_type)
        
        # Update status label
        count = self.line_chart.total_count
        if count > 0:
            self.line_chart_status.setText(f"Showing {count} equipment{'s' if count > 1 else ''}")
        else:
            self.line_chart_status.setText("")
    
    def refresh_data(self):
        """Refresh current dataset"""
        self.load_datasets_list()
        if self.current_dataset_id:
            self.load_dataset(self.current_dataset_id)
    
    def download_pdf(self):
        """Download PDF report"""
        if not self.current_dataset_id:
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", 
            f"equipment_report_{self.current_dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if filename:
            try:
                self.api_service.download_pdf_report(self.current_dataset_id, filename)
                QMessageBox.information(self, "Success", f"PDF saved to:\n{filename}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to download PDF:\n{str(e)}")
    
    def clear_dashboard(self):
        """Clear all dashboard data"""
        self.current_dataset_id = None
        self.current_dataset_data = None
        self.dataset_combo.clear()
        self.dataset_combo.addItem("Select a dataset...")
        self.info_label.setText("")
        self.total_card.update_value("0")
        self.flowrate_card.update_value("0.00")
        self.pressure_card.update_value("0.00")
        self.temp_card.update_value("0.00")
        self.pie_chart.update_chart({})
        self.bar_chart.update_chart(0, 0, 0)
        self.line_chart.update_chart([], 'flowrate', 'All')
        self.data_table.clear_table()
        self.pdf_btn.setEnabled(False)
