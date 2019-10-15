import sys

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

