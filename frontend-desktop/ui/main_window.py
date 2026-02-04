"""
Main Window for Chemical Equipment Visualizer Desktop Application
"""

from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QAction, QMessageBox,
                              QStatusBar, QMenuBar, QWidget, QVBoxLayout, 
                              QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from services.api_service import APIService
from ui.login_dialog import LoginDialog
from ui.upload_widget import UploadWidget
from ui.dashboard_tab import DashboardTab
from ui.history_tab import HistoryTab


class MainWindow(QMainWindow):
    """Main application window with tabs and menu"""
    
    def __init__(self):
        super().__init__()
        self.auth_token = None
        self.current_user = None
        self.api_service = APIService()
        self.init_ui()
        
        # Show login dialog on startup
        self.show_login_dialog()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Chemical Equipment Parameter Visualizer - Reactometrix")
        self.setMinimumSize(QSize(1200, 800))
        
        # Set window icon (will use default for now)
        # self.setWindowIcon(QIcon('icon.png'))
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        self.setCentralWidget(self.tabs)
        
        # Create tabs (placeholder widgets for now)
        self.create_tabs()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Please login to continue")
        
    def create_tabs(self):
        """Create and add tabs to the tab widget"""
        # Dashboard Tab with DashboardTab
        self.dashboard_tab = DashboardTab(self.api_service, self)
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        
        # Upload Tab with UploadWidget
        self.upload_widget = UploadWidget(self.api_service, self)
        self.upload_widget.upload_successful.connect(self.on_upload_successful)
        self.tabs.addTab(self.upload_widget, "📤 Upload")
        
        # History Tab with HistoryTab
        self.history_tab = HistoryTab(self.api_service, self)
        self.history_tab.dataset_selected.connect(self.on_dataset_selected)
        self.tabs.addTab(self.history_tab, "📋 History")
        
        # Set default tab
        self.tabs.setCurrentIndex(0)
        
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        upload_action = QAction("&Upload CSV", self)
        upload_action.setShortcut("Ctrl+O")
        upload_action.triggered.connect(self.on_upload_csv)
        file_menu.addAction(upload_action)
        
        download_action = QAction("&Download Report", self)
        download_action.setShortcut("Ctrl+D")
        download_action.triggered.connect(self.on_download_report)
        file_menu.addAction(download_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Account menu
        account_menu = menubar.addMenu("&Account")
        
        login_action = QAction("&Login", self)
        login_action.triggered.connect(self.on_login)
        account_menu.addAction(login_action)
        
        logout_action = QAction("L&ogout", self)
        logout_action.triggered.connect(self.on_logout)
        account_menu.addAction(logout_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
        
    def on_upload_csv(self):
        """Handle upload CSV action"""
        self.status_bar.showMessage("Upload CSV selected")
        # Will be implemented later
        
    def on_download_report(self):
        """Handle download report a from menu"""
        # Switch to upload tab
        self.tabs.setCurrentIndex(1)  # Upload tab is at index 1
        self.status_bar.showMessage("Select a CSV file to upload")
        
    def on_upload_successful(self, dataset_info: dict):
        """Handle successful upload"""
        dataset_name = dataset_info.get('name', 'Unknown')
        self.status_bar.showMessage(f"Successfully uploaded: {dataset_name}")
        
        # Refresh dashboard datasets list
        self.dashboard_tab.load_datasets_list()
        
        # Switch to dashboard tab
        self.tabs.setCurrentWidget(self.dashboard_tab)
        
        # Refresh history tab
        self.history_tab.load_datasets()
        
    def on_dataset_selected(self, dataset_id: int):
        """Handle dataset selection from history tab"""
        # Load dataset in dashboard
        self.dashboard_tab.load_dataset(dataset_id)
        
        # Switch to dashboard tab
        self.tabs.setCurrentWidget(self.dashboard_tab)
        
        # Update status bar
        self.status_bar.showMessage(f"Loaded dataset ID: {dataset_id}")
        
    def show_login_dialog(self):
        """Show login dialog"""
        login_dialog = LoginDialog(self.api_service, self)
        login_dialog.login_successful.connect(self.on_login_successful)
        login_dialog.exec_()
        
    def on_login(self):
        """Handle login action from menu"""
        if self.auth_token:
            reply = QMessageBox.question(
                self, 
                "Already Logged In",
                f"You are already logged in as {self.current_user}.\nDo you want to login as a different user?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
            # Logout first
            self.on_logout()
        
        self.show_login_dialog()
        
    def on_login_successful(self, token: str, username: str):
        """Handle successful login"""
        self.auth_token = token
        self.current_user = username
        self.api_service.set_token(token)
        
        # Update status bar
        self.status_bar.showMessage(f"Logged in as {username}")
        
        # Load history tab datasets
        self.history_tab.load_datasets()
        
        # Refresh dashboard datasets
        self.dashboard_tab.refresh_datasets()
        
        # Show success message
        QMessageBox.information(
            self, 
            "Login Successful", 
            f"Welcome, {username}!\n\nYou can now upload datasets and view analytics."
        )
        
        # Load datasets list for dashboard
        self.dashboard_tab.load_datasets_list()
        
        # TODO: Refresh history tab when implemented
        # self.refresh_history()
        
    def on_logout(self):
        """Handle logout action"""
        if not self.auth_token:
            QMessageBox.information(self, "Not Logged In", "You are not currently logged in.")
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            f"Are you sure you want to logout, {self.current_user}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Call logout API
                self.api_service.logout()
            except:
                pass  # Ignore errors during logout
            
            # Clear local state
            self.auth_token = None
            self.current_user = None
            self.api_service.clear_token()
            
            # Update status bar
            self.status_bar.showMessage("Logged out - Please login to continue")
            
            # Show message
            QMessageBox.information(self, "Logout", "You have been logged out successfully.")
            
            # Clear dashboard content
            self.dashboard_tab.clear_dashboard()
            
            # Clear history tab
            self.history_tab.list_widget.clear()
            self.history_tab.status_label.setText("Click refresh to load datasets")
        
    def on_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Chemical Equipment Parameter Visualizer</h2>
        <p>Version 1.0</p>
        <p>A desktop application for visualizing chemical equipment data.</p>
        <p><b>Tech Stack:</b> PyQt5, Matplotlib, Pandas</p>
        <p><b>Backend:</b> Django REST API</p>
        <p>&copy; 2026 FOSSEE Project</p>
        """
        QMessageBox.about(self, "About", about_text)
