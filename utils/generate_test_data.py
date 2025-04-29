import datetime
import json
import random
from typing import Any, Union

from utils.utils import field_key_generator


def generate_random_text(max_length: int = 100) -> str:
    """Генерирует случайный текст заданной максимальной длины."""
    placeholder = "... текст ..."
    if max_length < len(placeholder):
        return placeholder[:max_length]
    return placeholder


def generate_random_date(date_format: str = "DD.MM.YYYY") -> str:
    """Генерирует случайную дату в заданном формате."""
    now = datetime.datetime.now()
    # Генерируем дату в пределах следующих 12 месяцев
    random_days = random.randint(1, 365)
    random_date = now + datetime.timedelta(days=random_days)

    if date_format == "DD.MM.YYYY":
        return random_date.strftime("%d.%m.%Y")
    # Можно добавить другие форматы при необходимости
    return random_date.strftime("%d.%m.%Y")


def generate_random_value(field: dict[str, Any]) -> Union[str, list[str], dict[str, Any], list[dict[str, Any]], int]:
    """Генерирует случайное значение в зависимости от типа поля."""
    field_type = field.get("type", "text")

    if field_type == "text":
        max_length = field.get("maxLength", 100)
        description = field.get("description")
        return description[:max_length]

    elif field_type == "select":
        options = field.get("options", [])
        if options:
            return random.choice(options)
        return "выбранное значение"

    elif field_type == "multiselect":
        options = field.get("options", [])
        max_count = field.get("maxCount", 3)
        return ", ".join(
            random.choices(options, k=(random.randint(1, max_count))) if options else [f"тег{i + 1}" for i in range(
                random.randint(1, max_count))])

    elif field_type == "date":
        date_format = field.get("dateFormat", "DD.MM.YYYY")
        return generate_random_date(date_format)

    elif field_type == "number":
        return random.randint(1, 100)

    elif field_type == "boolean":
        return "Да" if random.randint(0, 1) else "Нет"

    elif field_type == "email":
        return "example@mail.com"

    elif field_type == "phone":
        return "+7800 000 00 00"

    elif field_type == "file":
        max_count = field.get("maxCount", 1)
        if max_count > 1:
            return "файлы"
        return "файл"

    elif field_type == "complex":
        is_repeated = field.get("is_repeated", False)
        max_count = field.get("maxCount", 3)
        result = []
        for _ in range(random.randint(1, max_count)):
            item = {}
            for sub_field in field.get("fields", []):
                sub_field_id = str(sub_field.get("id", "")).replace(".", "_")
                item[sub_field_id] = generate_random_value(sub_field)
            result.append(item)
        return result if is_repeated else result[0]

    return "значение"


def generate_test_data(form_structure: dict[str, Any]) -> dict[str, Any]:
    """Генерирует тестовые данные на основе структуры формы."""
    result = {}

    for field, field_key, _ in field_key_generator(form_structure):
        if field.get("is_repeated", False) and field["type"] != "complex":
            # Генерируем от 1 до 3 значений для повторяющихся полей
            count = random.randint(1, field.get("maxCount", 3))
            result[field_key] = [generate_random_value(field) for _ in range(count)]
        else:
            result[field_key] = generate_random_value(field)

    return result


def main():
    input_path = "test_data/input.json"

    # Загрузка входного JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    test_data = generate_test_data(input_data)
    print(json.dumps(test_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()