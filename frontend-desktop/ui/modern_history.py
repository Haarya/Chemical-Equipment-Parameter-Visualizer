"""
ChemViz Pro - Modern History Tab
Clean list view of uploaded datasets
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QListWidget, QListWidgetItem, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from ui.styles import LIGHT_COLORS, DARK_COLORS
from services.api_service import APIService
from datetime import datetime
import requests


class DatasetCard(QFrame):
    """Individual dataset card in the history list - minimal design"""
    
    delete_clicked = pyqtSignal(int)
    view_clicked = pyqtSignal(int)
    
    def __init__(self, dataset: dict, parent=None):
        super().__init__(parent)
        self.dataset = dataset
        self.dataset_id = dataset.get('id')
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT_COLORS['surface']};
                border: 1px solid {LIGHT_COLORS['border_light']};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border-color: {LIGHT_COLORS['primary']};
                background-color: #FAFAFA;
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # File icon
        icon_label = QLabel("📄")
        icon_label.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        icon_label.setFixedWidth(30)
        layout.addWidget(icon_label)
        
        # Info section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name = self.dataset.get('name', 'Unknown')
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {LIGHT_COLORS['text']};
            border: none;
            background: transparent;
        """)
        info_layout.addWidget(name_label)
        
        # Meta info row
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(20)
        
        records = self.dataset.get('total_records', 0)
        records_label = QLabel(f"📊 {records} records")
        records_label.setStyleSheet(f"color: {LIGHT_COLORS['text_secondary']}; font-size: 11px; border: none; background: transparent;")
        meta_layout.addWidget(records_label)
        
        # Format date
        uploaded_at = self.dataset.get('uploaded_at', '')
        try:
            if uploaded_at:
                dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%b %d, %Y')
            else:
                formatted_date = 'Unknown'
        except:
            formatted_date = uploaded_at[:10] if uploaded_at else 'Unknown'
        
        date_label = QLabel(f"📅 {formatted_date}")
        date_label.setStyleSheet(f"color: {LIGHT_COLORS['text_secondary']}; font-size: 11px; border: none; background: transparent;")
        meta_layout.addWidget(date_label)
        meta_layout.addStretch()
        
        info_layout.addLayout(meta_layout)
        layout.addLayout(info_layout, 1)
        
        # Action buttons
        # View button
        view_btn = QPushButton("View")
        view_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_COLORS['primary']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_COLORS['primary_hover']};
            }}
        """)
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.setFixedHeight(28)
        view_btn.clicked.connect(lambda: self.view_clicked.emit(self.dataset_id))
        layout.addWidget(view_btn)
        
        # Delete button - simple X
        delete_btn = QPushButton("×")
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {LIGHT_COLORS['border']};
                border-radius: 4px;
                color: {LIGHT_COLORS['text_secondary']};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #FEE2E2;
                color: #DC2626;
                border-color: #DC2626;
            }}
        """)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setFixedSize(28, 28)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.dataset_id))
        layout.addWidget(delete_btn)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.view_clicked.emit(self.dataset_id)


class ModernHistoryTab(QWidget):
    """Modern history tab with card-based dataset list"""
    
    dataset_selected = pyqtSignal(int)
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.datasets = []
        self.init_ui()
        
    def init_ui(self):
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        # Content
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("Dataset History")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {LIGHT_COLORS['text']};
        """)
        header.addWidget(title)
        
        header.addStretch()
        
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
        refresh_btn.clicked.connect(self.load_datasets)
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        subtitle = QLabel("View and manage your uploaded datasets (last 5 are kept)")
        subtitle.setStyleSheet(f"font-size: 14px; color: {LIGHT_COLORS['text_secondary']};")
        layout.addWidget(subtitle)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {LIGHT_COLORS['text_secondary']}; font-size: 13px;")
        layout.addWidget(self.status_label)
        
        # List container
        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setSpacing(15)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.list_widget)
        
        # Empty state
        self.empty_state = QFrame()
        self.empty_state.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT_COLORS['surface']};
                border: 2px dashed {LIGHT_COLORS['border']};
                border-radius: 16px;
                padding: 40px;
            }}
        """)
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_icon = QLabel("📭")
        empty_icon.setStyleSheet("font-size: 48px; border: none;")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_icon)
        
        empty_title = QLabel("No datasets yet")
        empty_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {LIGHT_COLORS['text']}; border: none;")
        empty_title.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_title)
        
        empty_text = QLabel("Upload a CSV file to get started with your analysis")
        empty_text.setStyleSheet(f"font-size: 13px; color: {LIGHT_COLORS['text_secondary']}; border: none;")
        empty_text.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_text)
        
        self.empty_state.setVisible(False)
        layout.addWidget(self.empty_state)
        
        layout.addStretch()
        
        scroll.setWidget(content)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def load_datasets(self):
        """Load datasets from API"""
        self.status_label.setText("Loading...")
        
        try:
            datasets = self.api_service.get_datasets()
            self.datasets = datasets
            
            # Clear existing cards
            while self.list_layout.count():
                item = self.list_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            if not datasets:
                self.empty_state.setVisible(True)
                self.status_label.setText("")
                return
            
            self.empty_state.setVisible(False)
            
            # Create cards
            for dataset in datasets:
                if not isinstance(dataset, dict):
                    continue
                    
                card = DatasetCard(dataset)
                card.view_clicked.connect(self.on_dataset_clicked)
                card.delete_clicked.connect(self.delete_dataset)
                self.list_layout.addWidget(card)
            
            self.status_label.setText(f"Showing {len(datasets)} dataset(s)")
            
        except requests.exceptions.ConnectionError:
            self.status_label.setText("⚠️ Cannot connect to server")
            self.empty_state.setVisible(True)
            
        except Exception as e:
            self.status_label.setText(f"⚠️ Error: {str(e)}")
    
    def on_dataset_clicked(self, dataset_id: int):
        """Handle dataset card click"""
        self.dataset_selected.emit(dataset_id)
    
    def delete_dataset(self, dataset_id: int):
        """Delete a dataset"""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this dataset?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.api_service.delete_dataset(dataset_id)
                self.load_datasets()
                QMessageBox.information(self, "Deleted", "Dataset deleted successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete dataset:\n{str(e)}")
