from PyQt5.QtWidgets import QWidget

class ListPanel(QWidget):
  def __init__(self, list_name):
    super().__init__()
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)
    
