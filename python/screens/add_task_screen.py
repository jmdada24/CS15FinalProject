"""Add/Edit Task Screen - matches Flutter AddTaskScreen"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
                              QTextEdit, QHBoxLayout, QFrame, QPushButton, QDateEdit, QTimeEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QFont
from datetime import datetime
from config.theme import AppTheme
from models.task import Task

class AddTaskScreen(QWidget):
    # Signal to go back with optional new task
    task_saved = pyqtSignal(Task)
    go_back = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_category = "Other"
        self.init_ui()
    
    def init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header (purple AppBar)
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Form content
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(16)
        
        # Task Title section
        title_label = QLabel("📝 Task Title")
        title_label.setFont(AppTheme.get_font(16, QFont.DemiBold))
        form_layout.addWidget(title_label)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task name")
        self.title_input.setFont(AppTheme.get_font(15))
        self.title_input.setFixedHeight(52)
        self.title_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1.5px solid {AppTheme.PRIMARY_LIGHT.name()};
                border-radius: 14px;
                padding: 12px 16px;
                background-color: white;
                font-size: 15px;
            }}
            QLineEdit:focus {{
                border: 2px solid {AppTheme.PRIMARY.name()};
            }}
        """)
        form_layout.addWidget(self.title_input)
        
        form_layout.addSpacing(8)
        
        # Category section
        category_label = QLabel("🏷️ Category")
        category_label.setFont(AppTheme.get_font(16, QFont.DemiBold))
        form_layout.addWidget(category_label)
        
        self.category_buttons = self.create_category_chips()
        form_layout.addLayout(self.category_buttons)
        
        form_layout.addSpacing(8)
        
        # Date and Time row
        datetime_label = QLabel("🕐 Date & Time")
        datetime_label.setFont(AppTheme.get_font(16, QFont.DemiBold))
        form_layout.addWidget(datetime_label)
        
        datetime_layout = QHBoxLayout()
        datetime_layout.setSpacing(12)
        
        # Date picker
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setFixedHeight(52)
        self.date_edit.setDisplayFormat("📅 MMM dd, yyyy")
        self.date_edit.setStyleSheet(f"""
            QDateEdit {{
                border: 1.5px solid {AppTheme.PRIMARY_LIGHT.name()};
                border-radius: 14px;
                padding: 8px 14px;
                background-color: white;
                font-size: 14px;
            }}
            QDateEdit:focus {{
                border: 2px solid {AppTheme.PRIMARY.name()};
            }}
            QDateEdit::drop-down {{
                border: none;
                padding-right: 8px;
            }}
        """)
        datetime_layout.addWidget(self.date_edit, 1)
        
        # Time picker
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setFixedHeight(52)
        self.time_edit.setDisplayFormat("🕐 hh:mm AP")
        self.time_edit.setStyleSheet(f"""
            QTimeEdit {{
                border: 1.5px solid {AppTheme.PRIMARY_LIGHT.name()};
                border-radius: 14px;
                padding: 8px 14px;
                background-color: white;
                font-size: 14px;
            }}
            QTimeEdit:focus {{
                border: 2px solid {AppTheme.PRIMARY.name()};
            }}
            QTimeEdit::drop-down {{
                border: none;
                padding-right: 8px;
            }}
        """)
        datetime_layout.addWidget(self.time_edit, 1)
        
        form_layout.addLayout(datetime_layout)
        
        form_layout.addSpacing(8)
        
        # Notes section
        notes_label = QLabel("📄 Notes")
        notes_label.setFont(AppTheme.get_font(16, QFont.DemiBold))
        form_layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add additional notes...")
        self.notes_input.setFont(AppTheme.get_font(14))
        self.notes_input.setFixedHeight(140)
        self.notes_input.setStyleSheet(f"""
            QTextEdit {{
                border: 1.5px solid {AppTheme.PRIMARY_LIGHT.name()};
                border-radius: 14px;
                padding: 12px 16px;
                background-color: white;
                font-size: 14px;
            }}
            QTextEdit:focus {{
                border: 2px solid {AppTheme.PRIMARY.name()};
            }}
        """)
        form_layout.addWidget(self.notes_input)
        
        form_layout.addSpacing(12)
        
        # Save button
        save_btn = QPushButton("✓ Save Task")
        save_btn.setFont(AppTheme.get_font(17, QFont.DemiBold))
        save_btn.setFixedHeight(56)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppTheme.PRIMARY.name()};
                color: white;
                border: none;
                border-radius: 28px;
                padding: 0px 32px;
                font-size: 17px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {AppTheme.PRIMARY_DARK.name()};
            }}
            QPushButton:pressed {{
                background-color: {AppTheme.PRIMARY_LIGHT.name()};
            }}
        """)
        save_btn.clicked.connect(self.save_task)
        form_layout.addWidget(save_btn)
        
        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget)
        
        self.setLayout(main_layout)
    
    def create_header(self):
        """Create purple AppBar with back button"""
        header = QFrame()
        header.setFixedHeight(90)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {AppTheme.PRIMARY.name()};
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 24, 20, 24)
        
        # Back button
        back_btn = QPushButton("←")
        back_btn.setFixedSize(44, 44)
        back_btn.setFont(AppTheme.get_font(24))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 22px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.15);
            }}
            QPushButton:pressed {{
                background-color: rgba(255, 255, 255, 0.25);
            }}
        """)
        back_btn.clicked.connect(self.go_back.emit)
        
        # Title
        title_label = QLabel("Add New Task")
        title_label.setFont(AppTheme.get_font(20, QFont.DemiBold))
        title_label.setStyleSheet("color: white; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(back_btn)
        layout.addWidget(title_label, 1)
        layout.addSpacing(44)  # Balance for back button
        
        header.setLayout(layout)
        return header
    
    def create_category_chips(self):
        """Create category selection chips"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        categories = ["Other", "Home", "Shopping", "Work", "Fitness"]
        category_icons = {
            "Other": "📌",
            "Home": "🏠",
            "Shopping": "🛒",
            "Work": "💼",
            "Fitness": "💪"
        }
        self.chip_buttons = {}
        
        for category in categories:
            icon = category_icons.get(category, "")
            btn = QPushButton(f"{icon} {category}")
            btn.setFont(AppTheme.get_font(14))
            btn.setFixedHeight(44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, c=category: self.select_category(c))
            self.chip_buttons[category] = btn
            layout.addWidget(btn)
        
        self.update_chip_styles()
        return layout
    
    def select_category(self, category: str):
        """Select a category"""
        self.selected_category = category
        self.update_chip_styles()
    
    def update_chip_styles(self):
        """Update chip button styles based on selection"""
        for category, btn in self.chip_buttons.items():
            if category == self.selected_category:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {AppTheme.PRIMARY.name()};
                        color: white;
                        border: none;
                        border-radius: 22px;
                        padding: 10px 18px;
                        font-weight: 600;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {AppTheme.PRIMARY.lighter(190).name()};
                        color: {AppTheme.TEXT_PRIMARY.name()};
                        border: 1.5px solid {AppTheme.PRIMARY_LIGHT.name()};
                        border-radius: 22px;
                        padding: 10px 18px;
                    }}
                    QPushButton:hover {{
                        background-color: {AppTheme.PRIMARY.lighter(175).name()};
                        border: 1.5px solid {AppTheme.PRIMARY.name()};
                    }}
                    QPushButton:pressed {{
                        background-color: {AppTheme.PRIMARY.lighter(165).name()};
                    }}
                """)
    
    def save_task(self):
        """Save the task"""
        title = self.title_input.text().strip()
        if not title:
            return
        
        # Create task
        task = Task(
            title=title,
            notes=self.notes_input.toPlainText().strip(),
            date=self.date_edit.date().toPyDate(),
            time=self.time_edit.time().toString("hh:mm AP"),
            category=self.selected_category,
            is_done=False
        )
        
        self.task_saved.emit(task)
