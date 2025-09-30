import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QLineEdit, QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont


# -------- Custom widget for list item -------- #
class ListItemWidget(QFrame):
    def __init__(self, name, date, delete_callback):
        super().__init__()
        self.name = name
        self.delete_callback = delete_callback

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        # Left side (name + date stacked vertically)
        text_layout = QVBoxLayout()
        self.name_label = QLabel(name)
        self.name_label.setFont(QFont("Segoe UI Variable", 18, QFont.Bold))
        self.name_label.setStyleSheet("color: #ffffff;")

        self.date_label = QLabel(date)
        self.date_label.setFont(QFont("Segoe UI Variable", 10))
        self.date_label.setStyleSheet("color: #aaaaaa;")

        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.date_label)

        # Right side (Delete button)
        self.del_btn = QPushButton("Delete")
        self.del_btn.setFont(QFont("Segoe UI Variable", 11))
        self.del_btn.setFixedWidth(80)
        self.del_btn.setBackgroundColor = "#ff4d4d"
        self.del_btn.clicked.connect(self.handle_delete)

        layout.addLayout(text_layout)
        layout.addWidget(self.del_btn)

        self.setLayout(layout)

    def handle_delete(self):
        self.delete_callback(self.name)


# -------- Task Window (tasks inside a list) -------- #
class TaskWindow(QWidget):
    def __init__(self, list_name, tasks, parent):
        super().__init__()
        self.list_name = list_name
        self.tasks = tasks
        self.parent = parent
        self.setWindowTitle(f"Tasks - {list_name}")
        self.setGeometry(200, 200, 500, 600)
        self.setStyleSheet(self.parent.styleSheet())  # Apply same style

        layout = QVBoxLayout()

        title = QLabel(list_name)
        title.setFont(QFont("Segoe UI Variable", 20, QFont.Bold))
        title.setStyleSheet("color: #ffffff;")
        layout.addWidget(title)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("font-size: 16px; color: #ffffff;")
        for task in tasks:
            self.task_list.addItem(task)
        layout.addWidget(self.task_list)

        input_row = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter new task...")
        input_row.addWidget(self.task_input)

        add_btn = QPushButton("Add Task")
        add_btn.setFont(QFont("Segoe UI Variable", 14))
        add_btn.setBackgroundColor = "#2d2d2d"
        add_btn.clicked.connect(self.add_task)
        input_row.addWidget(add_btn)
        layout.addLayout(input_row)

        del_btn = QPushButton("Delete Selected Task")
        del_btn.clicked.connect(self.delete_task)
        layout.addWidget(del_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def add_task(self):
        text = self.task_input.text().strip()
        if text:
            self.task_list.addItem(text)
            self.tasks.append(text)
            self.task_input.clear()

    def delete_task(self):
        current = self.task_list.currentRow()
        if current >= 0:
            del self.tasks[current]
            self.task_list.takeItem(current)

    def go_back(self):
        self.close()
        self.parent.show()


# -------- Main Window (list of lists) -------- #
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List Manager")
        self.setGeometry(150, 150, 500, 600)

        # Dark mode Windows 11 style
        self.setStyleSheet("""
            QWidget {
                background-color: #202020;
                font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
                color: #ffffff;
            }
            QPushButton {
                border: 1px solid #3a3a3a;
                border-radius: 10px;
                padding: 6px 10px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
            QListWidget {
                border: 1px solid #3a3a3a;
                border-radius: 10px;
                background-color: #252525;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #0078D4;
                color: white;
                border-radius: 6px;
            }
            QLineEdit {
                border: 1px solid #3a3a3a;
                border-radius: 10px;
                padding: 6px 8px;
                background-color: #2d2d2d;
                color: #ffffff;
            }
        """)

        self.lists = {}

        layout = QVBoxLayout()

        title = QLabel("My To-Do Lists")
        title.setFont(QFont("Segoe UI Variable", 24, QFont.Bold))
        layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.open_list)  # Open by clicking
        layout.addWidget(self.list_widget)

        input_row = QHBoxLayout()
        self.list_input = QLineEdit()
        self.list_input.setPlaceholderText("Enter new list name...")
        input_row.addWidget(self.list_input)

        add_list_btn = QPushButton("Add List")
        add_list_btn.clicked.connect(self.create_list)
        input_row.addWidget(add_list_btn)
        layout.addLayout(input_row)

        self.setLayout(layout)

    def create_list(self):
        name = self.list_input.text().strip()
        if name:
            if name in self.lists:
                QMessageBox.warning(self, "Error", "List already exists!")
                return
            date_created = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
            self.lists[name] = {"date": date_created, "tasks": []}

            widget = ListItemWidget(name, date_created, self.delete_list)
            item = QListWidgetItem(self.list_widget)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.setItemWidget(item, widget)

            self.list_input.clear()

    def open_list(self, item):
        # Find which row was clicked
        row = self.list_widget.row(item)
        name = list(self.lists.keys())[row]
        tasks = self.lists[name]["tasks"]
        self.hide()
        self.task_window = TaskWindow(name, tasks, self)
        self.task_window.show()

    def delete_list(self, name):
        if name in self.lists:
            del self.lists[name]
            for i in range(self.list_widget.count()):
                widget = self.list_widget.itemWidget(self.list_widget.item(i))
                if widget and widget.name == name:
                    self.list_widget.takeItem(i)
                    break


# -------- Run App -------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
