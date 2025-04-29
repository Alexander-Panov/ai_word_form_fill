import argparse
import asyncio
import json
import os
import sys

from docxtpl import DocxTemplate
from tenacity import RetryError

from doc_fill.ai_fill_form import ai_generate_fill_form
from doc_fill.openai_client import create_client
from doc_fill.vector_store import create_vector_store, add_files, IncorrectFilesException, delete_files, \
    delete_vector_store, clear_openai_storage
from logger import logger


async def word_fill_command(schema_path: str, template_path: str, file_paths: list[str], output_path: str):
    # Загрузка JSON схемы
    with open(schema_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    vector_store_id = None
    files_ids = None
    client = None

    try:
        client = create_client()

        vector_store_id = await create_vector_store(client)
        logger.info("vector store created")
        files_ids = await add_files(client, vector_store_id, file_paths)
        logger.info("files uploaded")
        answers = await ai_generate_fill_form(client, input_data, vector_store_id)
        doc_template = DocxTemplate(template_path)
        doc_template.render(answers)
        doc_template.save(output_path)
    except IncorrectFilesException as files_ex:
        print(f"❌ {files_ex}", file=sys.stderr)
        files_ids = files_ex.files_ids
    except RetryError as e:
        print(f"Достигнуты лимиты OpenAI", file=sys.stderr)
    except Exception as ex:
        print(f"❌ {ex}", file=sys.stderr)
    else:
        print(f"✅ Форма успешно заполнена")
    finally:
        await clear_openai_storage(client, files_ids, vector_store_id)


async def main():
    """
    Основная функция программы для заполнения Word документов на основе JSON схемы.
    """
    parser = argparse.ArgumentParser(
        description='Заполняет Word документ на основе JSON схемы данными из файлов'
    )

    # Обязательный аргумент - путь к JSON схеме
    parser.add_argument(
        'schema_path',
        help='Путь к файлу JSON схемы документа'
    )

    parser.add_argument(
        'template_path',
        help='Путь к размеченной Word форме'
    )

    # Обязательный аргумент - один или несколько путей к Word файлам
    parser.add_argument(
        'file_paths',
        nargs='+',  # Принимает один или более аргументов
        help='Пути к Word файлам для заполнения (один или несколько)'
    )

    # Необязательный аргумент - путь для сохранения результата
    parser.add_argument(
        '-o', '--output',
        help='Путь для сохранения результата (по умолчанию result.docx)'
    )

    args = parser.parse_args()

    # Проверка существования файла схемы
    if not os.path.exists(args.schema_path):
        print(f"❌ Ошибка: Файл схемы '{args.schema_path}' не существует", file=sys.stderr)
        return 1

    # Проверка существования файла шаблона
    if not os.path.exists(args.template_path):
        print(f"❌ Ошибка: Файл шаблона '{args.template_path}' не существует", file=sys.stderr)
        return 1

    # Проверка существования всех Word файлов
    for file_path in args.file_paths:
        if not os.path.exists(file_path):
            print(f"❌ Ошибка: Файл '{file_path}' не существует", file=sys.stderr)
            return 1

    try:
        # Вызов функции для заполнения документов
        await word_fill_command(args.schema_path, args.template_path, args.file_paths, args.output if args.output else 'result.docx')
        return 0
    except Exception as e:
        print(f"❌ Произошла ошибка при заполнении формы: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Запускаем асинхронную функцию main
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
