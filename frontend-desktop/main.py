"""
ChemViz Pro - Modern Desktop Application
Entry point for PyQt5 desktop application with Lab OS design
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.modern_main_window import ModernMainWindow
from ui.styles import MAIN_STYLESHEET


def main():
    """Main entry point for the desktop application"""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("ChemViz Pro")
    app.setOrganizationName("FOSSEE")
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply global stylesheet
    app.setStyleSheet(MAIN_STYLESHEET)
    
    # Create and show main window
    window = ModernMainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
