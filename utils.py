import argparse
import json
import os
import sys

from docxtpl import DocxTemplate

from logger import logger
from utils.check_correct_form import check_correct_template_fields
from utils.generate_test_data import generate_test_data
from utils.jinja_fields import get_jinja_fields


def jinja_fields_command(input_path):
    """
    Показывает Jinja шаблонами для JSON файла,
    Args:
        input_path: Путь к входному JSON файлу
    Returns:
        Код завершения: 0 при успехе, иначе код ошибки
    """
    try:
        # Проверка существования входного файла
        if not os.path.exists(input_path):
            print(f"❌ Ошибка: Входной файл '{input_path}' не существует", file=sys.stderr)
            return 1

        # Загрузка входного JSON
        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        # Вызов существующей функции преобразования
        result = get_jinja_fields(input_data)

        print(json.dumps(result, ensure_ascii=False, indent=4))
        return 0

    except json.JSONDecodeError as e:
        print(f"❌ Ошибка при разборе JSON: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}", file=sys.stderr)
        return 3

def check_correct_form_command(input_path: str, template_path: str) -> int:
    try:
        # Проверка существования входного файла
        if not os.path.exists(input_path):
            print(f"❌ Ошибка: Входной файл '{input_path}' не существует", file=sys.stderr)
            return 1

        # Проверка существования шаблона
        if not os.path.exists(template_path):
            print(f"❌ Ошибка: Файл шаблона '{template_path}' не существует", file=sys.stderr)
            return 1

        # Загрузка входного JSON
        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        # Загрузка шаблона

        errors = ""
        doc_template = DocxTemplate(template_path)
        # Получаем все переменные в шаблоне
        template_vars = doc_template.get_undeclared_template_variables()
        errors = check_correct_template_fields(get_jinja_fields(input_data), template_vars)

        if not errors:
            print("✅ Шаблон заполнен корректно.")
            return 0
        else:
            print("❌ Обнаружены несоответствия между полями и шаблоном:")
            print(errors)
            return 2

    except Exception as e:
        print(f"❌ Произошла ошибка при проверке формы: {e}", file=sys.stderr)
        return 3

def generate_test_data_command(input_path: str, template_path: str, output_path: str) -> int:
    try:
        # Проверка существования входного файла
        if not os.path.exists(input_path):
            print(f"❌ Ошибка: Входной файл '{input_path}' не существует", file=sys.stderr)
            return 1

        # Проверка существования шаблона
        if not os.path.exists(template_path):
            print(f"❌ Ошибка: Файл шаблона '{template_path}' не существует", file=sys.stderr)
            return 1

        # Загрузка входного JSON
        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        # Загрузка шаблона
        doc_template = DocxTemplate(template_path)
        doc_template.render(generate_test_data(input_data))
        doc_template.save(output_path)
        print("✅ Форма успешно заполнена фейковыми данными")
        return 0
    except Exception as e:
        print(f"❌ Произошла ошибка при заполнении формы: {e}", file=sys.stderr)
        return 3

def main():
    parser = argparse.ArgumentParser(description='Утилиты для работы с документами')
    subparsers = parser.add_subparsers(dest='command', help='Команды')

    # Команда jinja_fields
    jinja_parser = subparsers.add_parser('jinja_fields', help='Показать JSON для использования в Jinja шаблонах')
    jinja_parser.add_argument('input', help='Путь к входному JSON файлу')

    # Команда check_correct_form
    check_parser = subparsers.add_parser('check_correct_form', help='Проверить соответствие JSON полей и шаблона формы')
    check_parser.add_argument('input', help='Путь к входному JSON файлу')
    check_parser.add_argument('template', help='Путь к файлу шаблона формы')

    # Команда generate_test_data
    check_parser = subparsers.add_parser('generate_test_data', help='Заполнить шаблон формы фейковыми данными')
    check_parser.add_argument('input', help='Путь к входному JSON файлу')
    check_parser.add_argument('template', help='Путь к файлу шаблона формы')
    check_parser.add_argument('-o', '--output', help='Путь заполненной Word формы (по умолчанию: fake_filled_form.docx)')

    args = parser.parse_args()

    # Обработка команд
    if args.command == 'jinja_fields':
        return jinja_fields_command(args.input)
    elif args.command == 'check_correct_form':
        return check_correct_form_command(args.input, args.template)
    elif args.command == 'generate_test_data':
        return generate_test_data_command(args.input, args.template, args.output if args.output else 'fake_filled_form.docx')
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())