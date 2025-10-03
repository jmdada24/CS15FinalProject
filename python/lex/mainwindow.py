from PyQt5.QtWidgets import (
  QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt, QDateTime, QTimer, QTime
from todoLists import TodoLists
from listspanel import ListPanel
from addlistpanel import AddlistPanel

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Todo-List App")
    self.setGeometry(100, 100, 1800, 1000)
    self.showMaximized()
    
    mainPanel = QWidget()
    header = QWidget()
    self.body = QWidget()
    footer = QWidget()

    mainPanelLayout = QVBoxLayout()
    headerLayout = QVBoxLayout()
    bodyLayout = QVBoxLayout()
    footerLayout = QHBoxLayout()

    mainPanel.setLayout(mainPanelLayout)
    header.setLayout(headerLayout)
    self.body.setLayout(bodyLayout)
    footer.setLayout(footerLayout)

    mainPanel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    mainPanelLayout.setContentsMargins(0, 0, 0, 0)

    header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    header.setContentsMargins(100, 20, 100, 20)
    header.setStyleSheet("""
      background-color: rgb(92, 76, 129);
      color: white;
      font-family: 'Arial';
      border-bottom-right-radius: 20px;
      border-bottom-left-radius: 20px;
    """)
    header.setFixedHeight(150)
    
    self.headerUpperLabel = QLabel() 
    self.headerUpperLabel.setStyleSheet("""
      font-size: 10px;
      font-weight: normal;
      color: rgba(255, 255, 255, 0.7);
    """)

    headerLowerLabel = QLabel("My To-Do List")
    headerLowerLabel.setStyleSheet("""
      font-size: 32px; 
      font-weight: bold;
    """)

    headerLayout.addWidget(self.headerUpperLabel)
    headerLayout.addWidget(headerLowerLabel)

    self.body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.body.setMinimumHeight(700)
    self.body.setStyleSheet("""
      background-color: rgb(240, 240, 240);
      font-family: 'Arial';
    """)

    self.tempWidget = QStackedWidget()
    self.tempWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.contentPanel = QWidget()
    self.contentPanelLayout = QVBoxLayout()
    self.contentPanel.setLayout(self.contentPanelLayout)
    self.contentPanel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.contentPanel.setStyleSheet("""
      background-color: rgb(245, 245, 245);
    """)
    self.tempWidget.addWidget(self.contentPanel)
    bodyLayout.addWidget(self.tempWidget)

    addButton = QPushButton("Add")
    addButton.setFixedSize(100, 40)
    addButton.setCursor(Qt.PointingHandCursor)
    addButton.setStyleSheet("""
      background-color: rgb(92, 76, 129);
      color: white;
      font-size: 24px;
      padding: 10px 20px;
      border-radius: 10px;
    """)
    self.contentPanel.layout().addWidget(addButton, alignment=Qt.AlignCenter)
    addButton.clicked.connect(self.add_list)

    footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  
    footer.setFixedHeight(60)
    footer.setStyleSheet("""
      background-color: rgb(92, 76, 129);
      border-top-right-radius: 20px;
      border-top-left-radius: 20px;
    """)

    mainPanelLayout.addWidget(header)
    mainPanelLayout.addWidget(self.body)
    mainPanelLayout.addWidget(footer)

    self.setCentralWidget(mainPanel)
    self._update_date()
    self._schedule_midnight_update()
    lists = TodoLists()

    if lists.get_lists():
      self.tempWidget.setCurrentWidget(ListPanel())
    
  def _update_date(self):
    now = QDateTime.currentDateTime()
    formatted = now.toString("MMM d yyyy")  # e.g. "Sep 14 2025"
    self.headerUpperLabel.setText(formatted)

  def _schedule_midnight_update(self):
    now = QTime.currentTime()
    midnight = QTime(0, 0)
    msecs_until_midnight = now.msecsTo(midnight.addSecs(24 * 60 * 60))

    QTimer.singleShot(msecs_until_midnight, self._update_and_reschedule)

  def _update_and_reschedule(self):
    self._update_date()
    self._schedule_midnight_update()

  def add_list(self):
    panel = AddlistPanel()
    self.tempWidget.addWidget(panel)
    self.tempWidget.setCurrentWidget(panel)


  
