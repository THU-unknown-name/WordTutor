import sys
# PyQt files
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
# GUI
from StudyPlan.GUI import recite_gui
# Vocab
from StudyPlan import TodayList
from StudyPlan import Vocab


# class SetNumWindow(QWidget):
#     def __init__(self):
#         super(SetNumWindow).__init__()
#         self.setWindowTitle("每日词量设置")
#         self.resize(400, 300)
#         self.num = 50
#
#         widget_hori = QVBoxLayout(self)
#         label_hint = QLabel()
#         label_hint.setText('请输入每天需要背诵的单词数量：')
#         self.edit_num = QInputDialog()
#         push_button_confirm = QPushButton('确定')
#         widget_hori.addWidget(label_hint)
#         widget_hori.addWidget(self.edit_num)
#         widget_hori.addWidget(push_button_confirm)
#
#         # push_button_confirm.clicked.connect(self.close())
#         push_button_confirm.clicked.connect(self.num_upd)
#
#     def num_upd(self):
#         self.num = self.edit_num.getInt()


class ReciteWords:
    def __init__(self, WORD_DICT, parent):
        # Get todayList
        # self.today_list = ["test"]
        self.vocab = Vocab.Vocab(WORD_DICT)
        self.vocab.saveVocab()  # 保存词库
        self.today_list_obj = TodayList.TodayList(self.vocab)
        if self.today_list_obj.new_user:
            value, ok = QInputDialog.getInt(parent, '学习计划设定', '请输入每天需要背诵的数量(5-700)：', 50, 5, 700, 1)
            self.today_list_obj.plan_for_new_user(value, self.vocab)
        self.today_list_dict = self.today_list_obj.getTodayList()
        self.today_list = list(self.today_list_dict.keys())
        self.finished = False
        self.ite = -1
        self.review_list = []
        # self.is_first_round = True
        if self.next_word():
            print('开始背单词')
            if len(self.today_list) > 0:
                self.word_current = self.today_list[self.ite]
            else:
                print("Fail to get recite list for today")
                self.finished = True
        else:  # 今天的任务已经背完了
            QMessageBox.information(parent, '提醒', '你已经背完今天的单词了呢，注意劳逸结合哦~', QMessageBox.Yes)
            # parent.close()
            self.finished = True

    def next_word(self):
        """
        get next word
        if has_next_word:
            return true
        else: (have finished today's task)
            return false
        """
        while True:  # 找到下一个不是已完成的单词
            # today_list_dict: 0 -- 没背过；1 -- 背过没记住；2 -- 已经背过了（或者没记住然后记住了）
            self.ite += 1
            if self.ite >= len(self.today_list):
                self.today_list = self.review_list.copy()
                self.review_list.clear()
                self.ite = 0
                # self.is_first_round = False
                if len(self.today_list) < 1:
                    return False
            if self.today_list_dict[self.today_list[self.ite]] < 2:
                break

        self.word_current = self.today_list[self.ite]
        return True

    def get_word_info(self):
        return self.vocab.getInfo(self.word_current)

    def review_this_word(self):
        # this word will show again today
        self.review_list.append(self.word_current)
        print(self.word_current)

    def downgrade(self):
        """
        new 不会 --> unfamiliar
        familiar 不会 --> unfamiliar
        unfamiliar 不会 --> unfamiliar
        """
        self.today_list_dict[self.word_current] = 1  # 背过但没记住
        self.vocab.updateFamiliarity(word=self.word_current, familiarity=1)

    def upgrade(self):
        # Only upgrade in first round
        if self.today_list_dict[self.word_current] == 0:
            # new 会 --> familiar
            # familiar 会 --> familiar
            # unfamiliar 会 --> familiar
            self.vocab.updateFamiliarity(word=self.word_current, familiarity=2)
        else:
            pass
        self.today_list_dict[self.word_current] = 2  # 记住了，今天不再背


