"""
Summary Widget for Chemical Equipment Visualizer Desktop Application
Displays dataset summary statistics
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                              QFrame, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SummaryCard(QFrame):
    """Individual card for displaying a summary metric"""
    
    def __init__(self, title: str, icon: str, color: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.icon = icon
        self.color = color
        self.init_ui()
        
    def init_ui(self):
        """Initialize the card UI"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {self.color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title with icon
        title_layout = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_font = QFont()
        icon_font.setPointSize(20)
        icon_label.setFont(icon_font)
        icon_label.setStyleSheet(f"color: {self.color}; border: none;")
        title_layout.addWidget(icon_label)
        
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(False)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: #666; border: none;")
        title_layout.addWidget(title_label, stretch=1)
        
        layout.addLayout(title_layout)
        
        # Value label
        self.value_label = QLabel("--")
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet(f"color: {self.color}; border: none;")
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        # Unit label
        self.unit_label = QLabel("")
        unit_font = QFont()
        unit_font.setPointSize(9)
        self.unit_label.setFont(unit_font)
        self.unit_label.setStyleSheet("color: #999; border: none;")
        self.unit_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.unit_label)
        
        self.setLayout(layout)
        
    def set_value(self, value, unit: str = ""):
        """Update the card value"""
        if value is None or value == "--":
            self.value_label.setText("--")
            self.unit_label.setText("")
        else:
            # Format number based on magnitude
            if isinstance(value, (int, float)):
                if value >= 1000:
                    formatted = f"{value:,.0f}"
                elif value >= 100:
                    formatted = f"{value:.1f}"
                else:
                    formatted = f"{value:.2f}"
            else:
                formatted = str(value)
                
            self.value_label.setText(formatted)
            self.unit_label.setText(unit)


class SummaryWidget(QWidget):
    """Widget displaying dataset summary statistics"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Dataset Summary")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Cards container
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        # Card 1: Total Equipment Count
        self.count_card = SummaryCard(
            "Total Equipment",
            "📊",
            "#3b82f6"  # Blue
        )
        cards_layout.addWidget(self.count_card)
        
        # Card 2: Average Flowrate
        self.flowrate_card = SummaryCard(
            "Avg Flowrate",
            "💧",
            "#10b981"  # Emerald
        )
        cards_layout.addWidget(self.flowrate_card)
        
        # Card 3: Average Pressure
        self.pressure_card = SummaryCard(
            "Avg Pressure",
            "⚡",
            "#fb923c"  # Orange
        )
        cards_layout.addWidget(self.pressure_card)
        
        # Card 4: Average Temperature
        self.temperature_card = SummaryCard(
            "Avg Temperature",
            "🌡️",
            "#ef4444"  # Red
        )
        cards_layout.addWidget(self.temperature_card)
        
        layout.addLayout(cards_layout)
        
        # Dataset info label
        self.info_label = QLabel("No dataset loaded")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 11px;
                padding: 10px;
                background-color: #f5f5f5;
                border-radius: 4px;
            }
        """)
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
        
    def update_summary(self, dataset_data: dict):
        """
        Update summary with dataset information
        
        Args:
            dataset_data: Dictionary containing:
                - total_records: int
                - avg_flowrate: float
                - avg_pressure: float
                - avg_temperature: float
                - name: str (optional)
                - uploaded_at: str (optional)
        """
        self.current_data = dataset_data
        
        # Update cards
        total_records = dataset_data.get('total_records', 0)
        self.count_card.set_value(total_records, "equipment")
        
        avg_flowrate = dataset_data.get('avg_flowrate', None)
        if avg_flowrate is not None:
            self.flowrate_card.set_value(avg_flowrate, "m³/h")
        else:
            self.flowrate_card.set_value("--")
            
        avg_pressure = dataset_data.get('avg_pressure', None)
        if avg_pressure is not None:
            self.pressure_card.set_value(avg_pressure, "bar")
        else:
            self.pressure_card.set_value("--")
            
        avg_temperature = dataset_data.get('avg_temperature', None)
        if avg_temperature is not None:
            self.temperature_card.set_value(avg_temperature, "°C")
        else:
            self.temperature_card.set_value("--")
        
        # Update info label
        dataset_name = dataset_data.get('name', 'Unknown')
        uploaded_at = dataset_data.get('uploaded_at', '')
        
        if uploaded_at:
            # Format timestamp if it's a full datetime string
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%B %d, %Y at %I:%M %p')
                info_text = f"Dataset: {dataset_name} | Uploaded: {formatted_date}"
            except:
                info_text = f"Dataset: {dataset_name} | Uploaded: {uploaded_at}"
        else:
            info_text = f"Dataset: {dataset_name}"
            
        self.info_label.setText(info_text)
        
    def clear_summary(self):
        """Clear all summary data"""
        self.current_data = None
        self.count_card.set_value("--")
        self.flowrate_card.set_value("--")
        self.pressure_card.set_value("--")
        self.temperature_card.set_value("--")
        self.info_label.setText("No dataset loaded")
        
    def update_from_equipment_list(self, equipment_list: list):
        """
        Calculate and update summary from equipment list
        
        Args:
            equipment_list: List of equipment dictionaries with keys:
                          'flowrate', 'pressure', 'temperature'
        """
        if not equipment_list or len(equipment_list) == 0:
            self.clear_summary()
            return
            
        total_records = len(equipment_list)
        
        # Calculate averages
        total_flowrate = sum(eq.get('flowrate', 0) for eq in equipment_list)
        total_pressure = sum(eq.get('pressure', 0) for eq in equipment_list)
        total_temperature = sum(eq.get('temperature', 0) for eq in equipment_list)
        
        avg_flowrate = total_flowrate / total_records if total_records > 0 else 0
        avg_pressure = total_pressure / total_records if total_records > 0 else 0
        avg_temperature = total_temperature / total_records if total_records > 0 else 0
        
        # Update summary
        summary_data = {
            'total_records': total_records,
            'avg_flowrate': avg_flowrate,
            'avg_pressure': avg_pressure,
            'avg_temperature': avg_temperature,
            'name': 'Current Dataset'
        }
        
        self.update_summary(summary_data)
