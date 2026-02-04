"""
Upload Widget for Chemical Equipment Visualizer Desktop Application
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QLineEdit, QFileDialog, QMessageBox,
                              QTableWidget, QTableWidgetItem, QProgressBar,
                              QGroupBox, QHeaderView, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from services.api_service import APIService
import pandas as pd
import os
import requests


class UploadThread(QThread):
    """Thread for uploading file to API"""
    
    upload_complete = pyqtSignal(dict)  # Emits response data
    upload_error = pyqtSignal(str)  # Emits error message
    
    def __init__(self, api_service: APIService, file_path: str):
        super().__init__()
        self.api_service = api_service
        self.file_path = file_path
        
    def run(self):
        """Execute upload in background thread"""
        try:
            response = self.api_service.upload_csv(self.file_path)
            self.upload_complete.emit(response)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', 'Invalid file format')
                    details = error_data.get('details', '')
                    if details:
                        error_msg += f"\n\nDetails: {details}"
                    self.upload_error.emit(error_msg)
                except:
                    self.upload_error.emit("Invalid CSV file format")
            else:
                self.upload_error.emit(f"Server error: {e.response.status_code}")
        except requests.exceptions.ConnectionError:
            self.upload_error.emit("Cannot connect to server. Please check if backend is running.")
        except Exception as e:
            self.upload_error.emit(f"Upload failed: {str(e)}")


class UploadWidget(QWidget):
    """Widget for uploading CSV files"""
    
    upload_successful = pyqtSignal(dict)  # Emits dataset info on successful upload
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.selected_file_path = None
        self.preview_data = None
        self.upload_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Upload CSV File")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Instructions
        instructions = QLabel(
            "Select a CSV file containing chemical equipment data.\n"
            "Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
        )
        instructions.setStyleSheet("color: #666; font-size: 12px; padding: 10px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # File selection group
        file_group = QGroupBox("Select File")
        file_layout = QVBoxLayout()
        
        # File path display and browse button
        file_select_layout = QHBoxLayout()
        
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("No file selected")
        self.file_path_input.setReadOnly(True)
        self.file_path_input.setMinimumHeight(35)
        file_select_layout.addWidget(self.file_path_input, stretch=3)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setMinimumHeight(35)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_file)
        file_select_layout.addWidget(self.browse_btn, stretch=1)
        
        file_layout.addLayout(file_select_layout)
        
        # File info label
        self.file_info_label = QLabel("")
        self.file_info_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        self.file_info_label.hide()
        file_layout.addWidget(self.file_info_label)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Preview group
        preview_group = QGroupBox("Data Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.preview_table.setMaximumHeight(300)
        self.preview_table.hide()
        preview_layout.addWidget(self.preview_table)
        
        self.no_preview_label = QLabel("No file selected for preview")
        self.no_preview_label.setAlignment(Qt.AlignCenter)
        self.no_preview_label.setStyleSheet("color: #999; padding: 50px; font-size: 13px;")
        preview_layout.addWidget(self.no_preview_label)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group, stretch=1)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2e7d32;
                border-radius: 3px;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Message label
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setMinimumHeight(50)
        self.message_label.hide()
        layout.addWidget(self.message_label)
        
        # Upload button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.upload_btn = QPushButton("Upload to Server")
        self.upload_btn.setMinimumSize(180, 45)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
            QPushButton:pressed {
                background-color: #0d3d15;
            }
            QPushButton:disabled {
                background-color: #9e9e9e;
            }
        """)
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if file_path:
            self.selected_file_path = file_path
            self.file_path_input.setText(file_path)
            
            # Show file info
            file_size = os.path.getsize(file_path)
            file_size_kb = file_size / 1024
            self.file_info_label.setText(f"File size: {file_size_kb:.2f} KB")
            self.file_info_label.show()
            
            # Enable upload button
            self.upload_btn.setEnabled(True)
            
            # Load preview
            self.load_preview()
            
    def load_preview(self):
        """Load and display CSV preview"""
        if not self.selected_file_path:
            return
            
        try:
            # Read first 10 rows
            df = pd.read_csv(self.selected_file_path, nrows=10)
            self.preview_data = df
            
            # Display in table
            self.preview_table.clear()
            self.preview_table.setRowCount(len(df))
            self.preview_table.setColumnCount(len(df.columns))
            self.preview_table.setHorizontalHeaderLabels(df.columns.tolist())
            
            for i, row in df.iterrows():
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.preview_table.setItem(i, j, item)
            
            # Show preview table
            self.no_preview_label.hide()
            self.preview_table.show()
            
            # Show success message
            self.show_message(
                f"✓ Preview loaded: {len(df)} rows shown (total may be more)",
                "success"
            )
            
        except Exception as e:
            self.show_message(f"⚠️ Could not load preview: {str(e)}", "error")
            self.preview_table.hide()
            self.no_preview_label.setText(f"Error loading preview:\n{str(e)}")
            self.no_preview_label.show()
            
    def upload_file(self):
        """Upload selected file to API"""
        if not self.selected_file_path:
            self.show_message("⚠️ Please select a file first", "error")
            return
            
        # Confirm upload
        reply = QMessageBox.question(
            self,
            "Confirm Upload",
            f"Upload file: {os.path.basename(self.selected_file_path)}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.No:
            return
            
        # Disable UI during upload
        self.set_uploading(True)
        
        # Start upload thread
        self.upload_thread = UploadThread(self.api_service, self.selected_file_path)
        self.upload_thread.upload_complete.connect(self.on_upload_complete)
        self.upload_thread.upload_error.connect(self.on_upload_error)
        self.upload_thread.start()
        
    def set_uploading(self, uploading: bool):
        """Set uploading state"""
        self.browse_btn.setEnabled(not uploading)
        self.upload_btn.setEnabled(not uploading)
        
        if uploading:
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.progress_bar.show()
            self.upload_btn.setText("Uploading...")
            self.show_message("📤 Uploading file to server...", "info")
        else:
            self.progress_bar.hide()
            self.upload_btn.setText("Upload to Server")
            
    def on_upload_complete(self, response: dict):
        """Handle successful upload"""
        self.set_uploading(False)
        
        # Show success message
        dataset_name = response.get('name', 'Unknown')
        total_records = response.get('total_records', 0)
        
        self.show_message(
            f"✓ Upload successful!\n"
            f"Dataset: {dataset_name}\n"
            f"Records: {total_records}",
            "success"
        )
        
        # Show success dialog
        QMessageBox.information(
            self,
            "Upload Successful",
            f"File uploaded successfully!\n\n"
            f"Dataset: {dataset_name}\n"
            f"Total Records: {total_records}\n\n"
            f"You can view the data in the Dashboard tab."
        )
        
        # Emit signal
        self.upload_successful.emit(response)
        
        # Reset UI
        self.reset()
        
    def on_upload_error(self, error_message: str):
        """Handle upload error"""
        self.set_uploading(False)
        self.show_message(f"❌ Upload failed:\n{error_message}", "error")
        
        # Show error dialog
        QMessageBox.critical(
            self,
            "Upload Failed",
            f"Failed to upload file.\n\n{error_message}"
        )
        
    def show_message(self, message: str, msg_type: str = "info"):
        """Display message to user"""
        self.message_label.setText(message)
        
        if msg_type == "success":
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #2e7d32;
                    background-color: #e8f5e9;
                    padding: 15px;
                    border-radius: 4px;
                    font-size: 13px;
                }
            """)
        elif msg_type == "error":
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #d32f2f;
                    background-color: #ffebee;
                    padding: 15px;
                    border-radius: 4px;
                    font-size: 13px;
                }
            """)
        else:  # info
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #1976d2;
                    background-color: #e3f2fd;
                    padding: 15px;
                    border-radius: 4px;
                    font-size: 13px;
                }
            """)
            
        self.message_label.show()
        
    def reset(self):
        """Reset widget to initial state"""
        self.selected_file_path = None
        self.preview_data = None
        self.file_path_input.clear()
        self.file_info_label.hide()
        self.preview_table.hide()
        self.preview_table.clear()
        self.no_preview_label.setText("No file selected for preview")
        self.no_preview_label.show()
        self.upload_btn.setEnabled(False)
