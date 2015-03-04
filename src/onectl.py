'''One Control Server instance'''
import sys
from PySide.QtCore import *
from PySide.QtGui import *

import gflags

from onectl.ui.ServerWindow import ServerWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = ServerWindow()
    window.show()
    
    print "Running"    
    
    app.exec_()
    
    print "Finished"