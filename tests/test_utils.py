from utils.check_correct_form import check_correct_template_fields
from utils.generate_test_data import generate_test_data
from utils.jinja_fields import get_jinja_fields
from utils.utils import find_field_keys


def test_find_field_keys(view_output_schema: dict):
    vars = find_field_keys(view_output_schema, prefix="")
    assert len(vars) == 28
    expected = ['field_1_9', 'field_1_5', 'field_1_7', 'field_1_10', 'field_1_3_1', 'field_1_15', 'field_1_11',
                'field_1_3_3', 'field_1_8_1', 'field_1_8', 'field_1_1_1', 'field_1_13', 'field_1_14', 'field_1_6',
                'field_1_1', 'field_1_12', 'field_1_3', 'field_1_2', 'field_1_4', 'field_1_3_2', "link", "description",
                "target_group", "quantitative_results_indicator", "quantitative_results_value", "qualitative_results",
                "partner", "support_type"]
    assert sorted(vars) == sorted(expected)

def test_find_field_keys_with_prefix(view_output_schema: dict):
    vars = find_field_keys(view_output_schema)
    assert len(vars) == 20
    expected = ['field_1_9', 'field_1_5', 'field_1_7', 'field_1_10', 'field_1_3_1', 'field_1_15', 'field_1_11',
                'field_1_3_3', 'field_1_8_1', 'field_1_8', 'field_1_1_1', 'field_1_13', 'field_1_14', 'field_1_6',
                'field_1_1', 'field_1_12', 'field_1_3', 'field_1_2', 'field_1_4', 'field_1_3_2']
    assert sorted(vars) == sorted(expected)


def test_get_jinja_fields(input_document_schema: dict, view_output_schema: dict):
    result = get_jinja_fields(input_document_schema)
    assert view_output_schema == result


def test_check_correct_number_fields(view_output_schema: dict):
    template_vars = {'field_1_9', 'field_1_5', 'field_1_7', 'field_1_10', 'field_1_3_1', 'field_1_15', 'field_1_11',
                     'field_1_3_3', 'field_1_8_1', 'field_1_8', 'field_1_1_1', 'field_1_13', 'field_1_14', 'field_1_6',
                     'field_1_1', 'field_1_12', 'field_1_3', 'field_1_2', 'field_1_4', 'field_1_3_2'}

    errors = check_correct_template_fields(view_output_schema, template_vars)
    assert errors == ''


def test_check_correct_number_fields_errors(view_output_schema: dict):
    template_vars = {'field_1_5_1', 'field_1_7', 'field_1_10', 'field_1_3_1', 'field_1_15', 'field_1_11',
                     'field_1_3_3', 'field_1_8_1', 'field_1_8', 'field_1_1_1', 'field_1_13', 'field_1_14', 'field_1_6',
                     'field_1_1', 'field_1_12', 'field_1_3', 'field_1_2', 'field_1_4', 'field_1_3_2'}

    errors = check_correct_template_fields(view_output_schema, template_vars)
    assert errors == "Не совпадает кол-во полей: в схеме 20, в шаблоне 19\nНе хватает полей: ['field_1_5', 'field_1_9']\nЛишние поля: ['field_1_5_1']\n"

def test_generate_test_data(input_document_schema: dict, view_output_schema: dict):
    expected_vars=find_field_keys(view_output_schema, prefix="")
    tested_vars=find_field_keys(generate_test_data(input_document_schema), prefix="")
    assert sorted(expected_vars) == sorted(tested_vars)