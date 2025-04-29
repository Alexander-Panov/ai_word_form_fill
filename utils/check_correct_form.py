from utils.utils import find_field_keys


def check_correct_template_fields(json_data: dict, template_vars: set[str]) -> str:
    errors = ""

    schema_vars = set(find_field_keys(json_data))

    if (schema_count := len(schema_vars)) != (template_count := len(template_vars)):
        errors += f"Не совпадает кол-во полей: в схеме {schema_count}, в шаблоне {template_count}\n"

    # Находим элементы, которые есть в template_vars, но нет в schema_vars
    differences_to_schema = [var for var in schema_vars if var not in template_vars]
    if len(differences_to_schema) != 0:
        errors += f"Не хватает полей: {sorted(differences_to_schema)}\n"

    differences_to_template = [var for var in template_vars if var not in schema_vars]
    if len(differences_to_template) != 0:
        errors += f"Лишние поля: {sorted(differences_to_template)}\n"

    return errors

