import json

def json_to_dict(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

def remove_third_key_value(data):
    new_data = []
    temp_dict = {}
    for item in data:
        for key, value in item.items():
            if key == '단어':
                temp_dict[value] = None
            elif key == '뜻':
                temp_dict[list(temp_dict.keys())[0]] = value
                new_data.append(temp_dict)
                temp_dict = {}
    return new_data

def dict_to_python_file(output_file, data_list):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("words = ")
        json.dump(data_list, f, ensure_ascii=False, indent=4)

input_file_path = 'db/output_json.json'
output_file_path = 'db/wordDB.py'

data_dict = json_to_dict(input_file_path)
new_data_list = remove_third_key_value(data_dict)
dict_to_python_file(output_file_path, new_data_list)

