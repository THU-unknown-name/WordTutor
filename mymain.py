from mymainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #MainWindow.setStyleSheet("#MainWindow{border-image:url(background.jpg);}")
    MainWindow.show()
    sys.exit(app.exec_())