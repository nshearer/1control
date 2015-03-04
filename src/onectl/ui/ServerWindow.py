'''Main window for server'''
from PySide import QtCore
from PySide import QtGui

from .qt.ServerWindowQt import Ui_ServerWindow

class ServerWindow(QtGui.QMainWindow):
    '''This is the main window displayed for the server application'''
    
    def __init__(self, parent=None):
        super(ServerWindow, self).__init__(parent)
        
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)
        
#         self.browser = QTextBrowser()
#          self.lineedit = QLineEdit("Type something and hit enter")
        
#         layout = QVBoxLayout()
#         layout.addWidget(self.browser)
#         layout.addWidget(self.lineedit)
#         self.setLayout(layout)
        
        self.ui.lineedit.selectAll()
        self.ui.lineedit.setFocus()
        
        self.connect(self.ui.lineedit, QtCore.SIGNAL("returnPressed()"), self.updateUi)
        self.setWindowTitle("1 Control")
        
        
    def updateUi(self):
        try:
            text = self.ui.lineedit.text()
            self.ui.browser.append("%s = <b>%s</b>" % (text, eval(text)))
            self.ui.lineedit.clear()
        except:
            self.ui.browser.append("<font color='red'>%s is invalid</font>" % (text))