import sys
# PyQt files
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import *
# GUI
from GUI import recite_gui
# Vocab
import TodayList
import Vocab


class ReciteWords:
    def __init__(self):
        # Get todayList
        # self.today_list = ["test"]
        self.vocab = Vocab.Vocab()
        self.vocab.saveVocab()  # 保存词库
        self.today_list = TodayList.TodayList(self.vocab).getTodayList()
        self.ite = 0
        self.review_list = []
        self.is_first_round = True
        if len(self.today_list) > 0:
            self.word_current = self.today_list[self.ite]
        else:
            print("Fail to get recite list for today")
            sys.exit()

    def next_word(self):
        """
        get next word
        if has_next_word:
            return true
        else: (have finished today's task)
            return false
        """
        self.ite += 1
        if self.ite >= len(self.today_list):
            self.today_list = self.review_list.copy()
            self.review_list.clear()
            self.ite = 0
            self.is_first_round = False
            if len(self.today_list) < 1:
                return False

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
        self.vocab.updateFamiliarity(word=self.word_current, familiarity=1)

    def upgrade(self):
        # Only upgrade in first round
        if self.is_first_round:
            # new 会 --> familiar
            # familiar 会 --> familiar
            # unfamiliar 会 --> familiar
            self.vocab.updateFamiliarity(word=self.word_current, familiarity=2)
        else:
            pass


class ReciteGUI(QMainWindow, recite_gui.Ui_MainWindow, QObject):
    complete_all = pyqtSignal()

    def __init__(self):
        super(ReciteGUI, self).__init__()
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
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.pushButton_exit.setVisible(False)

        self.complete_all.connect(self.label_2.show)
        self.complete_all.connect(self.label_3.show)
        self.complete_all.connect(self.listWidget.hide)
        self.complete_all.connect(self.pushButton_yes.hide)
        self.complete_all.connect(self.pushButton_no.hide)
        self.complete_all.connect(self.pushButton_next.hide)
        self.complete_all.connect(self.pushButton_revoke.hide)
        self.complete_all.connect(self.label_show_again.hide)
        self.complete_all.connect(self.label_stop_showing.hide)
        self.complete_all.connect(self.pushButton_exit.show)

        self.reciting = ReciteWords()
        self.forget_this_word = False
        self.update_word_info()
        self.finished_words_num = 0
        self.total_words_num = len(self.reciting.today_list)
        self.progressBar.setValue(0)

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
        item.setText(_translate("MainWindow", info[0][0]))  # TODO: it is easy to break down
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", info[0][1]))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "".join(info[1])))


# if __name__ == "__main__":
#     # GUI setup
#     app = QApplication(sys.argv)
#     recite_gui = ReciteGUI()
#     recite_gui.show()
#     sys.exit(app.exec_())
