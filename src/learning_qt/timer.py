import sys
from PySide.QtCore import *
from PySide.QtGui import *
import time


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    due = QTime.currentTime()
    message = "Alert!"
    
    due = QTime(16, 48)
    
    while QTime.currentTime() < due:
        print "Waiting"
        time.sleep(10)
        
    print "Showing"
    label = QLabel("<font color=red size=72><b>Alert!</b></font>")
    label.setWindowFlags(Qt.SplashScreen)
    label.show()
    
    print "Scheduling"
    QTimer.singleShot(20000, app.quit)
    
    print "Running"    
    app.exec_()
    
    print "Finished"