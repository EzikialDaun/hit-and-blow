import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import uic
from origin import check_answer
from origin import create_task

form_class = uic.loadUiType("./hit_and_blow.ui")[0]

image_path = "./resource/image/"
max_digit = 4
max_number = 10
answer_list = [0, 0, 0, 0]
image_list = []
task = create_task.create_task(max_number, max_digit)
for i in range(0, max_number):
    image_list.append(image_path + "spade_" + str((i + 1)) + ".png")


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_cursor = 0
        self.arrow_down.setPixmap(QtGui.QPixmap(image_path + "arrow_down.png"))
        self.btn_try.clicked.connect(self.button_try_clicked)
        self.render()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_W:
            answer_list[self.current_cursor] = (answer_list[self.current_cursor] + 1) % max_number
        elif e.key() == Qt.Key_A:
            if self.current_cursor == 0:
                self.current_cursor = max_digit - 1
            else:
                self.current_cursor -= 1
        elif e.key() == Qt.Key_S:
            if answer_list[self.current_cursor] == 0:
                answer_list[self.current_cursor] = max_number - 1
            else:
                answer_list[self.current_cursor] -= 1
        elif e.key() == Qt.Key_D:
            self.current_cursor = (self.current_cursor + 1) % max_digit
        self.render()

    def button_try_clicked(self):
        result_dict = check_answer.check_answer(answer_list, task)
        print(result_dict)
        QMessageBox.about(self, 'Result', 'Hit: ' + str(result_dict['hit']) + ', Blow: ' + str(result_dict['blow']))

    def render(self):
        self.digit_0.setPixmap(QtGui.QPixmap(image_list[answer_list[0]]))
        self.digit_1.setPixmap(QtGui.QPixmap(image_list[answer_list[1]]))
        self.digit_2.setPixmap(QtGui.QPixmap(image_list[answer_list[2]]))
        self.digit_3.setPixmap(QtGui.QPixmap(image_list[answer_list[3]]))
        self.arrow_down.move(110 + (200 * self.current_cursor), 20)


# 본 파일에서 실행되었을 때 동작
# 다른 파일에서 import하여 실행했을 때에는 동작하지 않음.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
