import os
import sys
import random
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import uic
from origin import check_answer as ca
from origin import create_task as ct


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('./hit_and_blow.ui')
form_class = uic.loadUiType(form)[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.digit = 4
        self.max_number = 10
        self.try_count = 0
        self.answer = []
        self.task = []
        self.cursor = 0
        self.image_path = './resource/image/'
        self.image_list = []
        self.log = ""
        self.round = 0
        for i in range(0, self.max_number):
            self.image_list.append(self.image_path + "spade_" + str((i + 1)) + ".png")
        self.arrow_down.setPixmap(QtGui.QPixmap(resource_path(self.image_path + "arrow_down.png")))
        self.btn_try.clicked.connect(self.button_try_clicked)
        self.init_game()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_W or e.key() == Qt.Key_Up or e.key() == Qt.Key_8:
            self.answer[self.cursor] = (self.answer[self.cursor] + 1) % self.max_number
        elif e.key() == Qt.Key_A or e.key() == Qt.Key_Left or e.key() == Qt.Key_4:
            if self.cursor == 0:
                self.cursor = self.digit - 1
            else:
                self.cursor -= 1
        elif e.key() == Qt.Key_S or e.key() == Qt.Key_Down or e.key() == Qt.Key_2:
            if self.answer[self.cursor] == 0:
                self.answer[self.cursor] = self.max_number - 1
            else:
                self.answer[self.cursor] -= 1
        elif e.key() == Qt.Key_D or e.key() == Qt.Key_Right or e.key() == Qt.Key_6:
            self.cursor = (self.cursor + 1) % self.digit
        elif e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.button_try_clicked()
        self.render()

    def write_log(self, content, title=""):
        if title == "":
            self.log += f"{content}\n"
        else:
            QMessageBox.about(self, title, content)
            self.log += f"[{title}] {content}\n"

    def button_try_clicked(self):
        self.try_count -= 1
        result_dict = ca.check_answer(self.answer, self.task)
        if result_dict['hit'] == self.digit:
            QMessageBox.about(self, 'Success!', "Success! Restart Game.")
            self.init_game()
            return
        else:
            temp_answer = [i + 1 for i in self.answer]
            self.write_log(f"[round {self.round + 1}] {temp_answer}: {result_dict}", "Result")
            if self.try_count <= 0:
                temp_task = [i + 1 for i in self.task]
                QMessageBox.about(self, 'Game Over', f"Game Over. Goal was {temp_task}. Restart Game.")
                self.init_game()
                return
        self.render()
        self.round += 1

    def render(self):
        self.digit_0.setPixmap(QtGui.QPixmap(resource_path(self.image_list[self.answer[0]])))
        self.digit_1.setPixmap(QtGui.QPixmap(resource_path(self.image_list[self.answer[1]])))
        self.digit_2.setPixmap(QtGui.QPixmap(resource_path(self.image_list[self.answer[2]])))
        self.digit_3.setPixmap(QtGui.QPixmap(resource_path(self.image_list[self.answer[3]])))
        base_pos_x = 60
        interval_pos = 150
        base_pos_y = -10
        self.arrow_down.move(base_pos_x + (interval_pos * self.cursor), base_pos_y)
        self.txt_log.setText(self.log)
        self.txt_try_count.setText(f"{self.try_count}")
        if self.try_count <= 3:
            self.txt_try_count.setStyleSheet("Color : red")
        else:
            self.txt_try_count.setStyleSheet("Color : black")

    def init_game(self):
        self.task = ct.create_task(self.max_number, self.digit)
        self.try_count = 10
        self.answer = [i for i in range(self.digit)]
        self.cursor = 0
        self.round = 0
        self.log = ""
        self.render()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
