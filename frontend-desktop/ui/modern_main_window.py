"""
ChemViz Pro - Modern Lab OS Main Window
A frameless, modern desktop application with custom title bar and sidebar navigation
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QStackedWidget, QSizePolicy, QApplication,
    QMessageBox, QGraphicsDropShadowEffect, QScrollArea
)
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon

from ui.styles import get_stylesheet, LIGHT_COLORS
from ui.modern_dashboard import ModernDashboard
from ui.modern_upload import ModernUploadWidget
from ui.modern_history import ModernHistoryTab
from ui.login_dialog import LoginDialog
from ui.register_dialog import RegisterDialog
from services.api_service import APIService


class TitleBar(QWidget):
    """Custom frameless title bar with window controls"""
    
    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    close_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedHeight(45)
        self._drag_pos = None
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # App icon/logo area
        logo_label = QLabel("  🧪")
        logo_label.setStyleSheet("font-size: 20px; padding-left: 10px;")
        layout.addWidget(logo_label)
        
        # Title
        title = QLabel("ChemViz Pro")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)
        
        # Spacer
        layout.addStretch()
        
        # Window controls
        # Minimize button
        min_btn = QPushButton("─")
        min_btn.setObjectName("MinimizeButton")
        min_btn.setFixedSize(45, 45)
        min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A7C5D;
            }
        """)
        min_btn.clicked.connect(self.minimize_clicked.emit)
        layout.addWidget(min_btn)
        
        # Maximize button
        max_btn = QPushButton("□")
        max_btn.setObjectName("MaximizeButton")
        max_btn.setFixedSize(45, 45)
        max_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A7C5D;
            }
        """)
        max_btn.clicked.connect(self.maximize_clicked.emit)
        layout.addWidget(max_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("CloseButton")
        close_btn.setFixedSize(45, 45)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #EF4444;
            }
        """)
        close_btn.clicked.connect(self.close_clicked.emit)
        layout.addWidget(close_btn)
    
    # ============================================
    # FRAMELESS WINDOW DRAG LOGIC
    # ============================================
    def mousePressEvent(self, event):
        """Start dragging the window"""
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Drag the window"""
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.window().move(event.globalPos() - self._drag_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Stop dragging"""
        self._drag_pos = None
    
    def mouseDoubleClickEvent(self, event):
        """Double-click to maximize/restore"""
        if event.button() == Qt.LeftButton:
            self.maximize_clicked.emit()


class NavButton(QPushButton):
    """Custom navigation button for sidebar"""
    
    def __init__(self, icon_text: str, label: str, parent=None):
        super().__init__(parent)
        self.setObjectName("NavButton")
        self.setText(f"  {icon_text}   {label}")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(45)


class Sidebar(QWidget):
    """Modern sidebar navigation"""
    
    navigation_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)
        self.buttons = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # App branding
        brand_frame = QFrame()
        brand_layout = QVBoxLayout(brand_frame)
        brand_layout.setContentsMargins(20, 25, 20, 25)
        
        brand_title = QLabel("ChemViz Pro")
        brand_title.setStyleSheet(f"""
            font-size: 22px;
            font-weight: bold;
            color: {LIGHT_COLORS['primary']};
        """)
        brand_layout.addWidget(brand_title)
        
        brand_subtitle = QLabel("Chemical Equipment Visualizer")
        brand_subtitle.setStyleSheet(f"""
            font-size: 11px;
            color: {LIGHT_COLORS['text_secondary']};
        """)
        brand_layout.addWidget(brand_subtitle)
        
        layout.addWidget(brand_frame)
        
        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {LIGHT_COLORS['border_light']};")
        layout.addWidget(separator)
        
        # Navigation section title
        nav_title = QLabel("NAVIGATION")
        nav_title.setObjectName("SidebarTitle")
        layout.addWidget(nav_title)
        
        # Navigation buttons
        nav_items = [
            ("📊", "Dashboard"),
            ("📤", "Upload Data"),
            ("📋", "History"),
        ]
        
        for i, (icon, label) in enumerate(nav_items):
            btn = NavButton(icon, label)
            btn.clicked.connect(lambda checked, idx=i: self.on_nav_clicked(idx))
            self.buttons.append(btn)
            layout.addWidget(btn)
        
        # Set first button as active
        self.buttons[0].setChecked(True)
        
        layout.addStretch()
        
        # User section at bottom
        user_frame = QFrame()
        user_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {LIGHT_COLORS['hover_bg']};
                border-top: 1px solid {LIGHT_COLORS['border_light']};
            }}
        """)
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(15, 15, 15, 15)
        
        self.user_label = QLabel("Not logged in")
        self.user_label.setStyleSheet(f"""
            font-size: 12px;
            color: {LIGHT_COLORS['text_secondary']};
        """)
        user_layout.addWidget(self.user_label)
        
        self.login_btn = QPushButton("🔐 Login")
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {LIGHT_COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {LIGHT_COLORS['primary_hover']};
            }}
        """)
        user_layout.addWidget(self.login_btn)
        
        layout.addWidget(user_frame)
    
    def on_nav_clicked(self, index: int):
        """Handle navigation button click"""
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)
        self.navigation_changed.emit(index)
    
    def set_user(self, username: str):
        """Update user display"""
        if username:
            self.user_label.setText(f"👤 {username}")
            self.login_btn.setText("🚪 Logout")
        else:
            self.user_label.setText("Not logged in")
            self.login_btn.setText("🔐 Login")


