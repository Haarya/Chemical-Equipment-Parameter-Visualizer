"""
Chemical Equipment Parameter Visualizer - Desktop Application
Entry point for PyQt5 desktop application
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main entry point for the desktop application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("FOSSEE")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
