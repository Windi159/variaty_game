import random

class NumberYagu:
    def __init__(self):
        self.generate_random_num = ""
        self.strike = 0
        self.ball = 0
        self.out = 0
        self._user_input_data = ""

        self.game_start()


    def game_start(self):
        self.generate_com_num()

        for i in range(0, 9):
            self.user_input()
            self.who_is_winner()
            self.announce_winner()
            if self.check_break():
                break

            self.init_var()

    def generate_com_num(self):
        self.generate_random_num = str(random.randint(100, 999))

    def user_input(self):
        while True:
            self._user_input_data = input("숫자를 입력해주세요 (100~999) : ")  # 사용자한테 값을 받음

            if len(self._user_input_data) == 3 and self._user_input_data.isdigit() is False:
                print("다시 입력해주세요.")

            else:
                break

    def who_is_winner(self):
        for ident in range(0, 3):
            if self._user_input_data[ident] in self.generate_random_num:  # com_random_num에 user_num에 관련된 숫자가 있는지 확인
                if self.generate_random_num[ident] == self._user_input_data[ident]:  # 숫자와 자릿수가 확인
                    self.strike += 1

                else:
                    self.ball += 1

            else:  # 숫자와 자릿수가 다를 때
                self.out += 1


    def announce_winner(self):
        print(f"{self.strike} 스트라이크 {self.ball} 볼 {self.out} 아웃")

        if self.strike == 3:  # 맞췄을 때
            print("숫자를 맞춘걸 축하해요.\n")

        elif self.strike < 3 and self.out != 3:  # 완전히 틀리지 않았을 때
            print("아쉬워요, 다시 한 번 해봐요.\n")

        else:   # 완전히 틀렸을 때
            print("틀렸어요, 다시 한 번 해봐요.\n")


    def check_break(self):
        return self.strike == 3

    def init_var(self):
        self.strike, self.ball, self.out = 0, 0, 0  # 초기화


if __name__ == '__main__':
    yagu = NumberYagu()