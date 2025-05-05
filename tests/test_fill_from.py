from unittest.mock import patch, AsyncMock

import pytest

from doc_fill.ai_fill_form import ai_generate_fill_form
from doc_fill.parse_answer import parse_answer
from utils.utils import field_key_generator


async def base_test_ai_fill_form(input_schema: dict, raw_answers: list, answers: dict):
    # Создаем патч для функции prompt_ai
    with patch('doc_fill.ai_fill_form.prompt_ai', new_callable=AsyncMock) as mock_prompt_ai:
        # Настраиваем мок для последовательного возврата ответов из списка raw_answers
        mock_prompt_ai.side_effect = raw_answers

        result = await ai_generate_fill_form(None, input_schema, "fake_vector_store_id")
        assert answers == result
        assert mock_prompt_ai.call_count == len(raw_answers)

@pytest.mark.asyncio
async def test_ai_fill_form(input_document_schema: dict, raw_answers: list, answers: dict):
    await base_test_ai_fill_form(input_document_schema, raw_answers, answers)


@pytest.mark.asyncio
async def test_ai_fill_budget(budget_document_schema: dict, raw_answers_budget: list, answers_budget: dict):
    await base_test_ai_fill_form(budget_document_schema, raw_answers_budget, answers_budget)


def test_field_key_generator(input_document_schema: dict):
    results = [prompt for prompt in field_key_generator(input_document_schema)]
    assert len(results) == 20


def test_parse_answer(input_document_schema: dict, answers: dict, raw_answers: dict):
    results_cleared = {key: parse_answer(field, raw_answer) for (field, key, _), raw_answer in
                       zip(field_key_generator(input_document_schema), raw_answers)}

    assert answers == results_cleared


def test_parse_answer_dict(raw_answer_dict: str, answer_dict: dict):
    field = {
        "id": "salary_staff",
        "description": "Оплата труда штатных работников, включая НДФЛ",
        "type": "complex",
        "required": True,
        "is_repeated": True,
        "fields": [
            {
                "id": "position",
                "description": "Должность",
                "type": "text",
                "required": True
            },
            {
                "id": "total_cost",
                "description": "Общая стоимость (руб.)",
                "type": "number",
                "required": True
            },
            {
                "id": "co_financing",
                "description": "Софинансирование (если имеется) (руб.)",
                "type": "number",
                "required": False
            },
            {
                "id": "requested_amount",
                "description": "Запрашиваемая сумма (руб.)",
                "type": "number",
                "required": True
            }
        ]
    }
    assert parse_answer(field, raw_answer_dict) == answer_dict
