from typing import Any

from langsmith import traceable
from openai import AsyncClient

from doc_fill.openai_client import prompt_ai
from doc_fill.parse_answer import parse_answer
from doc_fill.prompt_generator import generate_prompt
from logger import logger
from utils.utils import field_key_generator

SYSTEM_PROMPT = """Ты помощник в заполнении формы "{}". Ты помогаешь пользователю заполнять форму, отвечая на его вопросы по проекту на основе документов. Если ответа на вопрос в документах не указано, оставь ответ пустым.
Прочитай внимательно требования пользователя к ответу, подумай шаг за шагом, напиши свои рассуждения и в конце дай ясный ответ соответствующий требованиям в формате \"Ответ: <твой ответ>\"
Твои ответы будут напрямую вставлены в форму. Начинай отвечать на вопросы пользователя"""


@traceable
async def ai_generate_fill_form(client: AsyncClient, input_data: dict, vector_store_id: str) -> dict[
    str, str | dict[str, str]]:
    messages = [{'role': "system", "content": SYSTEM_PROMPT.format(input_data["title"])}]
    logger.info("Start fill form")
    answers = {}
    for field, field_key, section_title in field_key_generator(input_data):
        answers.update(await prompt_ai_field(client, field_key, field, messages, vector_store_id, section_title))

    return answers


async def prompt_ai_field(client: AsyncClient, field_key: str, field: dict, messages: list, vector_store_id: str,
                          extra_description="") -> \
        dict[str, Any]:
    output = {}
    if not field.get("is_repeated", False):
        for inner_field in field.get("fields", []):
            if inner_field.get("fields"):
                inner_field_key = str(inner_field["id"]).replace(".", "_")
                output.update(await prompt_ai_field(client, inner_field_key, inner_field, messages, vector_store_id,
                                                    f"{extra_description}{field["description"]}. "))
    if not output:
        prompt = "Вопрос: " + generate_prompt(field, extra_description)
        messages.append({"role": "user", "content": prompt})
        logger.info(f"{field_key} PROMPT: {prompt}")
        ai_message_text = await prompt_ai(client, messages, vector_store_id)
        logger.info(f"{field_key} AI RESPONSE: {ai_message_text}")
        messages.append({"role": "assistant", "content": ai_message_text})
        output = parse_answer(field, ai_message_text)
    return {field_key: output}