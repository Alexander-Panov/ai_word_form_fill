from utils.utils import field_key_generator


def truncate_description(description, max_length=50):
    """Обрезает описание до указанной максимальной длины и добавляет многоточие"""
    if len(description) > max_length:
        return description[:max_length] + "..."
    return description


def get_jinja_fields(input_data: dict) -> dict:
    # Создаем структуру выходного JSON
    output_data = {}

    # Обработка каждой секции
    for field, field_key, _ in field_key_generator(input_data):
        output_data[field_key] = get_description_for_field(field)

    return output_data


def get_description_for_field(field: dict):
    if field.get("is_repeated", False) and field["type"] != "complex":
        # Для простых повторяющихся полей создаем массив
        return [truncate_description(field["description"])]
    elif field["type"] == "complex":
        # Для сложных повторяющихся полей создаем массив объектов
        sample_complex = {}
        for subfield in field["fields"]:
            subfield_id = str(subfield["id"]).replace(".", "_")
            sample_complex[subfield_id] = truncate_description(subfield["description"]) if not subfield.get(
                "fields") else get_description_for_field(subfield)
        return [sample_complex] if field.get("is_repeated", False) else sample_complex
    else:
        # Для простых неповторяющихся полей
        return truncate_description(field["description"])
