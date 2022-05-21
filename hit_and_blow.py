import json
import os
import sys

import PyQt5
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5 import uic
from origin import hit_blow_manager as hbm
from origin import sound_player as sp
from origin import json_config as jc


# 배포 시 리소스 참조 오류 방지하기 위한 함수
# 상대경로를 입력받아서
# 절대경로를 리턴하는 함수
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# UI 파일 로드
form = resource_path('./hit_and_blow.ui')
form_class = uic.loadUiType(form)[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 게임 매니저
        self.game_manager = hbm.HitBlowManager()
        # 시도 횟수
        self.try_count = 0
        # 유저 답안
        self.answer = []
        # 카드 커서
        self.cursor = 0
        # 로그
        self.log = ""
        # 현재 라운드 횟수
        self.round = 0
        # 카드 파일 자동화를 위한 변수들
        self.card_suit = ["spade", "heart", "diamond", "club"]
        self.card_symbol = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        image_path = './resource/image/'
        self.image_list = [["" for _ in range(len(self.card_symbol))] for _ in range(len(self.card_suit))]
        for suit in range(len(self.card_suit)):
            for num in range(len(self.card_symbol)):
                self.image_list[suit][num] = f"{image_path}{self.card_suit[suit]}_{num + 1}.png"
        # 카드 커서 이미지 지정
        self.arrow_down.setPixmap(QtGui.QPixmap(resource_path(f"{image_path}arrow_down.png")))
        # 위젯 이벤트 연결
        self.btn_try.clicked.connect(self.btn_try_clicked)
        self.btn_new_game.clicked.connect(self.btn_new_game_clicked)
        self.btn_browse.clicked.connect(self.btn_browse_clicked)
        self.btn_play.clicked.connect(self.btn_play_clicked)
        self.btn_prev.clicked.connect(self.btn_prev_clicked)
        self.btn_next.clicked.connect(self.btn_next_clicked)
        self.btn_clear.clicked.connect(self.btn_clear_clicked)
        self.btn_pause.clicked.connect(self.btn_pause_clicked)
        self.btn_resume.clicked.connect(self.btn_resume_clicked)
        self.btn_stop.clicked.connect(self.btn_stop_clicked)
        self.slider_volume.valueChanged.connect(self.slider_volume_changed)
        self.chk_continuous.stateChanged.connect(self.chk_continuous_changed)
        self.chk_shuffle.stateChanged.connect(self.chk_shuffle_changed)
        # 타이머
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.event_loop)
        # 사운드 플레이어 초기화
        self.sound_player = sp.SoundPlayer()
        try:
            latest_playlist = jc.get_playlist_config("./hb_config.json")
        except FileNotFoundError:
            latest_playlist = []
        except json.decoder.JSONDecodeError:
            latest_playlist = []
        if len(latest_playlist):
            for music in latest_playlist:
                self.sound_player.add_playlist(music)
        # 게임 초기화
        self.init_game()

    # 이벤트 루프. 1초마다 실행
    def event_loop(self):
        if not self.sound_player.get_busy() and self.sound_player.is_active:
            self.sound_player.queue_song()
        self.render_ui()

    # 유저 답안 또는 문제의 데이터 형식을 입력받아
    # 사용자가 알아보기 쉽게 포맷팅해주고 리턴하는 함수
    def reduce_answer(self, answer):
        result = [self.card_suit[answer[self.game_manager.key_color][i]][0].upper() + self.card_symbol[
            answer[self.game_manager.key_number][i]]
                  for i in range(self.game_manager.digit)]
        return result

    # 키 입력 이벤트
    def keyPressEvent(self, e):
        # 'W', 방향키 위, 숫자 패드 8
        # 카드 인덱스 증가
        if e.key() == Qt.Key_W or e.key() == Qt.Key_Up or e.key() == Qt.Key_8:
            self.answer[self.game_manager.key_number][self.cursor] = \
                (self.answer[self.game_manager.key_number][self.cursor] + 1) % self.game_manager.max_number
        # 'A', 방향키 왼쪽, 숫자 패드 4
        # 카드 커서 감소
        elif e.key() == Qt.Key_A or e.key() == Qt.Key_Left or e.key() == Qt.Key_4:
            if self.cursor == 0:
                self.cursor = self.game_manager.digit - 1
            else:
                self.cursor -= 1
        # 'S', 방향키 아래, 숫자 패드 2
        # 카드 인덱스 감소
        elif e.key() == Qt.Key_S or e.key() == Qt.Key_Down or e.key() == Qt.Key_2:
            if self.answer[self.game_manager.key_number][self.cursor] == 0:
                self.answer[self.game_manager.key_number][self.cursor] = self.game_manager.max_number - 1
            else:
                self.answer[self.game_manager.key_number][self.cursor] -= 1
        # 'D', 방향키 오른쪽, 숫자패드 6
        # 카드 커서 증가
        elif e.key() == Qt.Key_D or e.key() == Qt.Key_Right or e.key() == Qt.Key_6:
            self.cursor = (self.cursor + 1) % self.game_manager.digit
        # 엔터 키
        # 정답 체크
        elif e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.btn_try_clicked()
        # 'F'
        # 카드 색 바꾸기
        elif e.key() == Qt.Key_F:
            self.answer[self.game_manager.key_color][self.cursor] = (self.answer[self.game_manager.key_color][
                                                                         self.cursor] + 1) % self.game_manager.max_color
        # 렌더링
        self.render_ui()

    # 로그 쓰기
    # 타이틀이 지정될 경우 팝업 메세지도 표시
    def write_log(self, content, title=""):
        if title == "":
            self.log += f"{content}\n"
        else:
            QMessageBox.about(self, title, content)
            self.log += f"[{title}] {content}\n"

    def slider_volume_changed(self):
        volume = float(self.slider_volume.value() / 100)
        self.sound_player.set_volume(volume)

    def btn_play_clicked(self):
        self.sound_player.play()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()

    def btn_pause_clicked(self):
        self.sound_player.pause()
        self.btn_play.hide()
        self.btn_pause.hide()
        self.btn_resume.show()

    def btn_resume_clicked(self):
        self.sound_player.unpause()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()

    def btn_stop_clicked(self):
        self.sound_player.stop()
        self.btn_play.show()
        self.btn_pause.hide()
        self.btn_resume.hide()

    def btn_prev_clicked(self):
        self.sound_player.prev_song()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()

    def btn_next_clicked(self):
        self.sound_player.next_song()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()

    def btn_clear_clicked(self):
        reply = QMessageBox.question(self, 'Warning',
                                     'The playlist will be reset. Do you want to continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sound_player.init_playlist()
            jc.set_playlist_config("./hb_config.json", self.sound_player.playlist)
            self.btn_play.show()
            self.btn_pause.hide()
            self.btn_resume.hide()

    def chk_continuous_changed(self, state):
        result = False
        if state == Qt.Checked:
            result = True
        elif state == Qt.Unchecked:
            result = False
        self.sound_player.is_continuous = result

    def chk_shuffle_changed(self, state):
        result = False
        if state == Qt.Checked:
            result = True
        elif state == Qt.Unchecked:
            result = False
        self.sound_player.is_shuffle = result

    # 답안 확인 버튼 클릭 시
    def btn_try_clicked(self):
        # 시도 가능 횟수 차감
        self.try_count -= 1
        # 라운드 수 증가
        self.round += 1
        # 사용자의 답안과 문제를 비교
        result_dict = self.game_manager.check_answer(self.answer)
        # 4 hit면 성공
        if result_dict['hit'] == self.game_manager.digit:
            QMessageBox.about(self, 'Success!', "Success! Restart Game.")
            self.init_game()
            # 이미 init_game에 렌더링 함수가 있어서
            # 렌더링 피하기 위해 리턴
            return
        else:
            # 현재 라운드, 사용자가 어떤 답을 입력했는지, 비교 결과 등을 로그에 출력
            self.write_log(
                f"[round {self.round}] "
                f"{self.reduce_answer(self.answer)} "
                f"{result_dict}",
                "Result")
            # 시도 횟수가 없으면
            if self.try_count <= 0:
                # 게임 종료
                QMessageBox.about(self, 'Game Over',
                                  f"Game Over. Goal was {self.reduce_answer(self.game_manager.task)}. Restart Game.")
                self.init_game()
                # 이미 init_game에 렌더링 함수가 있어서
                # 렌더링 피하기 위해 리턴
                return
        self.render_ui()

    # 새 게임 버튼 클릭 시
    def btn_new_game_clicked(self):
        reply = QMessageBox.question(self, 'Warning',
                                     'The progress of the current game will be reset. Do you want to continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.about(self, 'New Game', "Config applied.")
            self.init_game()

    def btn_browse_clicked(self):
        path_list = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Music File", ".", "wav(*.wav);;mp3(*.mp3)")[0]
        for music_path in path_list:
            self.sound_player.add_playlist(music_path)
        jc.set_playlist_config("./hb_config.json", self.sound_player.playlist)
        self.render_ui()

    # 렌더링 함수
    def render_ui(self):
        # 현재 유저가 제시한 답안을 카드로 렌더링
        self.digit_0.setPixmap(
            QtGui.QPixmap(
                resource_path(self.image_list[self.answer[self.game_manager.key_color][0]][
                                  self.answer[self.game_manager.key_number][0]])))
        self.digit_1.setPixmap(
            QtGui.QPixmap(
                resource_path(self.image_list[self.answer[self.game_manager.key_color][1]][
                                  self.answer[self.game_manager.key_number][1]])))
        self.digit_2.setPixmap(
            QtGui.QPixmap(
                resource_path(self.image_list[self.answer[self.game_manager.key_color][2]][
                                  self.answer[self.game_manager.key_number][2]])))
        self.digit_3.setPixmap(
            QtGui.QPixmap(
                resource_path(self.image_list[self.answer[self.game_manager.key_color][3]][
                                  self.answer[self.game_manager.key_number][3]])))
        # 현재 유저가 어떤 카드를 조작하는지 나타내는 커서 화살표
        # 좌표 정보
        base_pos_x = 60
        interval_pos = 150
        base_pos_y = -10
        self.arrow_down.move(base_pos_x + (interval_pos * self.cursor), base_pos_y)
        # 로그 표시
        self.txt_log.setText(self.log)
        # 플레이리스트 표시
        str_playlist = ""
        for music in self.sound_player.temp_list:
            str_playlist += f"{sp.minimize_file_name(music)}\n"
        self.txt_playlist.setText(str_playlist)
        # 현재 재생 곡 표시
        self.txt_current_song.setText(sp.minimize_file_name(self.sound_player.current_song))
        # 남은 기회 표시
        self.txt_try_count.setText(f"{self.try_count}")
        # 남은 기회가 3회 이하면 빨간색 글씨로 강조
        if self.try_count <= 3:
            self.txt_try_count.setStyleSheet("Color : red")
        else:
            self.txt_try_count.setStyleSheet("Color : black")

    # 게임 초기화
    def init_game(self):
        # 카드 확장(J, Q, K) 여부 설정
        is_extra_deck = self.chk_extra_deck.isChecked()
        if is_extra_deck:
            max_number = 13
        else:
            max_number = 10
        # 카드 슈트(문양) 수 설정
        max_color = self.spin_max_color.value()
        # 시도 횟수 설정
        self.try_count = self.spin_max_try_count.value()
        # 게임 매니저 초기화
        max_digit = 4
        self.game_manager.init_game(max_number, max_digit, max_color)
        # 답안 초기화
        self.answer = {self.game_manager.key_color: [0 for _ in range(self.game_manager.digit)],
                       self.game_manager.key_number: [i for i in range(self.game_manager.digit)]}
        # 커서 초기화
        self.cursor = 0
        # 라운드 수 초기화
        self.round = 0
        # 로그 초기화
        self.log = ""
        # 렌더링
        self.render_ui()


# 이 파일이 메인 파일일 경우에 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
