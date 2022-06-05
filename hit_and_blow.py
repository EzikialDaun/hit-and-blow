import os
import sys

import PyQt5
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from origin import hit_blow_manager as hbm
from origin import sound_player as sp
from IMY import json_config as jc


# 배포 시 리소스 참조 오류 방지하기 위한 함수
# 상대경로를 입력받아서
# 절대경로를 리턴하는 함수
# https://devbruce.github.io/python/py-39-path+function/
# 'hit_and_blow.ui' => 'C:\\KMS\\인하대\\1학년\\1학기\\컴퓨터공학기초\\텀프\\튜토리얼\\hit-and-blow\\hit_and_blow.ui'
def resource_path(relative_path):
    # __file__                  =>  현재 실행중인 파일이 속한 디렉토리 리턴
    # os.path.abspath(__file__) =>  현재 실행중인 파일의 절대경로 리턴(어느 위치에서 실행해도 같은 값 리턴)
    # os.path.dirname(path)     =>  path의 상위 디렉토리까지 잘라서 리턴
    # py로 실행 시의 base_path    =>  C:\KMS\인하대\1학년\1학기\컴퓨터공학기초\텀프\튜토리얼\hit-and-blow (실행환경마다 다름)
    # exe로 실행 시의 base_path   =>  C:\Users\eziki\AppData\Local\Temp\_MEI18642 (실행환경마다 다름)
    # os.path.join(a, b)        =>  경로 합치기 => a/b

    # sys 객체의 _MEIPASS 속성을 base_path에 저장.
    # 만약 _MEIPASS 속성이 없으면 현재 실행중인 파일의 상위 디렉토리까지의 절대경로를 저장
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # 위에서 만든 상위 디렉토리까지의 절대경로와 입력받은 상대경로를 결합
    result = os.path.join(base_path, relative_path)
    return result


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# UI 파일 로드
form_class = uic.loadUiType(resource_path('hit_and_blow.ui'))[0]


class HitBlowWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # form_class에 속한 메서드
        # UI 셋업
        self.setupUi(self)
        # 버전 설정
        version = 1.01
        self.setWindowTitle(f"Hit & Trump v{version}")
        # 게임 매니저
        self.__game_manager: hbm.HitBlowManager = hbm.HitBlowManager()
        # 시도 횟수
        self.__try_count: int = 0
        # 유저 답안
        self.__answer: dict[str, list[int]] = {}
        # 카드 커서
        self.__cursor: int = 0
        # 로그
        self.__log: str = ""
        # 현재 라운드 횟수
        self.__round: int = 0
        # 카드 파일 자동화를 위한 변수들
        image_path: str = 'resource/image/'
        self.__card_suit: list[str] = ["spade", "heart", "diamond", "club"]
        self.__card_char: list[str] = ["♠", "♥", "◆", "♣"]
        self.__card_symbol: list[str] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.__image_list: list[list[str]] = [["" for _ in range(len(self.__card_symbol))] for _ in
                                              range(len(self.__card_suit))]
        for suit in range(len(self.__card_suit)):
            for num in range(len(self.__card_symbol)):
                self.__image_list[suit][num] = f"{image_path}{self.__card_suit[suit]}_{num + 1}.jpeg"
        # 카드 커서 이미지 지정
        self.arrow_down.setPixmap(QtGui.QPixmap(resource_path(f"{image_path}arrow_down.png")))
        self.key_a.setPixmap(QtGui.QPixmap(resource_path(f"{image_path}key_a.jpeg")))
        self.key_d.setPixmap(QtGui.QPixmap(resource_path(f"{image_path}key_d.jpeg")))
        self.key_w.setPixmap(QtGui.QPixmap(resource_path(f"{image_path}key_w.jpeg")))
        self.key_s.setPixmap(QtGui.QPixmap(resource_path(f"{image_path}key_s.jpeg")))
        self.key_f.setPixmap(QtGui.QPixmap(resource_path(f"{image_path}key_f.jpeg")))
        # 아이콘 이미지
        self.setWindowIcon(QIcon(resource_path(f"{image_path}/icon.png")))
        # 콤보박스 초기화
        self.combo_difficulty.addItem("1")
        self.combo_difficulty.addItem("2")
        self.combo_difficulty.addItem("3")
        self.combo_difficulty.addItem("4")
        self.combo_difficulty.addItem("Custom")
        # 위젯 숨기기
        self.chk_extra_deck.hide()
        self.label_try_count.hide()
        self.spin_max_try_count.hide()
        self.label_symbol.hide()
        self.spin_max_color.hide()
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
        self.spin_max_try_count.valueChanged.connect(self.spin_max_try_count_changed)
        self.spin_max_color.valueChanged.connect(self.spin_max_color_changed)
        self.chk_extra_deck.stateChanged.connect(self.chk_extra_deck_changed)
        self.slider_volume.valueChanged.connect(self.slider_volume_changed)
        self.chk_continuous.stateChanged.connect(self.chk_continuous_changed)
        self.chk_shuffle.stateChanged.connect(self.chk_shuffle_changed)
        self.combo_difficulty.currentTextChanged.connect(self.combo_difficulty_changed)
        # 타이머
        self.__timer: QTimer = QTimer(self)
        self.__timer.start(100)
        self.__timer.timeout.connect(self.event_loop)
        # 플레이리스트 설정 파일 경로
        self.__config_path = "hb_config.json"
        # 설정 키
        self.__key_playlist = 'latestPlaylist'
        self.__key_is_shuffle = 'isShuffle'
        self.__key_is_continuous = 'isContinuous'
        self.__key_volume = 'volume'
        # 사운드 플레이어 초기화
        self.__sound_player: sp.SoundPlayer = sp.SoundPlayer()
        # 설정 불러오기
        self.get_config()
        self.render_sound_player()
        # 게임 초기화
        self.init_game()

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
        self.__try_count = self.spin_max_try_count.value()
        # 게임 매니저 초기화
        max_digit = 4
        # 숫자 중복 가능 여부 설정
        self.__game_manager.init_game(max_number, max_digit, max_color)
        # 답안 초기화
        self.__answer = {self.__game_manager.key_color: [0 for _ in range(self.__game_manager.digit)],
                         self.__game_manager.key_number: [i for i in range(self.__game_manager.digit)]}
        # 커서 초기화
        self.__cursor = 0
        # 라운드 수 초기화
        self.__round = 0
        # 로그 초기화
        self.__log = ""
        # 로그 표시
        self.txt_log.setText(self.__log)
        self.label_warn_1.hide()
        self.label_warn_2.hide()

    def render_sound_player(self):
        # 플레이리스트 표시
        str_playlist = ""
        for music in self.__sound_player.temp_list:
            str_playlist += f"{sp.minimize_file_name(music)}\n"
        self.txt_playlist.setText(str_playlist)

    # 렌더링 함수
    def render_ui(self):
        # 게임 렌더링
        # 현재 유저가 제시한 답안을 카드로 렌더링
        self.digit_0.setPixmap(
            QtGui.QPixmap(
                resource_path(self.__image_list[self.__answer[self.__game_manager.key_color][0]][
                                  self.__answer[self.__game_manager.key_number][0]])))
        self.digit_1.setPixmap(
            QtGui.QPixmap(
                resource_path(self.__image_list[self.__answer[self.__game_manager.key_color][1]][
                                  self.__answer[self.__game_manager.key_number][1]])))
        self.digit_2.setPixmap(
            QtGui.QPixmap(
                resource_path(self.__image_list[self.__answer[self.__game_manager.key_color][2]][
                                  self.__answer[self.__game_manager.key_number][2]])))
        self.digit_3.setPixmap(
            QtGui.QPixmap(
                resource_path(self.__image_list[self.__answer[self.__game_manager.key_color][3]][
                                  self.__answer[self.__game_manager.key_number][3]])))
        # 현재 유저가 어떤 카드를 조작하는지 나타내는 커서 화살표
        # 좌표 정보
        base_pos_x = 60
        interval_pos = 150
        base_pos_y = -10
        self.arrow_down.move(base_pos_x + (interval_pos * self.__cursor), base_pos_y)
        # 남은 기회 표시
        self.txt_try_count.setText(f"{self.__try_count}")
        # 남은 기회가 3회 이하면 빨간색 글씨로 강조
        if self.__try_count <= 3:
            self.txt_try_count.setStyleSheet("Color : red")
        else:
            self.txt_try_count.setStyleSheet("Color : black")
        # 사운드 플레이어 렌더링
        # 현재 재생 곡 표시
        self.txt_current_song.setText(sp.minimize_file_name(self.__sound_player.current_song))
        # 셔플 여부 표시
        self.chk_shuffle.setChecked(self.__sound_player.is_shuffle)
        # 계속 재생 여부 표시
        self.chk_continuous.setChecked(self.__sound_player.is_continuous)
        # 볼륨 표시
        self.slider_volume.setValue(int(self.__sound_player.volume * 100))

    # 유저 답안 또는 문제의 데이터 형식을 입력받아
    # 사용자가 알아보기 쉽게 포맷팅해주고 리턴하는 함수
    def reduce_answer(self, answer: dict[str, list[int]]) -> list[str]:
        result = [self.__card_char[answer[self.__game_manager.key_color][i]] + self.__card_symbol[
            answer[self.__game_manager.key_number][i]]
                  for i in range(self.__game_manager.digit)]
        return result

    # 로그 쓰기
    # 타이틀이 지정될 경우 팝업 메세지도 표시
    def write_log(self, content: str, title: str = ""):
        if title == "":
            self.__log += f"{content}\n"
        else:
            QMessageBox.about(self, title, content)
            self.__log += f"[{title}] {content}\n"
        # 로그 표시
        self.txt_log.setText(self.__log)

    # 이벤트 루프. 0.1초마다 실행
    def event_loop(self):
        # 사운드 플레이어가 유휴 상태이면서 활성화 상태일 때
        if not self.__sound_player.is_busy and self.__sound_player.is_active:
            # 다음 곡 재생
            self.__sound_player.queue_song()
            self.render_sound_player()
        # UI 렌더링
        self.render_ui()

    # 키 입력 이벤트
    def keyPressEvent(self, e: PyQt5.QtGui.QKeyEvent):
        # 'W', 방향키 위, 숫자 패드 8
        # 카드 인덱스 증가
        if e.key() == Qt.Key_W or e.key() == Qt.Key_Up or e.key() == Qt.Key_8:
            self.__answer[self.__game_manager.key_number][self.__cursor] = \
                (self.__answer[self.__game_manager.key_number][self.__cursor] + 1) % self.__game_manager.max_number
        # 'A', 방향키 왼쪽, 숫자 패드 4
        # 카드 커서 감소
        elif e.key() == Qt.Key_A or e.key() == Qt.Key_Left or e.key() == Qt.Key_4:
            if self.__cursor == 0:
                self.__cursor = self.__game_manager.digit - 1
            else:
                self.__cursor -= 1
        # 'S', 방향키 아래, 숫자 패드 2
        # 카드 인덱스 감소
        elif e.key() == Qt.Key_S or e.key() == Qt.Key_Down or e.key() == Qt.Key_2:
            if self.__answer[self.__game_manager.key_number][self.__cursor] == 0:
                self.__answer[self.__game_manager.key_number][self.__cursor] = self.__game_manager.max_number - 1
            else:
                self.__answer[self.__game_manager.key_number][self.__cursor] -= 1
        # 'D', 방향키 오른쪽, 숫자패드 6
        # 카드 커서 증가
        elif e.key() == Qt.Key_D or e.key() == Qt.Key_Right or e.key() == Qt.Key_6:
            self.__cursor = (self.__cursor + 1) % self.__game_manager.digit
        # 엔터 키
        # 정답 체크
        elif e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.btn_try_clicked()
        # 'F'
        # 카드 색 바꾸기
        elif e.key() == Qt.Key_F:
            if self.__game_manager.max_color == 1:
                self.write_log("[Info] Cannot change the symbol. Currently 1 max. symbol.")
            else:
                self.__answer[self.__game_manager.key_color][self.__cursor] = \
                    (self.__answer[self.__game_manager.key_color][
                         self.__cursor] + 1) % self.__game_manager.max_color
        # 렌더링
        self.render_ui()

    def slider_volume_changed(self):
        volume: float = float(self.slider_volume.value() / 100)
        self.__sound_player.volume = volume

    def btn_play_clicked(self):
        self.__sound_player.play()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()
        self.render_sound_player()

    def btn_pause_clicked(self):
        self.__sound_player.pause()
        self.btn_play.hide()
        self.btn_pause.hide()
        self.btn_resume.show()
        self.render_sound_player()

    def btn_resume_clicked(self):
        self.__sound_player.unpause()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()
        self.render_sound_player()

    def btn_stop_clicked(self):
        self.__sound_player.stop()
        self.btn_play.show()
        self.btn_pause.hide()
        self.btn_resume.hide()
        self.render_sound_player()

    def btn_prev_clicked(self):
        self.__sound_player.prev_song()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()
        self.render_sound_player()

    def btn_next_clicked(self):
        self.__sound_player.next_song()
        self.btn_play.hide()
        self.btn_pause.show()
        self.btn_resume.hide()
        self.render_sound_player()

    def btn_clear_clicked(self):
        reply = QMessageBox.question(self, 'Warning',
                                     'The playlist will be reset. Do you want to continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.__sound_player.init_playlist()
            self.save_config()
            self.btn_play.show()
            self.btn_pause.hide()
            self.btn_resume.hide()
            self.render_sound_player()

    def chk_continuous_changed(self, state):
        result: bool = False
        if state == Qt.Checked:
            result = True
        elif state == Qt.Unchecked:
            result = False
        self.__sound_player.is_continuous = result

    def chk_shuffle_changed(self, state):
        result: bool = False
        if state == Qt.Checked:
            result = True
        elif state == Qt.Unchecked:
            result = False
        self.__sound_player.is_shuffle = result

    # 답안 확인 버튼 클릭 시
    def btn_try_clicked(self):
        # 시도 가능 횟수 차감
        self.__try_count -= 1
        # 라운드 수 증가
        self.__round += 1
        # 사용자의 답안과 문제를 비교
        result_dict = self.__game_manager.check_answer(self.__answer)
        # 4 hit면 성공
        if result_dict['hit'] == self.__game_manager.digit:
            QMessageBox.about(self, 'Success!', "Success! Restart Game.")
            self.init_game()
        else:
            # 현재 라운드, 사용자가 어떤 답을 입력했는지, 비교 결과 등을 로그에 출력
            self.write_log(
                f"[round {self.__round}] "
                f"{self.reduce_answer(self.__answer)} "
                f"{result_dict}",
                "Result")
            # 시도 횟수가 없으면
            if self.__try_count <= 0:
                # 게임 종료
                QMessageBox.about(self, 'Game Over',
                                  f"Game Over. Goal was {self.reduce_answer(self.__game_manager.task)}. Restart Game.")
                self.init_game()

    # 새 게임 버튼 클릭 시
    def btn_new_game_clicked(self):
        reply = QMessageBox.question(self, 'Warning',
                                     'The progress of the current game will be reset. Do you want to continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.about(self, 'New Game', "Config applied.")
            self.init_game()

    def btn_browse_clicked(self):
        path_list = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Music File", ".", "mp3(*.mp3);;wav(*.wav)")[0]
        for music_path in path_list:
            self.__sound_player.add_playlist(music_path)
        self.save_config()
        self.render_sound_player()

    def setting_changed(self):
        self.label_warn_1.show()
        self.label_warn_2.show()

    def combo_difficulty_changed(self, value):
        self.setting_changed()
        if value == "Custom":
            self.chk_extra_deck.show()
            self.spin_max_try_count.show()
            self.spin_max_color.show()
            self.label_symbol.show()
            self.label_try_count.show()
        else:
            self.chk_extra_deck.hide()
            self.spin_max_try_count.hide()
            self.spin_max_color.hide()
            self.label_symbol.hide()
            self.label_try_count.hide()
            self.chk_extra_deck.setChecked(False)
            self.spin_max_try_count.setValue(10)
            if value == "1":
                self.spin_max_color.setValue(1)
            elif value == "2":
                self.spin_max_color.setValue(2)
            elif value == "3":
                self.spin_max_color.setValue(3)
            elif value == "4":
                self.spin_max_color.setValue(4)

    def spin_max_try_count_changed(self):
        self.setting_changed()

    def spin_max_color_changed(self):
        self.setting_changed()

    def chk_extra_deck_changed(self):
        self.setting_changed()

    # 설정 저장
    def save_config(self):
        config_obj = {self.__key_playlist: self.__sound_player.playlist,
                      self.__key_is_shuffle: self.__sound_player.is_shuffle,
                      self.__key_is_continuous: self.__sound_player.is_continuous,
                      self.__key_volume: self.__sound_player.volume}
        jc.set_config_rev(self.__config_path, config_obj)

    # 설정 불러오기
    def get_config(self):
        config_obj = jc.get_config_rev(self.__config_path)
        # 플레이리스트
        try:
            latest_playlist = config_obj[self.__key_playlist]
        except KeyError:
            latest_playlist = []
        if len(latest_playlist) > 0:
            for music in latest_playlist:
                self.__sound_player.add_playlist(music)
        # 셔플 여부
        try:
            is_shuffle = config_obj[self.__key_is_shuffle]
        except KeyError:
            is_shuffle = self.__sound_player.is_shuffle
        self.__sound_player.is_shuffle = is_shuffle
        # 계속 재생 여부
        try:
            is_continuous = config_obj[self.__key_is_continuous]
        except KeyError:
            is_continuous = self.__sound_player.is_continuous
        self.__sound_player.is_continuous = is_continuous
        # 볼륨
        try:
            volume = config_obj[self.__key_volume]
        except KeyError:
            volume = self.__sound_player.volume
        self.__sound_player.volume = volume

    # 프로그램 종료 시
    def closeEvent(self, e):
        self.save_config()


# 이 파일이 메인 파일일 경우에 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = HitBlowWindow()
    main_window.show()
    sys.exit(app.exec_())
