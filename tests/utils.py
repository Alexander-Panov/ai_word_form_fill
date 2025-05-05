import json

TEST_DATA_DIR = "../examples/tests/"

def load_file_data(filename: str) -> str:
    input_path = TEST_DATA_DIR + filename

    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = f.read()

    return input_data

def load_json_data(filename) -> dict:
    input_path = TEST_DATA_DIR + filename

    # Загрузка входного JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    return input_data