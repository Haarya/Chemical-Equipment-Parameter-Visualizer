"""
ChemViz Pro - Modern Upload Widget
Clean, card-based file upload interface
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QFileDialog, QTableWidget, QTableWidgetItem, QProgressBar,
    QMessageBox, QScrollArea, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

from ui.styles import LIGHT_COLORS, DARK_COLORS
from services.api_service import APIService
import pandas as pd


class UploadThread(QThread):
    """Background thread for file upload"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_service, file_path):
        super().__init__()
        self.api_service = api_service
        self.file_path = file_path
    
    def run(self):
        try:
            result = self.api_service.upload_csv(self.file_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class DropZone(QFrame):
    """Drag and drop zone for file upload"""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(200)
        self.setMaximumHeight(250)
        self.setup_style()
        self.init_ui()
        
    def setup_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT_COLORS['surface']};
                border: 2px dashed {LIGHT_COLORS['border']};
                border-radius: 12px;
            }}
            QFrame:hover {{
                border-color: {LIGHT_COLORS['primary']};
                background-color: #F0F9F4;
            }}
        """)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Icon
        icon = QLabel("📁")
        icon.setStyleSheet("font-size: 40px; border: none; background: transparent;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)
        
        # Title
        title = QLabel("Drop your CSV file here")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {LIGHT_COLORS['text']};
            border: none;
            background: transparent;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("or click below to browse")
        subtitle.setStyleSheet(f"""
            font-size: 12px;
            color: {LIGHT_COLORS['text_secondary']};
            border: none;
            background: transparent;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Browse button
        browse_btn = QPushButton("Browse Files")
        browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_COLORS['primary_hover']};
            }}
        """)
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_files)
        layout.addWidget(browse_btn, 0, Qt.AlignCenter)
    
    def browse_files(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if filename:
            self.file_dropped.emit(filename)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: #E8F5E9;
                    border: 2px dashed {LIGHT_COLORS['primary']};
                    border-radius: 12px;
                }}
            """)
    
    def dragLeaveEvent(self, event):
        self.setup_style()
    
    def dropEvent(self, event: QDropEvent):
        self.setup_style()
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.csv'):
                self.file_dropped.emit(file_path)
                return
        QMessageBox.warning(self, "Invalid File", "Please drop a CSV file.")


