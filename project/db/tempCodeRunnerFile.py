import json

# JSON 파일을 딕셔너리로 변환하는 함수
def json_to_dict(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

# 딕셔너리를 JSON 파일로 저장하는 함수
def dict_to_json(output_file, data_dict):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

# 이상치 제거 함수
def remove_third_key_value(data):
    for item in data:
        del item["Unnamed: 2"]

# 딕셔너리 리스트의 구조 변경 함수
def convert_dictionary_list(dictionary_list):
    new_dictionary_list = []
    for dictionary in dictionary_list:
        for key, value in dictionary.items():
            new_dictionary_list.append({key: value})
    return new_dictionary_list

# 입력 파일 경로와 출력 파일 경로
input_file_path = 'db/output_json.json'
output_file_path = 'db/wordDB.py'

# JSON 파일을 딕셔너리로 변환
data_dict = json_to_dict(input_file_path)

# 이상치 삭제
remove_third_key_value(data_dict)

# 딕셔너리 리스트의 구조 변경
new_data_dict = convert_dictionary_list(data_dict)

# words 리스트 생성
words = [new_data_dict[i] for i in range(len(new_data_dict))]

# 파일에 words 리스트를 정의하는 문자열 작성
output_string = "words = " + json.dumps(words, ensure_ascii=False, indent=4)

# 문자열을 파일로 저장
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(output_string)
