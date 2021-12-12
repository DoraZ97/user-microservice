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
    firstName = tasks["firstName"]
    lastName = tasks["lastName"]
    phone = tasks["phone"]
    email = tasks["email"]
    addressID = tasks["addressID"]
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "INSERT INTO " + db_schema + "." + table_name + " (firstName, lastName, phone, email, addressID) VALUES (%s, %s, %s, %s, %s)"
    #sql = "Insert into " + db_schema + "." + table_name + " (ID, firstName, lastName, email, addressID) VALUES (" + id + ",'" + firstName + "','" + lastName + "','" + email + "'," + addressID + ")"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql, (firstName, lastName, phone, email, addressID))
    conn.commit()

    sql1 = "SELECT MAX(ID) as ID FROM " + db_schema + "." + table_name
    res = cur.execute(sql1)
    res = cur.fetchall()
    print(res)

    sql2 = "select * from " + db_schema + "." + table_name + " where ID = %s"
    print(sql2)
    res = cur.execute(sql2, (res[0]["ID"]))
    res = cur.fetchall()
    print(res)
    conn.close()
    return res

def update_address(db_schema, table_name, tasks):
    streetNo = tasks["streetNo"]
    streetName = tasks["streetName"]
    city = tasks["city"]
    region = tasks["region"]
    countryCode = tasks["countryCode"]
    postalCode = tasks["postalCode"]

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "INSERT INTO " + db_schema + "." + table_name + " (streetNo, streetName, city, region, countryCode, postalCode) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (streetNo, streetName, city, region, countryCode, postalCode))
    conn.commit()

    sql1 = "SELECT MAX(ID) as ID FROM " + db_schema + "." + table_name
    res = cur.execute(sql1)
    res = cur.fetchall()
    print(res)

    sql2 = "select * from " + db_schema + "." + table_name + " where ID = %s"
    print(sql2)
    res = cur.execute(sql2, (res[0]["ID"]))
    res = cur.fetchall()
    print(res)

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

def update_email(db_schema, table_name, ID, email):
    conn = _get_db_connection()
    cur = conn.cursor()
    print(ID)
    print(email)

    sql = "Update " + db_schema + "." + table_name + " SET email = %s WHERE ID = %s"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql, (email, ID))
    res = cur.fetchall()
    print(res)

    conn.commit()
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
