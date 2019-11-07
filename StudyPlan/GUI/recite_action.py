import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication
from StudyPlan.GUI import recite_gui


class Recite_Remember(QMainWindow, recite_gui.Ui_MainWindow):
    def __init__(self):
        super(Recite_Remember, self).__init__()
        self.setupUi(self)
        self.pushButton_revoke.setVisible(False)
        self.pushButton_next.setVisible(False)
        self.label_stop_showing.setVisible(False)
        self.label_show_again.setVisible(False)
        # self.today_list = today_list

    def show_exp(self):
        _translate = QCoreApplication.translate
        self.textBrowser_word.setHtml(_translate("MainWindow",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:36pt;\">test</span></p></body></html>"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = Recite_Remember()
    my_pyqt_form.show()
    sys.exit(app.exec_())
