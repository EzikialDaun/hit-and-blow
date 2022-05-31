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
        user_number_list = user_data[self.__key_number]
        task_number_list = self.__task[self.__key_number]
        dict_by_user_number = {}
        for num in set(user_number_list):
            index_list = [i for i, val in enumerate(user_number_list) if val == num]
            if len(index_list) > 0:
                dict_by_user_number[str(num)] = index_list
        for key, value in dict_by_user_number.items():
            int_key = int(key)
            if int_key in task_number_list:
                task_index = task_number_list.index(int_key)
                is_number_correct = task_index in value
                is_color_correct = user_data[self.__key_color][task_index] == self.__task[self.__key_color][task_index]
                if is_number_correct and is_color_correct:
                    hit += 1
                elif is_number_correct and not is_color_correct:
                    blow += 1
                else:
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
