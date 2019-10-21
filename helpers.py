from db import db_execute, db_execute_with_params


class Dimension:
    ROW = 'row'
    COLUMN = 'column'


def debug_dump_puzzle(conn):
    metadata = db_execute(conn, 'SELECT * FROM metadata')
    print(f'Metadata: {metadata}')

    row_count = db_execute_with_params(conn, 'SELECT COUNT(DISTINCT dimension_index) FROM rules WHERE dimension=?', (Dimension.ROW,))[0][0]
    column_count = db_execute_with_params(conn, 'SELECT COUNT(DISTINCT dimension_index) FROM rules WHERE dimension=?', (Dimension.COLUMN,))[0][0]

    print(f'Row count: {row_count}')
    for i in range(row_count):
        rule_list = get_rule_list(conn, Dimension.ROW, i)
        print(f'Row {i}: {rule_list}')

    print(f'Column count: {column_count}')
    for i in range(column_count):
        rule_list = get_rule_list(conn, Dimension.COLUMN, i)
        print(f'Column {i}: {rule_list}')

    for row in range(row_count):
        row_values = db_execute_with_params(conn, 'SELECT value FROM puzzle WHERE row=? ORDER BY column', (row,))
        row_values = [str(v[0]) for v in row_values]
        print(' '.join(row_values))


def get_rule_list(conn, dimension: str, dimension_index: int):
    sql = (
        f'SELECT rule FROM rules '
        f'WHERE dimension=? '
        f'AND dimension_index=? '
        f'ORDER BY rule_number'
    )
    params = (dimension, dimension_index)
    rule_list = db_execute_with_params(conn, sql, params)
    return [rule[0] for rule in rule_list]  # since fetch_all returns tuple of selected columns
