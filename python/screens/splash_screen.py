"""Splash Screen with animation - matches Flutter splash"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from config.theme import AppTheme

class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.init_ui()
    
    def init_ui(self):
        # Set background to primary color
        self.setStyleSheet(f"background-color: {AppTheme.PRIMARY.name()};")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # App title with animation
        self.title_label = QLabel("Boolean")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(AppTheme.get_font(42, QFont.Bold))
        self.title_label.setStyleSheet(f"color: white; background: transparent;")
        
        # Subtitle
        self.subtitle_label = QLabel("Todo List")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setFont(AppTheme.get_font(18))
        self.subtitle_label.setStyleSheet(f"color: {AppTheme.PRIMARY_LIGHT.name()}; background: transparent;")
        
        layout.addWidget(self.title_label)
        layout.addSpacing(10)
        layout.addWidget(self.subtitle_label)
        
        self.setLayout(layout)
        
        # Fade in animation
        self.title_label.setStyleSheet(f"color: rgba(255, 255, 255, 0); background: transparent;")
        self.animate_fade_in()
    
    def animate_fade_in(self):
        """Animate fade in effect"""
        QTimer.singleShot(100, lambda: self.title_label.setStyleSheet(
            f"color: white; background: transparent;"
        ))
