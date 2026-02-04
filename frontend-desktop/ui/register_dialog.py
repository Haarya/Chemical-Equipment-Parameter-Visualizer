"""
Registration Dialog for Chemical Equipment Visualizer Desktop Application
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QMessageBox, QGroupBox,
                              QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from services.api_service import APIService
import requests
import re


class RegisterDialog(QDialog):
    """Dialog for user registration"""
    
    # Signal emitted when registration is successful
    registration_successful = pyqtSignal(str, str)  # token, username
    
    def __init__(self, api_service: APIService, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Register - Reactometrix")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setMinimumHeight(400)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Create New Account")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Fill in the details to register")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(subtitle_label)
        
        # Registration form group
        form_group = QGroupBox("Registration Details")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setMinimumHeight(35)
        form_layout.addRow("Username:", self.username_input)
        
        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        self.email_input.setMinimumHeight(35)
        form_layout.addRow("Email:", self.email_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Choose a strong password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        form_layout.addRow("Password:", self.password_input)
        
        # Confirm password field
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Re-enter your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumHeight(35)
        self.confirm_password_input.returnPressed.connect(self.on_register)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
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
        
        # Success message label (hidden by default)
        self.success_label = QLabel()
        self.success_label.setAlignment(Qt.AlignCenter)
        self.success_label.setStyleSheet("""
            QLabel {
                color: #2e7d32;
                background-color: #e8f5e9;
                padding: 10px;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        self.success_label.setWordWrap(True)
        self.success_label.hide()
        layout.addWidget(self.success_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setStyleSheet("""
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
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        # Register button
        self.register_btn = QPushButton("Register")
        self.register_btn.setMinimumHeight(40)
        self.register_btn.setStyleSheet("""
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
        self.register_btn.clicked.connect(self.on_register)
        button_layout.addWidget(self.register_btn)
        
        layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Set focus to username field
        self.username_input.setFocus()
        
    def show_error(self, message: str):
        """Display error message"""
        self.success_label.hide()
        self.error_label.setText(f"⚠️ {message}")
        self.error_label.show()
        
    def show_success(self, message: str):
        """Display success message"""
        self.error_label.hide()
        self.success_label.setText(f"✓ {message}")
        self.success_label.show()
        
    def hide_messages(self):
        """Hide all messages"""
        self.error_label.hide()
        self.success_label.hide()
        
    def set_loading(self, loading: bool):
        """Set loading state for buttons"""
        self.register_btn.setEnabled(not loading)
        self.cancel_btn.setEnabled(not loading)
        self.username_input.setEnabled(not loading)
        self.email_input.setEnabled(not loading)
        self.password_input.setEnabled(not loading)
        self.confirm_password_input.setEnabled(not loading)
        
        if loading:
            self.register_btn.setText("Registering...")
        else:
            self.register_btn.setText("Register")
            
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def validate_inputs(self) -> tuple[bool, str]:
        """
        Validate all input fields
        Returns: (is_valid, error_message)
        """
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Username validation
        if not username:
            return False, "Username is required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if not username.isalnum() and '_' not in username:
            return False, "Username can only contain letters, numbers, and underscores"
            
        # Email validation
        if not email:
            return False, "Email is required"
        if not self.validate_email(email):
            return False, "Please enter a valid email address"
            
        # Password validation
        if not password:
            return False, "Password is required"
        if len(password) < 3:
            return False, "Password must be at least 3 characters long"
            
        # Confirm password validation
        if password != confirm_password:
            return False, "Passwords do not match"
            
        return True, ""
        
    def on_register(self):
        """Handle register button click"""
        self.hide_messages()
        
        # Validate inputs
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            self.show_error(error_message)
            return
        
        # Get input values
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        # Set loading state
        self.set_loading(True)
        
        try:
            # Call API
            response = self.api_service.register(username, email, password)
            
            # Success
            token = response.get('token')
            if token:
                self.show_success("Registration successful! Logging you in...")
                self.registration_successful.emit(token, username)
                # Close dialog after a brief delay to show success message
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(1000, self.accept)
            else:
                self.show_error("Invalid response from server")
                self.set_loading(False)
                
        except requests.exceptions.HTTPError as e:
            # HTTP error
            if e.response.status_code == 400:
                try:
                    error_data = e.response.json()
                    # Extract error messages from response
                    if isinstance(error_data, dict):
                        error_messages = []
                        for field, messages in error_data.items():
                            if isinstance(messages, list):
                                error_messages.extend(messages)
                            else:
                                error_messages.append(str(messages))
                        error_text = " ".join(error_messages)
                    else:
                        error_text = str(error_data)
                    self.show_error(error_text)
                except:
                    self.show_error("Registration failed. Username or email may already exist.")
            else:
                self.show_error(f"Server error: {e.response.status_code}")
            self.set_loading(False)
            
        except requests.exceptions.ConnectionError:
            self.show_error("Cannot connect to server. Please check if backend is running.")
            self.set_loading(False)
            
        except Exception as e:
            self.show_error(f"Registration failed: {str(e)}")
            self.set_loading(False)
