from . import DUPLICATE_KEY_ERROR_REGEX
import re

def not_null_constraint_key(error):
    return error.split('violates not-null constraint')[0] \
                .split('column')[1].strip().replace('"', '')

def unique_constraint_key(error):
    m = re.search(DUPLICATE_KEY_ERROR_REGEX, error)
    return m.group('duplicate_key')

def not_null_constraint_error(error):

    regexp_detail = r' (?P<value>.*) value in column "(?P<column>.*)" violates'
    match_detail = re.search(regexp_detail, error)
    column = match_detail.group('column')
    value = match_detail.group('value')
    regexp_table = r'INSERT INTO (?P<table>.*)'
    match_table = re.search(regexp_table, error)
    table = match_table.group('table').split(' ')[0]

    return {
        'table': table,
        'column': column,
        'value': value,
        'name': 'missing_attribute'
    }

def unique_constraint_error(error):
    regexp_detail = r'DETAIL:\s+Key \((?P<column>.*)\)=\((?P<value>.*)\) already exists.'
    match_detail = re.search(regexp_detail, error)
    column = match_detail.group('column')
    value = match_detail.group('value')
    regexp_table = r'violates unique constraint "(?P<table>.*)_' + re.escape(column) + r'_key"'
    match_table = re.search(regexp_table, error)
    table = match_table.group('table')
    return {
        'table': table,
        'column': column,
        'value': value,
        'name': 'value_exists'
    }