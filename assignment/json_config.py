import json


# 파일 경로(문자열)와 설정(딕셔너리)을 입력받아서
# 해당 경로에 JSON 파일의 형식으로 파일 write를 하는 함수
# JSON이란? https://m.blog.naver.com/demonic3540/221277604043
# 파이썬에서의 JSON 입출력 https://devpouch.tistory.com/33
# 설정이 {"digit": 4, "color": 6, "tryCount": 8} 와 같은 딕셔너리일 경우
# 파일의 내용은 아래와 같이 생성되어야 한다.
#   {
#       "latestConfig": {
#           "digit": 4,
#           "color": 6,
#           "tryCount": 8,
#       }
#   }
# 결과 확인 시 메모장 등으로 파일을 열 수 있다.
# 함수의 끝에서 파일 닫는 것을 잊지 말자.
def set_config(config_path, config):
    # 코드 작성


# 파일 경로(문자열)을 입력받아서
# 그 파일의 digit, color, tryCount의 값을 가져와
# 딕셔너리로 구성하여 리턴하는 함수
# 대상 파일은 JSON 형식의 파일
# 대상 파일의 데이터 구조는 아래와 같다.
#   {
#       "latestConfig": {
#           "digit": 4,
#           "color": 6,
#           "tryCount": 8,
#       }
#   }
# 예상 출력은 {'digit': 4, 'color': 6, 'tryCount': 8}
# 함수의 끝에서 파일 닫는 것을 잊지 말자.
def get_config(config_path):
    # 코드 작성


if __name__ == "__main__":
    path = "./config.json"
    set_config(path, {"digit": 4, "color": 6, "tryCount": 8})
    print(get_config(path))
