from PyQt5.QtWidgets import QWidget, QVBoxLayout

class ListPanel(QWidget):
  def __init__(self):
    super().__init__()
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)
    
    
