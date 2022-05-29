import random


class HitBlowManager:
    def __init__(self):
        self.__max_number: int = 0
        self.__digit: int = 0
        self.__max_color: int = 0
        self.__task: dict[str, list[int]] = {}
        self.__key_color: str = "c"
        self.__key_number: str = "n"
        self.__can_duplicate: bool = False

    def init_game(self, number: int, digit: int, color: int = 1, can_duplicate: bool = False):
        self.__max_number = number
        self.__digit = digit
        self.__max_color = color
        self.__can_duplicate = can_duplicate
        self.__task = self.create_task()

    def check_answer(self, user_data: dict[str, list[int]]) -> dict[str, int]:
        result = {"hit": 0, "blow": 0}
        hit = 0
        blow = 0
        for i in range(len(user_data[self.__key_number])):
            is_number_correct = user_data[self.__key_number][i] == self.__task[self.__key_number][i]
            is_color_correct = user_data[self.__key_color][i] == self.__task[self.__key_color][i]
            # 숫자와 자리와 색깔이 일치하면 hit
            if is_number_correct and is_color_correct:
                hit += 1
            # 자리 숫자 일치 but 색깔 불일치 blow
            elif is_number_correct and not is_color_correct:
                blow += 1
            # 숫자가 존재하면 blow
            elif user_data[self.__key_number][i] in self.__task[self.__key_number]:
                blow += 1
        result.update({"hit": hit})
        result.update({"blow": blow})
        return result

    def create_task(self) -> dict[str, list[int]]:
        if self.__digit > self.__max_number:
            return {}
        color_list = [random.randrange(0, self.__max_color) for _ in range(self.__digit)]
        if self.__can_duplicate:
            number_list = [random.randrange(0, self.__max_number) for _ in range(self.__digit)]
        else:
            temp = [i for i in range(0, self.__max_number)]
            random.shuffle(temp)
            number_list = temp[0:self.__digit]
        result = {self.__key_color: color_list, self.__key_number: number_list}
        return result

    @property
    def key_color(self):
        return self.__key_color

    @property
    def key_number(self):
        return self.__key_number

    @property
    def digit(self):
        return self.__digit

    @property
    def max_number(self):
        return self.__max_number

    @property
    def max_color(self):
        return self.__max_color

    @property
    def task(self):
        return self.__task
