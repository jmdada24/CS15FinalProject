from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit

class AddlistPanel(QWidget):
  def __init__(self):
    super().__init__()
    self.setStyleSheet("""
      font-family: 'Arial';
    """)
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    self.title = QLineEdit()
    self.title.setPlaceholderText("Enter list name")
    self.title.setStyleSheet("""                        
      font-size: 18px;
      font-weight: bold;
      padding: 10px;
                            border: 1px
    """)
    main_layout.addWidget(self.line_edit)

    self.descriptio = QTextEdit()
    self.description.setPlaceholderText("Enter list description")
    main_layout.addWidget(self.text_edit) 
