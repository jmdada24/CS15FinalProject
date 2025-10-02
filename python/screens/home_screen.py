"""Home Screen - Main todo list view matching Flutter design"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                              QScrollArea, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime
from config.theme import AppTheme
from models.task import Task
from widgets.task_card import TaskCard

class HomeScreen(QWidget):
    # Signal to navigate to add task screen
    navigate_to_add = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = []  # List of Task objects
        self.init_ui()
    
    def init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header with purple background (rounded bottom)
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Scrollable task list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")
        
        # Container for tasks
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_layout.setContentsMargins(16, 16, 16, 80)
        self.task_layout.setSpacing(0)
        self.task_container.setLayout(self.task_layout)
        
        scroll_area.setWidget(self.task_container)
        main_layout.addWidget(scroll_area)
        
        # Bottom Add button (fixed at bottom)
        add_button = self.create_add_button()
        main_layout.addWidget(add_button)
        
        self.setLayout(main_layout)
        self.refresh_tasks()
    
    def create_header(self):
        """Create purple header with date, title and progress"""
        header = QFrame()
        header.setFixedHeight(180)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {AppTheme.PRIMARY.name()};
                border-bottom-left-radius: 24px;
                border-bottom-right-radius: 24px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 32, 24, 32)
        layout.setSpacing(12)
        
        # Top row: Date and progress badge
        top_row = QHBoxLayout()
        
        # Date label
        date_label = QLabel(datetime.now().strftime("%b %d, %Y"))
        date_label.setFont(AppTheme.get_font(14))
        date_label.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent;")
        top_row.addWidget(date_label)
        
        top_row.addStretch()
        
        # Progress badge
        self.progress_badge = QLabel("0/0")
        self.progress_badge.setFont(AppTheme.get_font(14, QFont.DemiBold))
        self.progress_badge.setStyleSheet(f"""
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border-radius: 16px;
            padding: 6px 14px;
        """)
        self.progress_badge.setAlignment(Qt.AlignCenter)
        top_row.addWidget(self.progress_badge)
        
        layout.addLayout(top_row)
        
        # Title
        title_label = QLabel("My Tasks")
        title_label.setFont(AppTheme.get_font(32, QFont.Bold))
        title_label.setStyleSheet("color: white; background: transparent; letter-spacing: -0.5px;")
        layout.addWidget(title_label)
        
        # Progress bar
        self.progress_bar = QFrame()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet(f"""
            background-color: rgba(255, 255, 255, 0.25);
            border-radius: 4px;
        """)
        
        # Inner progress fill
        progress_container = QHBoxLayout()
        progress_container.setContentsMargins(0, 0, 0, 0)
        progress_container.setSpacing(0)
        
        self.progress_fill = QFrame()
        self.progress_fill.setStyleSheet(f"""
            background-color: white;
            border-radius: 4px;
        """)
        self.progress_fill.setFixedHeight(8)
        self.progress_fill.setFixedWidth(0)  # Will update dynamically
        
        progress_container.addWidget(self.progress_fill)
        progress_container.addStretch()
        self.progress_bar.setLayout(progress_container)
        
        layout.addWidget(self.progress_bar)
        
        header.setLayout(layout)
        return header
    
    def create_add_button(self):
        """Create fixed bottom Add New Task button"""
        container = QFrame()
        container.setFixedHeight(90)
        container.setStyleSheet(f"background-color: {AppTheme.BACKGROUND.name()};")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 16, 20, 16)
        
        btn = QPushButton("+ New Task")
        btn.setFont(AppTheme.get_font(16, QFont.DemiBold))
        btn.setFixedHeight(56)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppTheme.PRIMARY.name()};
                color: white;
                border: none;
                border-radius: 28px;
                padding: 0px 32px;
                font-size: 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {AppTheme.PRIMARY_DARK.name()};
            }}
            QPushButton:pressed {{
                background-color: {AppTheme.PRIMARY_LIGHT.name()};
            }}
        """)
        btn.clicked.connect(self.navigate_to_add.emit)
        
        layout.addWidget(btn)
        container.setLayout(layout)
        return container
    
    def refresh_tasks(self):
        """Refresh task list display"""
        # Clear existing widgets
        while self.task_layout.count():
            item = self.task_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Update progress
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.is_done])
        self.progress_badge.setText(f"{completed}/{total}")
        
        # Update progress bar
        if total > 0:
            progress_percent = (completed / total)
            bar_width = int(self.progress_bar.width() * progress_percent)
            self.progress_fill.setFixedWidth(max(bar_width, 0))
        else:
            self.progress_fill.setFixedWidth(0)
        
        if not self.tasks:
            # Show empty state with better styling
            empty_container = QWidget()
            empty_layout = QVBoxLayout()
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_layout.setSpacing(16)
            
            # Large icon
            icon_label = QLabel("✓")
            icon_label.setFont(AppTheme.get_font(80))
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet(f"""
                color: {AppTheme.PRIMARY_LIGHT.name()};
                background-color: {AppTheme.PRIMARY.lighter(195).name()};
                border-radius: 60px;
                min-width: 120px;
                max-width: 120px;
                min-height: 120px;
                max-height: 120px;
            """)
            
            # Text
            empty_label = QLabel("No tasks yet")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setFont(AppTheme.get_font(20, QFont.DemiBold))
            empty_label.setStyleSheet(f"color: {AppTheme.TEXT_PRIMARY.name()}; background: transparent;")
            
            subtitle_label = QLabel("Tap the button below to add your first task")
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_label.setFont(AppTheme.get_font(14))
            subtitle_label.setStyleSheet(f"color: {AppTheme.TEXT_SECONDARY.name()}; background: transparent;")
            subtitle_label.setWordWrap(True)
            
            empty_layout.addStretch()
            empty_layout.addWidget(icon_label)
            empty_layout.addSpacing(8)
            empty_layout.addWidget(empty_label)
            empty_layout.addWidget(subtitle_label)
            empty_layout.addStretch()
            
            empty_container.setLayout(empty_layout)
            self.task_layout.addWidget(empty_container)
            return
        
        # Separate pending and completed tasks
        pending = [t for t in self.tasks if not t.is_done]
        completed_tasks = [t for t in self.tasks if t.is_done]
        
        # Show pending tasks
        if pending:
            section_label = QLabel(f"Active Tasks")
            section_label.setFont(AppTheme.get_font(18, QFont.Bold))
            section_label.setStyleSheet(f"""
                color: {AppTheme.TEXT_PRIMARY.name()}; 
                background: transparent; 
                padding: 12px 8px 8px 8px;
                border-left: 4px solid {AppTheme.PRIMARY.name()};
                padding-left: 12px;
            """)
            self.task_layout.addWidget(section_label)
            
            for task in pending:
                card = TaskCard(task)
                card.edit_clicked.connect(lambda t=task: self.edit_task(t))
                card.delete_clicked.connect(lambda t=task: self.delete_task(t))
                card.toggle_clicked.connect(lambda t=task: self.toggle_task(t))
                self.task_layout.addWidget(card)
            
            self.task_layout.addSpacing(8)
        
        # Show completed tasks
        if completed_tasks:
            self.task_layout.addSpacing(16)
            section_label = QLabel(f"Completed")
            section_label.setFont(AppTheme.get_font(18, QFont.Bold))
            section_label.setStyleSheet(f"""
                color: {AppTheme.TEXT_PRIMARY.name()}; 
                background: transparent; 
                padding: 12px 8px 8px 8px;
                border-left: 4px solid {AppTheme.SUCCESS.name()};
                padding-left: 12px;
            """)
            self.task_layout.addWidget(section_label)
            
            for task in completed_tasks:
                card = TaskCard(task)
                card.edit_clicked.connect(lambda t=task: self.edit_task(t))
                card.delete_clicked.connect(lambda t=task: self.delete_task(t))
                card.toggle_clicked.connect(lambda t=task: self.toggle_task(t))
                self.task_layout.addWidget(card)
        
        self.task_layout.addStretch()
    
    def add_task(self, task: Task):
        """Add new task"""
        self.tasks.insert(0, task)
        self.refresh_tasks()
    
    def edit_task(self, task: Task):
        """Handle edit task - to be implemented with navigation"""
        print(f"Edit task: {task.title}")
    
    def delete_task(self, task: Task):
        """Delete task"""
        if task in self.tasks:
            self.tasks.remove(task)
            self.refresh_tasks()
    
    def toggle_task(self, task: Task):
        """Toggle task completion"""
        task.toggle_done()
        self.refresh_tasks()
