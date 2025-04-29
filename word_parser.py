import argparse
import asyncio
import os
import sys

from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_core.prompts import PromptTemplate

from logger import logger
from config import AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
from models import FillForm

form_analyzer_template = """
Есть следующая форма для заявки:
{doc}
---
Напиши json структуру полей этой формы. Постарайся максимально точно отразить заполняемые поля по данной структуре, удобной для последующего автоматического заполнения, при этом не вводя лишние поля.
Дели форму на секции и поля. Не обращай внимания на подпункты
В ответе перечисли только те поля структуры, которые не равны null или значению по-умолчанию
"""

# noinspection PyArgumentList
form_analyzer_prompt = PromptTemplate(
    template=form_analyzer_template,
    input_varialbes=["doc"],
)

#  noinspection PyArgumentList
model = ChatAnthropic(model='claude-3-7-sonnet-latest', temperature=0, timeout=None, max_tokens=64000)


form_analyzer_chain = (form_analyzer_prompt | model.with_structured_output(FillForm)).with_config(
    run_name="Form Analyzer")


async def parse_document(doc: bytes) -> FillForm:
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
        api_key=AZURE_DOCUMENT_INTELLIGENCE_KEY,
        bytes_source=doc,
        api_model="prebuilt-layout"
    )

    documents = await loader.aload()
    logger.info("Azure Document Intelligence разобран")
    document_content = documents[0].page_content

    return await form_analyzer_chain.ainvoke({"doc": document_content})


async def main():
    parser = argparse.ArgumentParser(description='Проводит ИИ разбор Word формы и сохраняет схему в формате json')
    parser.add_argument('input_file', help='Путь к Word форме')
    parser.add_argument('-o', '--output', help='Вывод JSON файл путь (по умолчанию: schema.json)')
    args = parser.parse_args()

    # Проверяем существование входного файла
    if not os.path.exists(args.input_file):
        print(f"❌ Ошибка: Входной файл '{args.input_file}' не существует", file=sys.stderr)
        return 1

    # Определяем путь к выходному файлу
    output_file = args.output if args.output else 'schema.json'

    try:
        with open(args.input_file, 'rb') as f:
            content = f.read()
        # Вызываем функцию для обработки документа
        schema = await parse_document(content)

        # Сохраняем результат в JSON файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(schema.model_dump_json(exclude_defaults=True, indent=4))

        print(f"✅ Схема успешно сохранена '{output_file}'")
        return 0
    except Exception as e:
        print(f"❌ Ошибка при обработке документа: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Запускаем асинхронную функцию main
    exit_code = asyncio.run(main())
    sys.exit(exit_code)