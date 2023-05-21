from django.db import connection


def commit():
    connection.commit()


def rollback():
    connection.rollback()


def sql_clean(table, doc_id):
    with connection.cursor() as cursor:
        q = "delete from myapp_" + table + " where doc_id = " + str(doc_id)
        print(q)
        cursor.execute(q)
        res = cursor.fetchone()

    return res


def sql_insert(table, query_str):
    with connection.cursor() as cursor:
        q = "insert or replace into myapp_" + table + " values " + query_str
        print(q)
        cursor.execute(q)
        res = cursor.fetchone()

    return res


def db_to_df(table, doc_id):
    with connection.cursor() as cursor:
        q = "select * from myapp_" + table + " where doc_id = " + str(doc_id)
        cursor.execute(q)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def df_to_query_str(df, doc, skip=0):
    q_str = ''
    for index, row in df.iterrows():
        if index < skip and skip > 0:
            continue
        row_str = '(null,'
        for col in df.columns:
            val = str(row[col])
            if val == 'Х' or val == 'X':
                val = '-1'
            row_str += val + ','
        row_str += str(doc) + ',' + str(index+1-skip) + ')'
        q_str += row_str + ','

    return q_str[:-1]
