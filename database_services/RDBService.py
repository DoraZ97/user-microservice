import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_db_connection():
    db_connect_info = context.get_db_info()

    logger.info("RDBService._get_db_connection:")
    logger.info("\t HOST = " + db_connect_info['host'])

    db_info = context.get_db_info()
    db_connection = pymysql.connect(
        **db_info
    )
    return db_connection


def get_by_prefix(db_schema, table_name, column_name, value_prefix):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
          column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def get_user(db_schema, table_name):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res

def get_userID(db_schema, table_name, ID):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where ID = " + ID
    print(sql)
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res

def update_users(db_schema, table_name, tasks):
    print(tasks)
    id = tasks["ID"]
    firstName = tasks["firstName"]
    lastName = tasks["lastName"]
    email = tasks["email"]
    addressID = tasks["addressID"]
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "Insert into " + db_schema + "." + table_name + " (ID, firstName, lastName, email, addressID) VALUES (" + id + ",'" + firstName + "','" + lastName + "','" + email + "'," + addressID + ")"
    print(sql)
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    conn.commit()
    conn.close()
    return res

def get_address_by_userID(db_schema, table_name1, table_name2, ID):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name2 + " WHERE ID = (select addressID from " + \
          db_schema + "." + table_name1 + " Where ID = " + ID + ")"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res

def get_address(db_schema, table_name):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()
    print(res)

    conn.close()

    return res


def _get_where_clause_args(template):
    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " + " AND ".join(terms)

    return clause, args


def find_by_template(db_schema, table_name, template, field_list):
    wc, args = _get_where_clause_args(template)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    res = cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res
