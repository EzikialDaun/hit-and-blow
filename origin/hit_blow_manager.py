import random


class HitBlowManager:
    def __init__(self):
        self.max_number = 0
        self.digit = 0
        self.max_color = 0
        self.task = []
        self.key_color = "color"
        self.key_number = "number"

    def init_game(self, number, digit, color):
        self.max_number = number
        self.digit = digit
        self.max_color = color
        self.task = self.create_task()

    def check_answer(self, user_data):
        result = {"hit": 0, "blow": 0}
        hit = 0
        blow = 0
        for i in range(len(user_data[self.key_number])):
            is_number_correct = user_data[self.key_number][i] == self.task[self.key_number][i]
            is_color_correct = user_data[self.key_color][i] == self.task[self.key_color][i]
            # 숫자와 자리와 색깔이 일치하면 hit
            if is_number_correct and is_color_correct:
                hit += 1
            # 자리와 숫자가 일치하거나 숫자만 일치하면
            elif user_data[self.key_number][i] in self.task[self.key_number]:
                blow += 1
        result.update({"hit": hit})
        result.update({"blow": blow})
        return result

    def create_task(self):
        temp = [i for i in range(0, self.max_number)]
        random.shuffle(temp)
        color_list = [random.randrange(0, self.max_color) for _ in range(self.digit)]
        number_list = temp[0:self.digit]
        result = {self.key_color: color_list, self.key_number: number_list}
        return result
