from enum import Enum

from pydantic import BaseModel, Field


class FormFieldType(Enum):
    """Тип поля:
    select - выбрать один вариант из предложенных
    multiselect - выбрать несколько вариантов из предложенных
    text - текстовое поле
    number - числовое поле
    boolean - указать "Да" или "Нет"
    file - прикрепить файл
    link - прикрепить ссылку
    date - указать дату
    phone - указать номер телефона
    email - указать email
    complex - состоит из нескольких полей других типов
    """
    Select = "select"
    Multiselect = "multiselect"
    Text = "text"
    Number = "number"
    Boolean = "boolean"
    File = "file"
    Link = "link"
    Date = "date"
    Phone = "phone"
    Email = "email"
    Complex = "complex"


class FormField(BaseModel):
    """Поле в форме. Может содержать внутри себя другие поля"""
    id: str = Field(description="Цифровой номер (присвой текстовой id если нет номера)")
    description: str = Field(description="Описание и подсказки для заполнения поля")
    type: FormFieldType = Field(description="Тип поля")
    required: bool = Field(description="Поле обязательно для заполнения")

    options: list[str] | None = Field(description="Варианты выбора (для типа select)", default=None)
    maxLength: int | None = Field(description="Максимальная длина текста в символах (для типа text)", default=None)
    is_repeated: bool = Field(description="Поле повторяется несколько раз?", default=False)
    maxCount: int | None = Field(description="Максимальное количество", default=None)
    fileTypes: list[str] | None = Field(description="Разрешенные форматы файлов (для типа file)", default=None)
    dateFormat: str | None = Field(description="Формат возвращаемой даты (для типа date)", default=None)
    fields: list["FormField"] | None = Field(description="Внутренние поля (для типа complex)", default=None)


class FormSection(BaseModel):
    """Секция формы"""
    id: str = Field(description="Цифровой номер (или название) секции в документе")
    title: str = Field(description="Заголовок секции")
    fields: list[FormField] = Field(description="Заполняемые поля секции")

class FillForm(BaseModel):
    """Форма для заполнения"""
    title: str = Field(description="Заголовок формы")
    sections: list[FormSection] = Field(description="Секции, из которых состоит форма")

