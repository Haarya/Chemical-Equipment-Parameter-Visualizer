"""
Login Dialog for Chemical Equipment Visualizer Desktop Application
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QMessageBox, QGroupBox,
                              QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from services.api_service import APIService
import requests


class LoginDialog(QDialog):
    """Dialog for user authentication"""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal(str, str)  # token, username
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Login - Reactometrix")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Chemical Equipment Visualizer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Please login to continue")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(subtitle_label)
        
        # Login form group
        form_group = QGroupBox("Login")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(35)
        self.username_input.returnPressed.connect(self.on_login)
        form_layout.addRow("Username:", self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        self.password_input.returnPressed.connect(self.on_login)
        form_layout.addRow("Password:", self.password_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Error message label (hidden by default)
        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("""
            QLabel {
                color: #d32f2f;
                background-color: #ffebee;
                padding: 10px;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Register button
        self.register_btn = QPushButton("Register")
        self.register_btn.setMinimumHeight(40)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        self.register_btn.clicked.connect(self.on_register)
        button_layout.addWidget(self.register_btn)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setStyleSheet("""
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
        self.login_btn.clicked.connect(self.on_login)
        button_layout.addWidget(self.login_btn)
        
        layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Set focus to username field
        self.username_input.setFocus()
        
    def show_error(self, message: str):
        """Display error message"""
        self.error_label.setText(f"⚠️ {message}")
        self.error_label.show()
        
    def hide_error(self):
        """Hide error message"""
        self.error_label.hide()
        
    def set_loading(self, loading: bool):
        """Set loading state for buttons"""
        self.login_btn.setEnabled(not loading)
        self.register_btn.setEnabled(not loading)
        self.username_input.setEnabled(not loading)
        self.password_input.setEnabled(not loading)
        
        if loading:
            self.login_btn.setText("Logging in...")
        else:
            self.login_btn.setText("Login")
            
    def on_login(self):
        """Handle login button click"""
        self.hide_error()
        
        # Validate inputs
        username = self.username_input.text().strip()
        password = self.password_input.text()  # Don't strip password - keep exact input
        
        if not username:
            self.show_error("Please enter your username")
            self.username_input.setFocus()
            return
            
        if not password:
            self.show_error("Please enter your password")
            self.password_input.setFocus()
            return
        
        # Set loading state
        self.set_loading(True)
        
        try:
            # Call API
            response = self.api_service.login(username, password)
            
            # Success
            token = response.get('token')
            if token:
                self.login_successful.emit(token, username)
                self.accept()
            else:
                self.show_error("Invalid response from server")
                self.set_loading(False)
                
        except requests.exceptions.HTTPError as e:
            # HTTP error
            if e.response.status_code == 400:
                self.show_error("Invalid username or password")
            elif e.response.status_code == 401:
                self.show_error("Invalid credentials")
            else:
                self.show_error(f"Server error: {e.response.status_code}")
            self.set_loading(False)
            
        except requests.exceptions.ConnectionError:
            self.show_error("Cannot connect to server. Please check if backend is running.")
            self.set_loading(False)
            
        except Exception as e:
            self.show_error(f"Login failed: {str(e)}")
            self.set_loading(False)
            
    def on_register(self):
        """Handle register button click"""
        from ui.register_dialog import RegisterDialog
        
        # Close this dialog
        self.hide()
        
        # Open register dialog
        register_dialog = RegisterDialog(self.api_service, self.parent())
        register_dialog.registration_successful.connect(self.on_registration_successful)
        
        if register_dialog.exec_() == QDialog.Rejected:
            # User cancelled registration, show login dialog again
            self.show()
            
    def on_registration_successful(self, token: str, username: str):
        """Handle successful registration"""
        # Auto-login after registration
        self.login_successful.emit(token, username)
        self.accept()
