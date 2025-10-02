"""Theme configuration matching Flutter app design"""
from PyQt5.QtGui import QColor, QFont

class AppTheme:
    # Colors - matching Flutter deepPurple theme
    PRIMARY = QColor(103, 58, 183)  # Deep Purple
    PRIMARY_LIGHT = QColor(179, 157, 219)
    PRIMARY_DARK = QColor(69, 39, 160)
    BACKGROUND = QColor(245, 245, 245)
    CARD_BG = QColor(255, 255, 255)
    TEXT_PRIMARY = QColor(33, 33, 33)
    TEXT_SECONDARY = QColor(117, 117, 117)
    TEXT_WHITE = QColor(255, 255, 255)
    
    # Category colors
    HOME_COLOR = QColor(76, 175, 80)  # Green
    SHOPPING_COLOR = QColor(255, 152, 0)  # Orange
    WORK_COLOR = QColor(33, 150, 243)  # Blue
    FITNESS_COLOR = QColor(156, 39, 176)  # Purple
    OTHER_COLOR = QColor(158, 158, 158)  # Grey
    
    # Status colors
    SUCCESS = QColor(76, 175, 80)
    ERROR = QColor(244, 67, 54)
    
    # Fonts - using system fonts similar to Poppins
    FONT_FAMILY = "Segoe UI"
    
    @staticmethod
    def get_font(size=14, weight=QFont.Normal):
        font = QFont(AppTheme.FONT_FAMILY, size)
        font.setWeight(weight)
        return font
    
    @staticmethod
    def get_stylesheet():
        """Main stylesheet for the app"""
        return f"""
            QWidget {{
                background-color: {AppTheme.BACKGROUND.name()};
                font-family: '{AppTheme.FONT_FAMILY}';
                color: {AppTheme.TEXT_PRIMARY.name()};
            }}
            
            QPushButton {{
                background-color: {AppTheme.PRIMARY.name()};
                color: white;
                border: none;
                border-radius: 24px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
            }}
            
            QPushButton:hover {{
                background-color: {AppTheme.PRIMARY_DARK.name()};
            }}
            
            QPushButton:pressed {{
                background-color: {AppTheme.PRIMARY_LIGHT.name()};
            }}
            
            QLineEdit, QTextEdit {{
                border: 1px solid {AppTheme.PRIMARY_LIGHT.name()};
                border-radius: 12px;
                padding: 12px;
                background-color: white;
                font-size: 14px;
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid {AppTheme.PRIMARY.name()};
            }}
            
            QLabel {{
                background: transparent;
            }}
            
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """
