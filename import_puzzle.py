import sys
from typing import List
import sqlite3
import sys

from hashlib import md5

from db import create_connection, db_execute, db_execute_with_task

class Dimension:
    ROW = 'row'
    COLUMN = 'column'

class ValidKeys:
    catalogue = 'catalogue'
    title = 'title'
    width = 'width'
    height = 'height'

class ParseState:
    metadata = 'metadata'
    rows = 'rows'
    columns = 'columns'
    goal = 'goal'
    
def insert_puzzle_into_db(puzzle_id: str, width: int, height: int, row_rules: List[List[int]], column_rules: List[List[int]]):
    db_conn = create_connection(f'{puzzle_id}.sqlite')
    db_conn.set_trace_callback(print)
    setup_db(db_conn, puzzle_id)

    for row, rule_list in enumerate(row_rules):
        for rule_number, rule in enumerate(rule_list):
            insert_rule(db_conn, row, rule, rule_number, Dimension.ROW)

    for column, column_list in enumerate(column_rules):
        for column_number, rule in enumerate(column_list):
            insert_rule(db_conn, column, rule, column_number, Dimension.COLUMN)
    db_conn.commit()


def setup_db(db_conn, puzzle_id: str):
    create_metadata_sql = (
        f'CREATE TABLE IF NOT EXISTS metadata ('
        f'id integer PRIMARY KEY,'
        f'title text NOT NULL,'
        f'width integer NOT NULL,'
        f'height integer NOT NULL'
        f');'
    )
    
    create_rules_sql = (
        f'CREATE TABLE IF NOT EXISTS rules ('
        f'id integer PRIMARY KEY, '
        f'dimension_index integer NOT NULL, '
        f'rule integer NOT NULL, '
        f'rule_number integer NOT NULL, '
        f'dimension text NOT NULL'
        f');'
    )
    db_execute(db_conn, create_metadata_sql)
    db_execute(db_conn, create_rules_sql)
    db_conn.commit()

def insert_rule(conn, dimension_index, rule, rule_number, dimension):
    insert_rule_sql = (
        f'INSERT INTO rules(dimension_index,rule,rule_number,dimension)'
        f'VALUES(?,?,?,?)'
    )
    
    task = (dimension_index, rule, rule_number, dimension)
    db_execute_with_task(conn, insert_rule_sql, task)

if __name__ == '__main__':
    filename = sys.argv[1]

    title = ''
    width = height = 0
    goal = ''
    row_rules = []
    column_rules = []

    parse_state = ParseState.metadata

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == ParseState.rows:
                parse_state = ParseState.rows
                continue
            elif line == ParseState.columns:
                parse_state = ParseState.columns
                continue
            elif line.startswith(ParseState.goal):
                goal = line.split(' ')[-1].replace('"', '')
                parse_state = ParseState.goal
                continue

            if parse_state == ParseState.metadata:
                if line.startswith(ValidKeys.catalogue):
                    pass
                elif line.startswith(ValidKeys.title):
                    title = line[len(ValidKeys.title) + 1:]
                    title = title.replace('"', '')
                    title = title.encode('utf-8')
                elif line.startswith(ValidKeys.width):
                    width = int(line.split(' ')[-1])
                elif line.startswith(ValidKeys.height):
                    height = int(line.split(' ')[-1])
            elif parse_state == ParseState.rows or parse_state == ParseState.columns:
                target_rule_list = row_rules if parse_state == ParseState.rows else column_rules
                if line == '':
                    continue
                target_rule_list.append(list(map(int, line.split(','))))
                
    print(f'Title: {title}')
    print(f'width {width} x column {height}')
    print('rows')
    for r in row_rules:
        print(r)
    print('columns')
    for c in column_rules:
        print(c)

    insert_puzzle_into_db(md5(title).hexdigest(), width, height, row_rules, column_rules)
