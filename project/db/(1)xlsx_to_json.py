import pandas as pd

def xlsx_to_json(file_path, output_file):
    # XLSX 파일을 DataFrame으로 읽기
    # pd.read_excel('경로/파일명/xlsx')
    # engine='openpyxl': 필수
    df = pd.read_excel(file_path, engine='openpyxl')

    # JSON으로 변환
    # orient : JSON string format을 결정하는 방향
    # orient='records'
    # :한 행에 대해, {columns:value} 형태의 딕셔너리를 요소로 하는 리스트 형태
    json_data = df.to_json(orient='records')

    # JSON 데이터를 파일로 저장
    # python에서 파일을 열고 JSON 데이터를 쓰는 작업
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_data)

# 예시 파일 경로와 출력 파일 경로
input_file_path = 'db/단어장 파일.xlsx'
output_file_path = 'db/output_json.json'

# XLSX 파일을 JSON으로 변환하여 파일로 저장
xlsx_to_json(input_file_path, output_file_path)
