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
    if field["type"] == "complex":
        left_brace = min(answer.find('{') + 1 or len(answer) + 1, answer.find('[') + 1 or len(answer) + 1) - 1
        right_brace = max(answer.rfind('}'), answer.rfind(']')) + 1
        answer = answer[left_brace:right_brace]
        if answer:
            try:
                answer = ast.literal_eval(answer)
            except (ValueError, SyntaxError):
                answer = [] if is_repeated else {}
    elif is_repeated:
        answer = [answer_n.strip() for answer_n in answer.split(';') if answer_n.strip()]
    return answer
