"""Task Card Widget - matches Flutter TaskCard design"""
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from config.theme import AppTheme
from models.task import Task

class TaskCard(QFrame):
    # Signals
    edit_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()
    toggle_clicked = pyqtSignal()
    
    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.task = task
        self.init_ui()
    
    def init_ui(self):
        self.setFrameShape(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        
        # Card styling with shadow effect
        bg_color = "#fafafa" if self.task.is_done else "white"
        border_color = "#e8e8e8" if self.task.is_done else "#f0f0f0"
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 20px;
                border: 1.5px solid {border_color};
                padding: 0px;
            }}
            QFrame:hover {{
                border: 1.5px solid {AppTheme.PRIMARY_LIGHT.name()};
                background-color: {AppTheme.PRIMARY.lighter(198).name() if not self.task.is_done else '#f5f5f5'};
            }}
        """)
        
        self.setFixedHeight(90)
        self.setContentsMargins(0, 0, 0, 0)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(16)
        
        # Category icon (clickable to toggle complete)
        self.category_icon = self.create_category_icon()
        main_layout.addWidget(self.category_icon)
        
        # Task title and date/time
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)
        
        title_label = QLabel(self.task.title)
        title_label.setFont(AppTheme.get_font(16, QFont.DemiBold))
        text_color = AppTheme.TEXT_SECONDARY.name() if self.task.is_done else AppTheme.TEXT_PRIMARY.name()
        decoration = "line-through" if self.task.is_done else "none"
        title_label.setStyleSheet(f"color: {text_color}; text-decoration: {decoration}; background: transparent;")
        title_label.setWordWrap(False)
        text_layout.addWidget(title_label)
        
        if self.task.get_datetime_str():
            datetime_container = QHBoxLayout()
            datetime_container.setSpacing(6)
            
            # Clock icon
            clock_icon = QLabel("🕐")
            clock_icon.setFont(AppTheme.get_font(12))
            clock_icon.setStyleSheet("background: transparent;")
            datetime_container.addWidget(clock_icon)
            
            datetime_label = QLabel(self.task.get_datetime_str())
            datetime_label.setFont(AppTheme.get_font(13))
            datetime_label.setStyleSheet(f"color: {AppTheme.TEXT_SECONDARY.name()}; background: transparent;")
            datetime_container.addWidget(datetime_label)
            datetime_container.addStretch()
            
            text_layout.addLayout(datetime_container)
        
        main_layout.addLayout(text_layout, 1)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Edit button
        edit_btn = self.create_icon_button("✏️", AppTheme.PRIMARY)
        edit_btn.clicked.connect(self.edit_clicked.emit)
        buttons_layout.addWidget(edit_btn)
        
        # Delete button
        delete_btn = self.create_icon_button("🗑️", AppTheme.ERROR)
        delete_btn.clicked.connect(self.confirm_delete)
        buttons_layout.addWidget(delete_btn)
        
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
    
    def create_category_icon(self):
        """Create category icon that changes to checkmark when complete"""
        icon_frame = QFrame()
        icon_frame.setFixedSize(56, 56)
        icon_frame.setCursor(Qt.PointingHandCursor)
        
        if self.task.is_done:
            # Green checkmark
            bg_color = "rgba(76, 175, 80, 0.18)"
            icon_text = "✓"
            text_color = AppTheme.SUCCESS.name()
        else:
            # Category icon
            bg_color = self.get_category_color().lighter(185).name()
            icon_text = self.get_category_emoji()
            text_color = self.get_category_color().name()
        
        icon_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 16px;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon_text)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(AppTheme.get_font(26))
        icon_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        
        layout.addWidget(icon_label)
        icon_frame.setLayout(layout)
        
        # Make clickable
        icon_frame.mousePressEvent = lambda e: self.toggle_clicked.emit()
        
        return icon_frame
    
    def create_icon_button(self, icon_text: str, color: QColor):
        """Create small icon button"""
        btn = QPushButton(icon_text)
        btn.setFixedSize(42, 42)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.lighter(195).name()};
                color: {color.name()};
                border: none;
                border-radius: 10px;
                font-size: 18px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {color.lighter(175).name()};
            }}
            QPushButton:pressed {{
                background-color: {color.lighter(160).name()};
            }}
        """)
        return btn
    
    def get_category_color(self) -> QColor:
        """Get color for category"""
        colors = {
            "Home": AppTheme.HOME_COLOR,
            "Shopping": AppTheme.SHOPPING_COLOR,
            "Work": AppTheme.WORK_COLOR,
            "Fitness": AppTheme.FITNESS_COLOR,
        }
        return colors.get(self.task.category, AppTheme.OTHER_COLOR)
    
    def get_category_emoji(self) -> str:
        """Get emoji icon for category"""
        emojis = {
            "Home": "🏠",
            "Shopping": "🛒",
            "Work": "💼",
            "Fitness": "💪",
        }
        return emojis.get(self.task.category, "📌")
    
    def confirm_delete(self):
        """Show confirmation dialog before deleting"""
        reply = QMessageBox.question(
            self,
            "Delete Task",
            "Are you sure you want to delete this task?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.delete_clicked.emit()
    
    def mousePressEvent(self, event):
        """Make entire card clickable to edit"""
        if event.button() == Qt.LeftButton:
            self.edit_clicked.emit()
