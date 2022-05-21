import pygame.mixer
import random


# 파일 경로를 입력받아
# 확장자를 제외한 파일 이름 리턴
def minimize_file_name(file_name, has_extension=False, separator="/"):
    split_list = file_name.split(separator)
    result = split_list[len(split_list) - 1]
    if not has_extension:
        result = result.split(".")[0]
    return result


class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()
        # 원본 플레이리스트
        # 셔플 모드 여부와 상관없이 순서 유지
        self.playlist = []
        # 실제 재생용 플레이 리스트(원본 플레이리스트의 사본)
        # 셔플 모드에 의해 순서 임의로 바뀔 수 있음
        # 실제 재생은 이 리스트 참조
        self.temp_list = []
        # 현재 재생 곡 정보(이름)
        self.current_song = ""
        # 반복 재생 모드 플래그
        # True: 곡 재생이 모두 끝나면 계속해서 다시 곡을 재생
        self.is_continuous = False
        # 곡 셔플 모드 플래그
        # True: 재생용 플레이리스트를 랜덤으로 셔플
        self.is_shuffle = False
        # 본 플레이리스트의 활성화 상태 여부를 나타냄
        self.is_active = False
        # 본 플레이리스트의 곡 재생 여부를 나타냄
        self.is_busy = False
        # 곡 재생 인덱싱용 커서
        self.cursor = 0
        init_volume = 0.1
        # 곡 볼륨
        self.volume = init_volume
        pygame.mixer.music.set_volume(self.volume)
        # 페이드아웃 소요 시간
        self.fadeout_wait = 1000

    # 플레이리스트 전체 초기화
    def init_playlist(self):
        pygame.mixer.music.fadeout(self.fadeout_wait)
        self.playlist = []
        self.temp_list = []
        self.current_song = ""
        self.is_active = False
        self.is_busy = False
        self.cursor = 0

    # 플레이리스트 부분 초기화
    # 커서 원점 복귀
    # 원본 플레이리스트로부터 실제 재생용 플레이리스트 복사
    # 셔플 옵션 활성화 시 재생용 플레이리스트 셔플
    def playlist_copy(self):
        self.cursor = 0
        self.temp_list = self.playlist.copy()
        if self.is_shuffle:
            random.shuffle(self.temp_list)

    # 비활성화와 곡 정보 초기화를 같이 진행하는 함수
    # 재생이 완전히 멈췄을 경우 사용
    def deactivate_playlist(self):
        self.is_active = False
        self.current_song = ""

    # 음악 파일이 있는 절대경로를 입력받아
    # 플레이리스트에 추가하는 함수
    def add_playlist(self, abs_path):
        # 파일이 이미 플레이리스트에 하면 추가하지 않음
        if abs_path not in self.playlist:
            self.playlist.append(abs_path)
            self.temp_list.append(abs_path)

    # 파일 로드하고 재생하는 함수
    def load_and_play(self):
        # 재생용 리스트의 길이가 0보다 클 때
        if len(self.temp_list) > 0:
            # 재생용 리스트의 커서 인덱스에 해당하는 파일을 재생곡으로 지정
            self.current_song = self.temp_list[self.cursor]
            try:
                pygame.mixer.music.unpause()
                # 현재 재생곡을 로드
                pygame.mixer.music.load(self.current_song)
                # 로드된 파일을 재생
                pygame.mixer.music.play()
            # 파일이 경로에 없을 때
            except pygame.error:
                # 초기화
                self.init_playlist()
                print("파일 로드 오류.")

    # 플레이리스트 시작 메서드
    def play(self):
        # 기존 곡 페이드아웃
        pygame.mixer.music.fadeout(self.fadeout_wait)
        # 원본 플레이리스트의 길이가 0보다 크면
        if len(self.playlist) > 0:
            # 재생용 플레이리스트 만들기
            self.playlist_copy()
            # 재생 시작
            self.load_and_play()
            # 플레이리스트 활성화
            self.is_active = True
        # 원본 플레이리스트의 길이가 0 이하이면
        else:
            self.deactivate_playlist()

    # 다음 곡 재생
    def queue_song(self):
        # 재생용 리스트의 길이 구하기
        len_temp_list = len(self.temp_list)
        # 재생용 리스트의 길이가 0보다 크면
        if len_temp_list > 0:
            # 커서 증가
            self.cursor += 1
            # 증가한 커서가 리스트의 길이를 초과하지 않는다면
            # (인덱싱 범위를 벗어나지 않는, 보통의 경우)
            if self.cursor < len_temp_list:
                # 로드, 재생
                self.load_and_play()
            # 증가한 커서가 리스트의 길이 이상일 경우, 그리고 반복 재생 옵션이 활성화인 경우
            # (인덱싱 범위를 벗어나는, 곡을 전부 재생한 경우)
            elif self.cursor >= len_temp_list and self.is_continuous:
                # 플레이리스트 부분 초기화
                self.playlist_copy()
                # 로드, 재생
                self.load_and_play()
            # 증가한 커서가 리스트의 길이 이상일 경우, 그리고 반복 재생 옵션이 비활성화인 경우
            # (인덱싱 범위를 벗어나는, 곡을 전부 재생한 경우)
            else:
                self.deactivate_playlist()
        #
        else:
            self.deactivate_playlist()

    # 이전 곡으로 커서 옮기는 함수
    def prev_song(self):
        # 현재 곡 페이드아웃
        pygame.mixer.music.fadeout(self.fadeout_wait)
        # 비활성 상태 상태에서 해당 함수를 동작시키는 경우를 고려하여
        # 플레이리스트 활성화
        self.is_active = True
        # 커서가 0이면 맨 끝 파일로 커서 옮김
        if self.cursor <= 0:
            self.cursor = len(self.temp_list) - 1
        # 보통의 경우에는 커서 1 감소
        else:
            self.cursor -= 1
        # 로드, 재생
        self.load_and_play()

    # 다음 곡으로 커서 옮기는 함수
    def next_song(self):
        # 현재 곡 페이드아웃
        pygame.mixer.music.fadeout(self.fadeout_wait)
        # 비활성 상태 상태에서 해당 함수를 동작시키는 경우를 고려하여
        # 플레이리스트 활성화
        self.is_active = True
        # 현재 커서가 리스트의 끝일 경우
        if self.cursor >= len(self.temp_list) - 1:
            # 처음 곡으로 커서 옮김
            self.cursor = 0
        # 보통의 경우에는 커서 1 증가
        else:
            self.cursor += 1
        # 로드, 재생
        self.load_and_play()

    # 일시정지
    def pause(self):
        # 플레이리스트 비활성화
        self.is_active = False
        # 곡 일시정지
        pygame.mixer.music.pause()

    # 곡 재개
    def unpause(self):
        # 플레이리스트 활성화
        self.is_active = True
        # 곡 재개
        pygame.mixer.music.unpause()

    # 플레이리스트 정지
    def stop(self):
        self.deactivate_playlist()
        # 곡 정지
        pygame.mixer.music.stop()

    # 현재 재생 모듈이 곡을 재생 중인지 확인하는 함수
    def get_busy(self):
        self.is_busy = pygame.mixer.music.get_busy()
        return self.is_busy

    # 볼륨 설정 함수
    # volume: 양의 실수(0.0 ~ 1.0)
    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)
