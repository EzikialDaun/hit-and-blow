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
        self.__playlist: list[str] = []
        # 실제 재생용 플레이 리스트(원본 플레이리스트의 사본)
        # 셔플 모드에 의해 순서 임의로 바뀔 수 있음
        # 실제 재생은 이 리스트 참조
        self.__temp_list: list[str] = []
        # 현재 재생 곡 정보(이름)
        self.__current_song: str = ""
        # 반복 재생 모드 플래그
        # True: 곡 재생이 모두 끝나면 계속해서 다시 곡을 재생
        self.__is_continuous: bool = False
        # 곡 셔플 모드 플래그
        # True: 재생용 플레이리스트를 랜덤으로 셔플
        self.__is_shuffle: bool = False
        # 본 플레이리스트의 활성화 상태 여부를 나타냄
        self.__is_active: bool = False
        # 본 플레이리스트의 곡 재생 여부를 나타냄
        self.__is_busy: bool = False
        # 곡 재생 인덱싱용 커서
        self.__cursor: int = 0
        # 곡 볼륨
        self.__volume: float = 0.5
        # 페이드아웃 소요 시간
        self.__fadeout_wait: int = 1000

    # 플레이리스트 전체 초기화
    def init_playlist(self):
        pygame.mixer.music.fadeout(self.__fadeout_wait)
        self.__playlist = []
        self.__temp_list = []
        self.__current_song = ""
        self.__is_active = False
        self.__is_busy = False
        self.__cursor = 0

    # 플레이리스트 부분 초기화
    # 커서 원점 복귀
    # 원본 플레이리스트로부터 실제 재생용 플레이리스트 복사
    # 셔플 옵션 활성화 시 재생용 플레이리스트 셔플
    def playlist_copy(self):
        self.__cursor = 0
        self.__temp_list = self.__playlist.copy()
        if self.__is_shuffle:
            random.shuffle(self.__temp_list)

    # 비활성화와 곡 정보 초기화를 같이 진행하는 함수
    # 재생이 완전히 멈췄을 경우 사용
    def deactivate_playlist(self):
        self.__is_active = False
        self.__current_song = ""

    # 음악 파일이 있는 절대경로를 입력받아
    # 플레이리스트에 추가하는 함수
    def add_playlist(self, abs_path):
        # 파일이 이미 플레이리스트에 하면 추가하지 않음
        if abs_path not in self.__playlist:
            self.__playlist.append(abs_path)
            self.__temp_list.append(abs_path)

    # 파일 로드하고 재생하는 함수
    def load_and_play(self):
        # 재생용 리스트의 길이가 0보다 클 때
        if len(self.__temp_list) > 0:
            # 재생용 리스트의 커서 인덱스에 해당하는 파일을 재생곡으로 지정
            self.__current_song = self.__temp_list[self.__cursor]
            try:
                pygame.mixer.music.unpause()
                # 현재 재생곡을 로드
                pygame.mixer.music.load(self.__current_song)
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
        pygame.mixer.music.fadeout(self.__fadeout_wait)
        # 원본 플레이리스트의 길이가 0보다 크면
        if len(self.__playlist) > 0:
            # 재생용 플레이리스트 만들기
            self.playlist_copy()
            # 재생 시작
            self.load_and_play()
            # 플레이리스트 활성화
            self.__is_active = True
        # 원본 플레이리스트의 길이가 0 이하이면
        else:
            self.deactivate_playlist()

    # 다음 곡 재생
    def queue_song(self):
        # 재생용 리스트의 길이 구하기
        len_temp_list = len(self.__temp_list)
        # 재생용 리스트의 길이가 0보다 크면
        if len_temp_list > 0:
            # 커서 증가
            self.__cursor += 1
            # 증가한 커서가 리스트의 길이를 초과하지 않는다면
            # (인덱싱 범위를 벗어나지 않는, 보통의 경우)
            if self.__cursor < len_temp_list:
                # 로드, 재생
                self.load_and_play()
            # 증가한 커서가 리스트의 길이 이상일 경우, 그리고 반복 재생 옵션이 활성화인 경우
            # (인덱싱 범위를 벗어나는, 곡을 전부 재생한 경우)
            elif self.__cursor >= len_temp_list and self.is_continuous:
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
        pygame.mixer.music.fadeout(self.__fadeout_wait)
        # 비활성 상태 상태에서 해당 함수를 동작시키는 경우를 고려하여
        # 플레이리스트 활성화
        self.__is_active = True
        # 커서가 0이면 맨 끝 파일로 커서 옮김
        if self.__cursor <= 0:
            self.__cursor = len(self.__temp_list) - 1
        # 보통의 경우에는 커서 1 감소
        else:
            self.__cursor -= 1
        # 로드, 재생
        self.load_and_play()

    # 다음 곡으로 커서 옮기는 함수
    def next_song(self):
        # 현재 곡 페이드아웃
        pygame.mixer.music.fadeout(self.__fadeout_wait)
        # 비활성 상태 상태에서 해당 함수를 동작시키는 경우를 고려하여
        # 플레이리스트 활성화
        self.__is_active = True
        # 현재 커서가 리스트의 끝일 경우
        if self.__cursor >= len(self.__temp_list) - 1:
            # 처음 곡으로 커서 옮김
            self.__cursor = 0
        # 보통의 경우에는 커서 1 증가
        else:
            self.__cursor += 1
        # 로드, 재생
        self.load_and_play()

    # 일시정지
    def pause(self):
        # 플레이리스트 비활성화
        self.__is_active = False
        # 곡 일시정지
        pygame.mixer.music.pause()

    # 곡 재개
    def unpause(self):
        # 플레이리스트 활성화
        self.__is_active = True
        # 곡 재개
        pygame.mixer.music.unpause()

    # 플레이리스트 정지
    def stop(self):
        self.deactivate_playlist()
        # 곡 정지
        pygame.mixer.music.stop()

    @property
    def playlist(self):
        return self.__playlist

    @property
    def is_continuous(self) -> bool:
        return self.__is_continuous

    @is_continuous.setter
    def is_continuous(self, flag: bool):
        self.__is_continuous = flag

    @property
    def is_shuffle(self):
        return self.__is_shuffle

    @is_shuffle.setter
    def is_shuffle(self, flag: bool):
        self.__is_shuffle = flag

    @property
    def volume(self):
        return self.__volume

    # volume: 양의 실수(0.0 ~ 1.0)
    @volume.setter
    def volume(self, volume: float):
        self.__volume = volume
        pygame.mixer.music.set_volume(self.__volume)

    @property
    def temp_list(self) -> list[str]:
        return self.__temp_list

    @property
    def current_song(self) -> str:
        return self.__current_song

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def is_busy(self) -> bool:
        self.__is_busy = pygame.mixer.music.get_busy()
        return self.__is_busy