class ModernUploadWidget(QWidget):
    """Modern file upload widget with preview"""
    
    upload_successful = pyqtSignal(int)  # Emits dataset ID
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.selected_file = None
        self.upload_thread = None
        self.init_ui()
        
    def init_ui(self):
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        # Content
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        title = QLabel("Upload Dataset")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {LIGHT_COLORS['text']};
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("Upload a CSV file containing chemical equipment data for analysis")
        subtitle.setStyleSheet(f"font-size: 14px; color: {LIGHT_COLORS['text_secondary']};")
        layout.addWidget(subtitle)
        
        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.file_dropped.connect(self.on_file_selected)
        layout.addWidget(self.drop_zone)
        
        # Selected file card
        self.file_card = QFrame()
        self.file_card.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT_COLORS['surface']};
                border: 1px solid {LIGHT_COLORS['border_light']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        self.file_card.setVisible(False)
        
        file_layout = QVBoxLayout(self.file_card)
        
        # File info row
        file_info_layout = QHBoxLayout()
        
        self.file_icon = QLabel("📄")
        self.file_icon.setStyleSheet("font-size: 32px; border: none;")
        file_info_layout.addWidget(self.file_icon)
        
        file_details = QVBoxLayout()
        self.file_name_label = QLabel("No file selected")
        self.file_name_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {LIGHT_COLORS['text']}; border: none;")
        file_details.addWidget(self.file_name_label)
        
        self.file_size_label = QLabel("")
        self.file_size_label.setStyleSheet(f"font-size: 12px; color: {LIGHT_COLORS['text_secondary']}; border: none;")
        file_details.addWidget(self.file_size_label)
        
        file_info_layout.addLayout(file_details)
        file_info_layout.addStretch()
        
        # Clear button
        clear_btn = QPushButton("✕")
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {LIGHT_COLORS['border']};
                border-radius: 15px;
                color: {LIGHT_COLORS['text_secondary']};
                font-size: 14px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_COLORS['accent_red']};
                color: white;
                border-color: {LIGHT_COLORS['accent_red']};
            }}
        """)
        clear_btn.setFixedSize(30, 30)
        clear_btn.clicked.connect(self.clear_selection)
        file_info_layout.addWidget(clear_btn)
        
        file_layout.addLayout(file_info_layout)
        
        layout.addWidget(self.file_card)
        
        # Preview section
        self.preview_card = QFrame()
        self.preview_card.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT_COLORS['surface']};
                border: 1px solid {LIGHT_COLORS['border_light']};
                border-radius: 12px;
            }}
        """)
        self.preview_card.setVisible(False)
        
        preview_layout = QVBoxLayout(self.preview_card)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        
        preview_title = QLabel("📊 Data Preview")
        preview_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {LIGHT_COLORS['text']};
            border: none;
            padding-bottom: 10px;
        """)
        preview_layout.addWidget(preview_title)
        
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.setMinimumHeight(250)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        preview_layout.addWidget(self.preview_table)
        
        self.preview_info = QLabel("")
        self.preview_info.setStyleSheet(f"color: {LIGHT_COLORS['text_secondary']}; font-size: 12px; border: none;")
        preview_layout.addWidget(self.preview_info)
        
        layout.addWidget(self.preview_card)
        
        # Upload button and progress
        action_layout = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)  # Indeterminate
        action_layout.addWidget(self.progress_bar)
        
        self.upload_btn = QPushButton("Upload Dataset")
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 32px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_COLORS['primary_hover']};
            }}
            QPushButton:disabled {{
                background-color: {LIGHT_COLORS['border']};
            }}
        """)
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        action_layout.addWidget(self.upload_btn)
        
        layout.addLayout(action_layout)
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"font-size: 14px; padding: 10px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        scroll.setWidget(content)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def on_file_selected(self, file_path: str):
        """Handle file selection"""
        self.selected_file = file_path
        
        import os
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Update file card
        self.file_name_label.setText(file_name)
        self.file_size_label.setText(f"{file_size / 1024:.1f} KB")
        self.file_card.setVisible(True)
        
        # Load preview
        self.load_preview(file_path)
        
        # Enable upload
        self.upload_btn.setEnabled(True)
        self.status_label.setText("")
    
    def load_preview(self, file_path: str):
        """Load file preview"""
        try:
            df = pd.read_csv(file_path)
            
            # Show first 10 rows
            preview_df = df.head(10)
            
            self.preview_table.setRowCount(len(preview_df))
            self.preview_table.setColumnCount(len(preview_df.columns))
            self.preview_table.setHorizontalHeaderLabels(list(preview_df.columns))
            
            for row in range(len(preview_df)):
                for col in range(len(preview_df.columns)):
                    value = str(preview_df.iloc[row, col])
                    item = QTableWidgetItem(value)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.preview_table.setItem(row, col, item)
            
            self.preview_info.setText(f"Showing {len(preview_df)} of {len(df)} rows | {len(df.columns)} columns")
            self.preview_card.setVisible(True)
            
        except Exception as e:
            self.preview_info.setText(f"Error loading preview: {str(e)}")
            self.preview_card.setVisible(True)
    
    def clear_selection(self):
        """Clear selected file"""
        self.selected_file = None
        self.file_card.setVisible(False)
        self.preview_card.setVisible(False)
        self.upload_btn.setEnabled(False)
        self.status_label.setText("")
    
    def upload_file(self):
        """Upload the selected file"""
        if not self.selected_file:
            return
        
        self.upload_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Uploading...")
        self.status_label.setStyleSheet(f"color: {LIGHT_COLORS['accent_blue']}; font-size: 14px;")
        
        self.upload_thread = UploadThread(self.api_service, self.selected_file)
        self.upload_thread.finished.connect(self.on_upload_finished)
        self.upload_thread.error.connect(self.on_upload_error)
        self.upload_thread.start()
    
    def on_upload_finished(self, result: dict):
        """Handle successful upload"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("✅ Upload successful!")
        self.status_label.setStyleSheet(f"color: {LIGHT_COLORS['primary']}; font-size: 14px; font-weight: bold;")
        
        dataset_id = result.get('dataset_id') or result.get('id')
        if dataset_id:
            self.upload_successful.emit(dataset_id)
        
        # Clear for next upload
        self.clear_selection()
    
    def on_upload_error(self, error: str):
        """Handle upload error"""
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        self.status_label.setText(f"❌ Upload failed: {error}")
        self.status_label.setStyleSheet(f"color: {LIGHT_COLORS['accent_red']}; font-size: 14px;")
