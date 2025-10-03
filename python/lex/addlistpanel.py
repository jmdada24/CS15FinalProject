from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit

class AddlistPanel(QWidget):
  def __init__(self):
    super().__init__()
    self.setStyleSheet("""
      font-family: 'Arial';
    """)
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    self.ltitle = QLineEdit()
    self.ltitle.setPlaceholderText("Enter list name")
    self.ltitle.setStyleSheet("""                        
      font-size: 18px;
      font-weight: bold;
      padding: 10px;
      border: 1px solid rgb(113,94,157);
      border-radius: 5px;
    """)
    main_layout.addWidget(self.ltitle)

    self.txtadescription = QTextEdit()
    self.txtadescription.setPlaceholderText("Enter list description")
    self.txtadescription.setStyleSheet("""
      font-size: 16px;
      padding: 10px;
      border: 1px solid rgb(113,94,157);
      border-radius: 5px;
    """)
    main_layout.addWidget(self.txtadescription) 




