import ast
from typing import Any

ANSWER_WORD = "Ответ:"
ANSWER_WORD_IND_SHIFT = len(ANSWER_WORD)


def parse_answer(field: dict[str, Any], ai_message_text: str) -> str | list | dict:
    # хитрая математика, чтобы писать меньше кода
    answer_ind = ai_message_text.find(ANSWER_WORD) + 1 or -ANSWER_WORD_IND_SHIFT + 1
    answer = ai_message_text[answer_ind + ANSWER_WORD_IND_SHIFT - 1:]
    if answer.endswith('.'):
        answer = answer[:-1]

    answer = answer.strip()

    is_repeated = field.get("is_repeated")
    if is_repeated:
        answer = [answer_n.strip() for answer_n in answer.split(';') if answer_n.strip()]
    if field["type"] == "complex":
        answer = answer if isinstance(answer, list) else [answer]
        answers = []
        for answer_n in answer:
            left_curly_brace = answer_n.find('{') + 1
            right_curly_brace = answer_n.find('}') + 1
            if left_curly_brace and right_curly_brace:
                answers.append(ast.literal_eval(answer_n[left_curly_brace-1:right_curly_brace]))
        if is_repeated:
            answer = answers
        else:
            try:
                answer = answers[0]
            except IndexError:
                answer = {}
    return answer
