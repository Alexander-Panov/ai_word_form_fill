def generate_prompt(field, extra_description=""):
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

    # Обязательность поля
    # if is_required:
    #     prompt += "Это поле обязательно для заполнения\n"
    # else:
    #     prompt += "Это поле не обязательно для заполнения\n"

    # Дополнение промпта в зависимости от типа поля
    if field_type == "text":
        prompt += f"(ответ должен быть текстом"
        if max_length:
            prompt += f" не более {max_length} символов"
    elif field_type == "boolean":
        prompt += f'(в ответе укажи только "Да" или "Нет"'
    elif field_type == "email":
        prompt += f'(в ответе укажи только адрес электронной почты'
    elif field_type == "phone":
        prompt += f'(в ответе укажи только номер телефона, начинающийся с +7'
    elif field_type == "select":
        options_str = ", ".join([f'"{option}"' for option in options])
        prompt += f"(в ответе выбери один вариант из {options_str if options_str else "прошлых вариантов"}"

    elif field_type == "multiselect":
        options_str = ", ".join([f'"{option}"' for option in options])
        prompt += f"(в ответе выбери {f"до {max_count}" if max_count else 'нескольких'} вариантов из {options_str if options_str else "прошлых вариантов"}"

    elif field_type == "date":
        prompt += f"(в ответе укажи только дату в формате {date_format}"

    elif field_type == "number":
        prompt += f"(в ответе укажи только число"

    elif field_type == "file":
        file_types_str = ", ".join(file_types)
        prompt += f"(в ответе укажи только названия файлов (до {max_count if max_count else 'нескольких'}) в формате: {file_types_str}"

    elif field_type == "complex":
        # Для сложных полей с вложенными полями
        prompt += f"(ответ должен содержать следующие подпункты:\n"
        subfields_ids = []
        for subfield in field.get("fields", []):
            if not subfield.get("fields"):
                subfields_ids.append(subfield["id"])
                prompt += f"- {generate_prompt(subfield)}\n"

        subfield_join = ', '.join(f"'{subfield_id}':'значение'" for subfield_id in subfields_ids)
        prompt += f'Ответ дай в следующем формате: {{{subfield_join}}}. '
        prompt += 'Те подпункты, ответы на которые ты не можешь дать оставь в виде пустых значений'


    # Повторяемость поля
    if is_repeated:
        prompt += f". Необходимо указать несколько ответов на вопрос, разделяя ответы знаком ';'"
        if max_count:
            prompt += f". Напиши не более {max_count} значений. "

    return prompt + ")"
