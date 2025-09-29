import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton


class CounterApp(QWidget):
  def __init__(self, title="Demo Counter"):
    super().__init__()
    self.setWindowTitle(title)

    # No explicit type required — could be int, str, or even a list
    self._counter = 0

    # Widgets
    self.label_info = QLabel("Button pressed this many times:")
    self.label_counter = QLabel(str(self._counter))
    self.button = QPushButton("Increment")

    # In Python, signals can be connected at runtime — no strict signature enforcement
    self.button.clicked.connect(self._increment)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(self.label_info)
    layout.addWidget(self.label_counter)
    layout.addWidget(self.button)
    self.setLayout(layout)

  def _increment(self):
    # Python doesn’t force type safety — this could break if _counter was set to a str
    self._counter += 1
    self.label_counter.setText(str(self._counter))


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = CounterApp()
  window.show()
  sys.exit(app.exec_())
