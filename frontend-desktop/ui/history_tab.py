"""
History Tab for Chemical Equipment Visualizer Desktop Application
Displays last 5 uploaded datasets
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QListWidget, QListWidgetItem, QLabel, QFrame,
                              QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont
from services.api_service import APIService
import requests
from datetime import datetime


class DatasetListItem(QWidget):
    """Custom widget for dataset list item"""
    
    delete_clicked = pyqtSignal(int)  # Emits dataset ID
    
    def __init__(self, dataset_info: dict, parent=None):
        super().__init__(parent)
        self.dataset_info = dataset_info
        self.dataset_id = dataset_info.get('id')
        self.init_ui()
        
    def init_ui(self):
        """Initialize the list item UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px;
            }
            QWidget:hover {
                background-color: #f5f5f5;
                border-color: #3b82f6;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Top row: Name and delete button
        top_layout = QHBoxLayout()
        
        name = self.dataset_info.get('name', 'Unknown')
        name_label = QLabel(name)
        name_font = QFont()
        name_font.setPointSize(11)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setStyleSheet("border: none; color: #1976d2;")
        top_layout.addWidget(name_label, stretch=1)
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
            QPushButton:pressed {
                background-color: #b91c1c;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.dataset_id))
        delete_btn.setToolTip("Delete this dataset")
        top_layout.addWidget(delete_btn)
        
        layout.addLayout(top_layout)
        
        # Info row: Records count and upload date
        info_layout = QHBoxLayout()
        
        # Records count
        total_records = self.dataset_info.get('total_records', 0)
        records_label = QLabel(f"📊 {total_records} records")
        records_label.setStyleSheet("border: none; color: #666; font-size: 10px;")
        info_layout.addWidget(records_label)
        
        info_layout.addStretch()
        
        # Upload date
        uploaded_at = self.dataset_info.get('uploaded_at', '')
        if uploaded_at:
            try:
                dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%b %d, %Y')
                date_label = QLabel(f"📅 {formatted_date}")
            except:
                date_label = QLabel(f"📅 {uploaded_at}")
        else:
            date_label = QLabel("📅 Unknown")
            
        date_label.setStyleSheet("border: none; color: #666; font-size: 10px;")
        info_layout.addWidget(date_label)
        
        layout.addLayout(info_layout)
        
        self.setLayout(layout)


class HistoryTab(QWidget):
    """Tab for displaying dataset history"""
    
    dataset_selected = pyqtSignal(int)  # Emits dataset ID when selected
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.datasets = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Dataset History")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setMinimumHeight(35)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #9e9e9e;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_datasets)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Info label
        info_label = QLabel("Last 5 uploaded datasets. Double-click to view details.")
        info_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        layout.addWidget(info_label)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(10)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px;
            }
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: transparent;
            }
        """)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget, stretch=1)
        
        # Status label
        self.status_label = QLabel("Click refresh to load datasets")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                padding: 20px;
                background-color: #f5f5f5;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def load_datasets(self):
        """Load datasets from API"""
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Loading...")
        self.status_label.setText("Loading datasets...")
        
        try:
            # Fetch datasets from API
            datasets = self.api_service.get_datasets()
            self.datasets = datasets
            
            # Clear list
            self.list_widget.clear()
            
            if not datasets or len(datasets) == 0:
                self.status_label.setText("No datasets found. Upload a CSV file to get started.")
                self.refresh_btn.setEnabled(True)
                self.refresh_btn.setText("🔄 Refresh")
                return
            
            # Add datasets to list
            for dataset in datasets:
                # Create custom widget
                item_widget = DatasetListItem(dataset)
                item_widget.delete_clicked.connect(self.delete_dataset)
                
                # Create list item
                list_item = QListWidgetItem(self.list_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                list_item.setData(Qt.UserRole, dataset.get('id'))
                
                # Add to list
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)
            
            self.status_label.setText(f"Loaded {len(datasets)} dataset(s)")
            
        except requests.exceptions.ConnectionError:
            self.status_label.setText("⚠️ Cannot connect to server. Please check if backend is running.")
            QMessageBox.warning(
                self,
                "Connection Error",
                "Cannot connect to backend server.\nPlease make sure the Django backend is running."
            )
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                self.status_label.setText("⚠️ Please login to view datasets")
            else:
                self.status_label.setText(f"⚠️ Error: {e.response.status_code}")
                
        except Exception as e:
            self.status_label.setText(f"⚠️ Error loading datasets: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load datasets:\n{str(e)}"
            )
            
        finally:
            self.refresh_btn.setEnabled(True)
            self.refresh_btn.setText("🔄 Refresh")
            
    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on dataset item"""
        dataset_id = item.data(Qt.UserRole)
        if dataset_id:
            self.dataset_selected.emit(dataset_id)
            
    def delete_dataset(self, dataset_id: int):
        """Delete a dataset"""
        # Find dataset name
        dataset = next((ds for ds in self.datasets if ds.get('id') == dataset_id), None)
        dataset_name = dataset.get('name', 'Unknown') if dataset else 'Unknown'
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this dataset?\n\n{dataset_name}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
            
        try:
            # Delete via API
            self.api_service.delete_dataset(dataset_id)
            
            # Show success message
            self.status_label.setText(f"✓ Deleted: {dataset_name}")
            
            # Reload list
            self.load_datasets()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                QMessageBox.warning(self, "Not Found", "Dataset not found.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete dataset:\n{e.response.status_code}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete dataset:\n{str(e)}")
            
    def get_selected_dataset_id(self) -> int:
        """Get currently selected dataset ID"""
        current_item = self.list_widget.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