class ModernMainWindow(QMainWindow):
    """
    Modern frameless main window with custom title bar and sidebar
    
    FRAMELESS WINDOW IMPLEMENTATION:
    - Qt.FramelessWindowHint removes the standard window decorations
    - Custom TitleBar handles window dragging via mouse events
    - Resize handles can be added at window edges (not implemented here for simplicity)
    """
    
    def __init__(self):
        super().__init__()
        
        # Remove standard window frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        # API and auth state
        self.api_service = APIService()
        self.auth_token = None
        self.current_user = None
        
        # Window state
        self._is_maximized = False
        self._normal_geometry = None
        
        self.init_ui()
        self.apply_styles()
        
        # Show login dialog on startup
        self.show_login_dialog()
    
    def init_ui(self):
        """Initialize the modern UI"""
        self.setWindowTitle("ChemViz Pro")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Central widget
        central = QWidget()
        central.setObjectName("MainWindow")
        self.setCentralWidget(central)
        
        # Main layout (vertical: title bar + content)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        self.title_bar = TitleBar()
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self.toggle_maximize)
        self.title_bar.close_clicked.connect(self.close)
        main_layout.addWidget(self.title_bar)
        
        # Content area (horizontal: sidebar + main content)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_changed.connect(self.on_navigation_changed)
        self.sidebar.login_btn.clicked.connect(self.on_login_logout_clicked)
        content_layout.addWidget(self.sidebar)
        
        # Main content area with stacked widget
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"background-color: {LIGHT_COLORS['background']};")
        
        # Create pages
        self.dashboard_page = ModernDashboard(self.api_service)
        self.upload_page = ModernUploadWidget(self.api_service)
        self.history_page = ModernHistoryTab(self.api_service)
        
        # Connect signals
        self.upload_page.upload_successful.connect(self.on_upload_successful)
        self.history_page.dataset_selected.connect(self.on_dataset_selected)
        
        # Add pages to stack
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.upload_page)
        self.content_stack.addWidget(self.history_page)
        
        content_layout.addWidget(self.content_stack)
        
        main_layout.addWidget(content_widget)
    
    def apply_styles(self):
        """Apply the stylesheet"""
        stylesheet = get_stylesheet('light')
        self.setStyleSheet(stylesheet)
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self._is_maximized:
            if self._normal_geometry:
                self.setGeometry(self._normal_geometry)
            self._is_maximized = False
        else:
            self._normal_geometry = self.geometry()
            screen = QApplication.primaryScreen().availableGeometry()
            self.setGeometry(screen)
            self._is_maximized = True
    
    def on_navigation_changed(self, index: int):
        """Handle sidebar navigation"""
        self.content_stack.setCurrentIndex(index)
    
    def on_login_logout_clicked(self):
        """Handle login/logout button click"""
        if self.auth_token:
            self.logout()
        else:
            self.show_login_dialog()
    
    def show_login_dialog(self):
        """Show the login dialog"""
        dialog = LoginDialog(self.api_service, self)
        dialog.login_successful.connect(self.on_login_successful)
        
        # Check if register button exists
        if hasattr(dialog, 'register_btn'):
            dialog.register_btn.clicked.connect(lambda: self.show_register_dialog(dialog))
        
        dialog.exec_()
    
    def show_register_dialog(self, login_dialog=None):
        """Show registration dialog"""
        if login_dialog:
            login_dialog.close()
        
        dialog = RegisterDialog(self.api_service, self)
        dialog.register_successful.connect(self.on_login_successful)
        dialog.exec_()
    
    def on_login_successful(self, token: str, username: str):
        """Handle successful login"""
        self.auth_token = token
        self.current_user = username
        self.api_service.set_token(token)
        
        # Update sidebar
        self.sidebar.set_user(username)
        
        # Load data
        self.dashboard_page.load_datasets_list()
        self.history_page.load_datasets()
        
        QMessageBox.information(
            self,
            "Welcome",
            f"Welcome back, {username}! 🎉\n\nYou can now upload datasets and view analytics."
        )
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.api_service.logout()
            except:
                pass
            
            self.auth_token = None
            self.current_user = None
            self.api_service.clear_token()
            
            # Update sidebar
            self.sidebar.set_user(None)
            
            # Clear dashboard
            self.dashboard_page.clear_dashboard()
            
            # Clear history (clear list_layout items)
            while self.history_page.list_layout.count():
                item = self.history_page.list_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Show login dialog
            self.show_login_dialog()
    
    def on_upload_successful(self, dataset_id: int):
        """Handle successful upload"""
        # Refresh data
        self.dashboard_page.load_datasets_list()
        self.history_page.load_datasets()
        
        # Load new dataset in dashboard
        self.dashboard_page.load_dataset(dataset_id)
        
        # Switch to dashboard
        self.sidebar.on_nav_clicked(0)
        self.content_stack.setCurrentIndex(0)
    
    def on_dataset_selected(self, dataset_id: int):
        """Handle dataset selection from history"""
        self.dashboard_page.load_dataset(dataset_id)
        self.sidebar.on_nav_clicked(0)
        self.content_stack.setCurrentIndex(0)


def main():
    """Application entry point"""
    import sys
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ModernMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