class ReciteGUI(QMainWindow, recite_gui.Ui_MainWindow, QObject):
    complete_all = pyqtSignal()

    def __init__(self, WORD_DICT):
        super(ReciteGUI, self).__init__()
        self.WORD_DICT = WORD_DICT
        self.setupUi(self)
        self.pushButton_revoke.setVisible(False)
        self.pushButton_next.setVisible(False)
        self.label_stop_showing.setVisible(False)
        self.label_show_again.setVisible(False)
        _translate = QCoreApplication.translate
        self.listWidget.setSortingEnabled(False)
        self.listWidget.item(1).setHidden(True)
        self.listWidget.item(2).setHidden(True)
        self.listWidget.item(3).setHidden(True)
        self.listWidget.item(4).setHidden(True)
        self.listWidget.item(5).setHidden(True)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        #self.pushButton_exit.setVisible(False)

        self.complete_all.connect(self.label_2.show)
        self.complete_all.connect(self.label_3.show)
        self.complete_all.connect(self.listWidget.hide)
        self.complete_all.connect(self.pushButton_yes.hide)
        self.complete_all.connect(self.pushButton_no.hide)
        self.complete_all.connect(self.pushButton_next.hide)
        self.complete_all.connect(self.pushButton_revoke.hide)
        self.complete_all.connect(self.label_show_again.hide)
        self.complete_all.connect(self.label_stop_showing.hide)
        #self.complete_all.connect(self.pushButton_exit.show)

        self.reciting = ReciteWords(self.WORD_DICT, self)
        self.finished = False
        if self.reciting.finished:
            # self.close()
            self.finished = True
        else:
            self.forget_this_word = False
            self.update_word_info()
            self.finished_words_num = self.reciting.today_list_obj.finished_num
            self.total_words_num = len(self.reciting.today_list)
            self.progressBar.setValue((self.finished_words_num * 100.0) / self.total_words_num)

    def word_display_upd(self, visible):
        # _translate = QCoreApplication.translate
        # item = self.listWidget.item(0)
        # item.setText(_translate("MainWindow", self.word_current))
        # item = self.listWidget.item(1)
        # item.setText(_translate("MainWindow", "pron"))
        # item = self.listWidget.item(2)
        # item.setText(_translate("MainWindow", "meaning"))
        # item = self.listWidget.item(3)
        # item.setText(_translate("MainWindow", "sent1"))
        self.listWidget.item(1).setHidden(not visible)
        self.listWidget.item(2).setHidden(not visible)
        self.listWidget.item(3).setHidden(not visible)
        self.listWidget.item(4).setHidden(not visible)
        self.listWidget.item(5).setHidden(not visible)

    def show_exp(self):
        # slot
        self.word_display_upd(True)

    def hide_exp(self):
        # slot
        self.word_display_upd(False)

    def forget(self):
        # slot
        self.reciting.review_this_word()
        self.reciting.downgrade()
        self.forget_this_word = True

    def next_word(self):
        # slot
        if self.forget_this_word:
            pass
        else:
            self.reciting.upgrade()
            self.finished_words_num += 1
            self.progressBar.setValue((self.finished_words_num * 100.0) / self.total_words_num)
        if self.reciting.next_word():
            self.update_word_info()
            self.forget_this_word = False
            self.pushButton_yes.setVisible(True)
            self.pushButton_no.setVisible(True)
        else:
            # signal for finishing today_list
            self.complete_all.emit()

    # def complete(self):
    #     self.complete_all.emit()

    def update_word_info(self):
        word = self.reciting.word_current
        info = self.reciting.get_word_info()

        _translate = QCoreApplication.translate
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", word))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", info[0][0]).replace('\n', ' '))  # TODO: merge into a single line
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", info[0][1]).replace('\n', ' '))
        exp = info[1]['reiku']
        str = []
        for i in range(len(exp)):
            s_en = exp[i][0].split('\n')
            s_en = s_en[2:]
            s_ch = exp[i][1].split('\n')
            s_ch = s_ch[1:]
            if (len(s_ch) > 0) and (len(s_en) > 0):
                str.append("{}\n{}".format(s_en[0], s_ch[0]))
        for i in range(min(len(str), 3)):
            item = self.listWidget.item(3 + i)
            item.setText(_translate("MainWindow", str[i]))

    def closeEvent(self, event):
        print("Close event activated.")
        self.reciting.vocab.saveVocab()
        self.reciting.today_list_obj.record_finished(self.finished_words_num,
                                                     self.reciting.today_list_dict)  # 为了下次能够显示已经背的词数
        self.reciting.today_list_obj.save_todaylist()

# if __name__ == "__main__":
#     # GUI setup
#     app = QApplication(sys.argv)
#     recite_gui = ReciteGUI()
#     recite_gui.show()
#     sys.exit(app.exec_())
