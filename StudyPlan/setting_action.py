import sys
# PyQt files
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
# WordDict
from WordDict import WordDict
# GUI
from StudyPlan.GUI import setting_gui
# Vocab
from StudyPlan import TodayList
from StudyPlan import Vocab


class SettingGUI(QMainWindow, setting_gui.Ui_MainWindow, QObject):
    def __init__(self, WORD_DICT):
        super(SettingGUI, self).__init__()
        self.setupUi(self)

        # Init study setting
        self.vocab = Vocab.Vocab(WORD_DICT)
        self.vocab.saveVocab()  # 保存词库
        self.today_list_obj = TodayList.TodayList(self.vocab)

        if self.today_list_obj.new_user:
            self.word_num_today = 50  # 默认值为50
        else:
            self.word_num_today = self.today_list_obj.get_stated_todaylist_length()

        self.textBrowser.setText(str(self.word_num_today))  # 显示今日词数
        self.textBrowser.setAutoFillBackground(True)
        self.listWidget.setAutoFillBackground(True)
        self.listWidget_2.setAutoFillBackground(True)

        self.vocab_dict = self.vocab.getVocabDict()
        _translate = QCoreApplication.translate
        ite = 0
        # print(len(self.vocab_dict))
        for word in self.vocab_dict:
            if self.vocab_dict[word] == 0:
                continue
            print(word)
            self.listWidget.addItem(word)
            self.listWidget_2.addItem('未掌握')
            if self.vocab_dict[word] == 1:
                item = self.listWidget.item(ite)
                # item.setText(_translate("MainWindow", str(word)))
                item.setBackground(QtGui.QColor(0, 255, 0, 40))
                item.setSizeHint(QSize(350, 30))
                item = self.listWidget_2.item(ite)
                # item.setText(_translate("MainWindow", '未掌握'))
                item.setBackground(QtGui.QColor(0, 255, 0, 40))
                item.setSizeHint(QSize(350, 30))
            else:
                print(word)
                item = self.listWidget.item(ite)
                # item.setText(_translate("MainWindow", str(word)))
                item.setBackground(QtGui.QColor(0, 255, 0, 127))
                item.setSizeHint(QSize(350, 30))
                item = self.listWidget_2.item(ite)
                # item.setText(_translate("MainWindow", '未掌握'))
                item.setBackground(QtGui.QColor(0, 255, 0, 127))
                item.setSizeHint(QSize(350, 30))
            ite += 1

    # 设置
    def modify_num(self):
        value, ok = QInputDialog.getInt(self, '学习计划设定', '请输入每天需要背诵的数量：\n（明天才会生效哦）',
                                        self.word_num_today, 5, 700, 1)
        self.word_num_today = value
        self.textBrowser.setText(str(self.word_num_today))  # 更新今日词数
        try:
            self.today_list_obj.set_stated_todaylist_length(value)
        except ValueError:
            QMessageBox.warning(self, '提醒', '设定计划表长度必须为小于等于词库总词数的正整数', QMessageBox.Yes)


if __name__ == "__main__":
    # GUI setup
    WORD_DICT = WordDict.WordDict()
    load_err = WORD_DICT.load('WordDict\dict')
    app = QApplication(sys.argv)
    setting_gui = SettingGUI(WORD_DICT)
    setting_gui.show()
    sys.exit(app.exec_())
