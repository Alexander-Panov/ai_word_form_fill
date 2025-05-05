import json
import logging
import os

import pytest

from logger import logger
from tests.utils import load_json_data, load_file_data


@pytest.fixture(scope="session", autouse=True)
def setup():
    os.environ["LANGSMITH_TRACING"] = "false"  # отключить langsmith
    logger.setLevel(logging.CRITICAL + 1)  # отключить логирование


@pytest.fixture(scope="session")
def input_document_schema() -> dict:
    return load_json_data("input.json")


@pytest.fixture(scope="session")
def view_output_schema() -> dict:
    return load_json_data("view_output.json")


@pytest.fixture(scope="session")
def form_fill_data_test() -> dict:
    return load_json_data("test_fill_data.json")


@pytest.fixture(scope="session")
def input_document_schema() -> dict:
    return load_json_data("simple/input.json")


@pytest.fixture(scope="session")
def answers() -> dict:
    return load_json_data("simple/answers.json")


@pytest.fixture(scope="session")
def raw_answers() -> dict:
    return load_json_data("simple/raw_answers.json")


@pytest.fixture(scope="session")
def raw_answer_dict() -> str:
    return load_file_data("dict/raw_answer_dict.txt")


@pytest.fixture(scope="session")
def answer_dict() -> dict:
    return load_json_data("dict/answer_dict.json")


@pytest.fixture(scope="session")
def raw_answers_budget() -> dict:
    return load_json_data("budget/raw_answers.json")


@pytest.fixture(scope="session")
def answers_budget() -> dict:
    return load_json_data("budget/answers.json")


@pytest.fixture(scope="session")
def budget_document_schema() -> dict:
    return load_json_data("budget/document_schema.json")


@pytest.fixture(scope="session")
def complex_document_schema() -> dict:
    return load_json_data("complex/document_schema.json")
