from typing import Generator


def field_key_generator(input_data: dict) -> Generator[tuple[dict, str, str], None, None]:
    # Обработка каждой секции
    for section in input_data["sections"]:
        section_title = section["title"]
        for field in section["fields"]:
            yield field, f"field_{section['id']}_{field["id"]}".replace(".", "_"), f"{section_title}. "


def find_field_keys(json_data, prefix="field_"):
    """
    Рекурсивно находит все ключи, начинающиеся с указанного префикса в JSON-структуре.

    Args:
        json_data: JSON-данные (словарь, список или примитивный тип)
        prefix: Префикс для поиска ключей (по умолчанию "field_")

    Returns:
        list: Список найденных ключей, начинающихся с указанным префиксом
    """
    found_keys = []

    if isinstance(json_data, dict):
        # Для словарей проверяем ключи и рекурсивно обрабатываем значения
        for key, value in json_data.items():
            if key.startswith(prefix):
                found_keys.append(key)
            # Рекурсивно проверяем значения
            found_keys.extend(find_field_keys(value, prefix))

    elif isinstance(json_data, list):
        # Для списков рекурсивно обрабатываем только первый элемент
        found_keys.extend(find_field_keys(json_data[0], prefix))

    return found_keys