def generate_prompt(field, extra_description="") -> str:
    prompt, format = generate_prompt_and_format(field, extra_description)
    if format:
        prompt += f'\nОтвет дай в следующем формате: {format}. '
    if field.get("type", "") == "complex":
        prompt += 'Те подпункты, ответы на которые ты не можешь дать оставь в виде пустых значений'
    return prompt


def generate_prompt_and_format(field, extra_description="", tab_level=1) -> tuple[str, str]:
    field_type = field.get("type", "")
    description = field.get("description", "")
    # is_required = field.get("required", False)
    max_length = field.get("maxLength", None)
    max_count = field.get("maxCount", None)
    options = field.get("options", [])
    is_repeated = field.get("is_repeated", False)
    date_format = field.get("dateFormat", None)
    file_types = field.get("fileTypes", [])

    # Базовая часть промпта
    prompt = f'"{extra_description}{description}" '
    format = ''
    split_sign = ";"

    # Обязательность поля
    # if is_required:
    #     prompt += "Это поле обязательно для заполнения\n"
    # else:
    #     prompt += "Это поле не обязательно для заполнения\n"

    # Дополнение промпта в зависимости от типа поля
    if field_type == "text":
        prompt += f"(укажи только текст"
        if max_length:
            prompt += f" не более {max_length} символов"
    elif field_type == "boolean":
        prompt += f'(укажи только "Да" или "Нет"'
    elif field_type == "email":
        prompt += f'(укажи только адрес электронной почты'
    elif field_type == "phone":
        prompt += f'(укажи только номер телефона, начинающийся с +7'
    elif field_type == "select":
        options_str = ", ".join([f'"{option}"' for option in options])
        prompt += f"(выбери один вариант из {options_str if options_str else "прошлых вариантов"}"

    elif field_type == "multiselect":
        options_str = ", ".join([f'"{option}"' for option in options])
        prompt += f"(выбери {f"до {max_count}" if max_count else 'нескольких'} вариантов из {options_str if options_str else "прошлых вариантов"}"

    elif field_type == "date":
        prompt += f"(укажи только дату"
        format = date_format

    elif field_type == "number":
        prompt += f"(укажи только число"

    elif field_type == "file":
        file_types_str = ", ".join(file_types)
        prompt += f"(укажи только названия файлов (до {max_count if max_count else 'нескольких'}) в формате: {file_types_str}"


    elif field_type == "complex":
        # Для сложных полей с вложенными полями
        prompt += f"(поле должно содержать следующие подпункты:\n"
        subfields_formats = []
        for subfield in field.get("fields", []):
            subfield_prompt, subfield_format = generate_prompt_and_format(subfield, tab_level=tab_level+1)
            subfields_formats.append(f"'{subfield["id"]}':{subfield_format if subfield_format else "'значение'"}")
            prompt += "\t" * tab_level + f"- {subfield_prompt}\n"
        prompt += "\t" * tab_level
        format = f"{{{', '.join(subfields_formats)}}}"
        if is_repeated:
            format = f"[{format}]"
            split_sign = ','


    # Повторяемость поля
    if is_repeated:
        prompt += f"Необходимо указать {f"не более {max_count}" if max_count else "несколько"} значений, разделяя их знаком '{split_sign}'"

    return prompt + ")", format
