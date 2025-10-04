# local-client/app/main.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from app.gui.main_window import MainWindow
from app.core.config import settings
from app.db.manager import DatabaseManager

def main():
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.init_database()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow(db_manager)
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()