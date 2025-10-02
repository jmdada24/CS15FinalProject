"""
Boolean Todo List - Python/PyQt5 Version
Main entry point with phone-like frame and navigation
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from config.theme import AppTheme
from screens.splash_screen import SplashScreen
from screens.home_screen import HomeScreen
from screens.add_task_screen import AddTaskScreen

class PhoneFrame(QMainWindow):
    """Main window with phone-like dimensions and frame"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_navigation()
    
    def init_ui(self):
        """Initialize the phone frame UI"""
        self.setWindowTitle("Boolean - Todo List")
        
        # Phone-like dimensions (larger for better viewing)
        phone_width = 520
        phone_height = 920
        
        # Set default size but allow resizing
        self.resize(phone_width, phone_height)
        
        # Set minimum size to prevent too small window
        self.setMinimumSize(350, 600)
        
        # Center window on screen
        screen = QApplication.desktop().screenGeometry()
        x = (screen.width() - phone_width) // 2
        y = (screen.height() - phone_height) // 2
        self.move(x, y)
        
        # Apply theme
        self.setStyleSheet(AppTheme.get_stylesheet())
        
        # Create stacked widget for navigation
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create screens
        self.splash_screen = SplashScreen()
        self.home_screen = HomeScreen()
        self.add_task_screen = AddTaskScreen()
        
        # Add screens to stack
        self.stacked_widget.addWidget(self.splash_screen)  # index 0
        self.stacked_widget.addWidget(self.home_screen)     # index 1
        self.stacked_widget.addWidget(self.add_task_screen) # index 2
        
        # Start with splash screen
        self.stacked_widget.setCurrentIndex(0)
        
        # Transition to home after 2 seconds
        QTimer.singleShot(2000, self.show_home)
    
    def setup_navigation(self):
        """Setup navigation signals"""
        # Home screen navigation
        self.home_screen.navigate_to_add.connect(self.show_add_task)
        
        # Add task screen navigation
        self.add_task_screen.task_saved.connect(self.on_task_saved)
        self.add_task_screen.go_back.connect(self.show_home)
    
    def show_home(self):
        """Navigate to home screen"""
        self.stacked_widget.setCurrentIndex(1)
    
    def show_add_task(self):
        """Navigate to add task screen"""
        # Reset form
        self.add_task_screen.title_input.clear()
        self.add_task_screen.notes_input.clear()
        self.add_task_screen.selected_category = "Other"
        self.add_task_screen.update_chip_styles()
        
        self.stacked_widget.setCurrentIndex(2)
    
    def on_task_saved(self, task):
        """Handle task saved from add screen"""
        self.home_screen.add_task(task)
        self.show_home()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(AppTheme.get_font(14))
    
    # Create and show phone frame
    phone = PhoneFrame()
    phone.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
