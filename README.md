# ИИ заполнение Word форм

[Хабр статья](https://habr.com/ru/sandbox/244650/)

## Установка зависимостей
Требуется пакетный менеджер uv:
```shell
uv sync --frozen --no-dev
```

## Шаг 1. ИИ Анализ формы
```shell
uv run python word_parser.py "examples/Форма ФСИ студстартап.docx" -o examples/schema.json
```

## Шаг 2. Разметка формы
Получаем список id полей с помощью утилиты
```shell
uv run python utils.py jinja_fields examples/schema.json
```

![jinja.gif](images/jinja.gif)

Размечаем шаблон используя [Jinja2 синтаксис](https://docxtpl.readthedocs.io/en/latest/#jinja2-like-syntax)

![markup_form.png](images/markup_form.png)

Проверяем корректность заполнения
```shell
uv run python utils.py check_correct_form examples/schema.json "examples/Форма ФСИ студстартап размеченная.docx"
```

![check_uncorrect.gif](images/check_uncorrect.gif)

Исправляем неправильные теги. Проверяем еще раз

![check_correct.gif](images/check_correct.gif)

Заполняем тестовыми данными
```shell
uv run python utils.py generate_test_data examples/schema.json "examples/Форма ФСИ студстартап размеченная.docx"
```
![generate_test_data.gif](images/generate_test_data.gif)

![filled_fake_data_form.png](images/filled_fake_data_form.png)


## Шаг 3. Заполнение ИИ
```shell
uv run python word_fill.py examples/schema.json "examples/Форма ФСИ студстартап размеченная.docx" examples/документ1.docx
```

![filled_form.png](images/filled_form.png)
