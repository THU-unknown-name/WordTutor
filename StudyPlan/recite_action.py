import sys
# PyQt files
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication
# GUI
from StudyPlan.GUI import recite_gui
# Vocab
from StudyPlan import TodayList
from StudyPlan import Vocab


class ReciteWords:
    def __init__(self):
        # Get todayList
        # self.today_list = ["test"]
        self.vocab = Vocab.Vocab()
        self.today_list = TodayList.TodayList(self.vocab).getTodayList()
        self.ite = 0
        self.review_list = []
        if len(self.today_list) > 0:
            self.word_current = self.today_list[self.ite]
        else:
            print("Fail to get recite list for today")
            sys.exit()

    def next_word(self):
        self.ite += 1
        if self.ite < len(self.today_list):
            self.word_current = self.today_list[self.ite]
        else:
            self.today_list = self.review_list
            self.review_list = []
            self.ite = 0
            if len(self.today_list) < 1:
                # TODO: 结束背诵
                pass

    def get_word_info(self):
        return self.vocab.getInfo(self.word_current)

    def review_this_word(self):
        self.review_list.append(self.word_current)

    def downgrade(self):
        # new 不会 --> unfamiliar
        # familiar 不会 --> unfamiliar
        # unfamiliar 不会 --> unfamiliar
        self.vocab.updateFamiliarity(word=self.word_current, familiarity=1)

    def upgrade(self):
        # new 会 --> familiar
        # familiar 会 --> familiar
        # unfamiliar 会 --> familiar
        self.vocab.updateFamiliarity(word=self.word_current, familiarity=2)


class ReciteGUI(QMainWindow, recite_gui.Ui_MainWindow):
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

        self.reciting = ReciteWords()
        self.forget_this_word = False

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
        self.listWidget.item(1).setHidden(~visible)
        self.listWidget.item(2).setHidden(~visible)
        self.listWidget.item(3).setHidden(~visible)

    def show_exp(self):
        self.word_display_upd(True)

    def hide_exp(self):
        self.word_display_upd(False)

    def forget(self):
        self.reciting.review_this_word()
        self.reciting.downgrade()
        self.forget_this_word = True

    def next_word(self):
        if self.forget_this_word:
            pass
        else:
            self.reciting.upgrade()
        self.reciting.next_word()

    def update_word_info(self):
        word = self.reciting.word_current
        info = self.reciting.get_word_info()

        _translate = QCoreApplication.translate
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", word))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", info[0][0]))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", info[0][1]))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", info[1]))


if __name__ == "__main__":
    # GUI setup
    app = QApplication(sys.argv)
    recite_gui = ReciteGUI()
    recite_gui.show()
    sys.exit(app.exec_())
