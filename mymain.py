from mymainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget
from WordDict import WordDict
import sys
if __name__ == '__main__':
    #创建主界面
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    WORD_DICT = WordDict.WordDict()
    ui = Ui_MainWindow(WORD_DICT)
    ui.setupUi(MainWindow)
    MainWindow.setStyleSheet("#MainWindow{border-image:url(background1.jpg);}")
    MainWindow.show()    
    #程序开始前，先读入词库数据库
    load_err = WORD_DICT.load('WordDict\\dict')
    if load_err != WordDict.WORD_DICT_LOAD_SUCCEED:
        print(load_err)
        errorWin = QWidget()
        reply = QMessageBox.question(errorWin, 'Message', load_err, QMessageBox.Yes, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            exit(0)
    sys.exit(app.exec_())