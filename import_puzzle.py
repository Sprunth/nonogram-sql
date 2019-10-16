import sys
from typing import List
import sqlite3

from db import create_connection

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

    create_metadata_sql = (
        f'CREATE TABLE IF NOT EXISTS metadata'
        f'id integer PRIMARY KEY'
        f'title text NOT NULL'
        f'width integer NOT NULL'
        f'height integer NOT NULL'
    )

    create_row_rules_sql = (
        f'CREATE TABLE IF NOT EXISTS row_rules'
        f'id integer PRIMARY KEY'
        f'' # array??
    )

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

    insert_puzzle_into_db(hash(title), width, height, row_rules, column_rules)
