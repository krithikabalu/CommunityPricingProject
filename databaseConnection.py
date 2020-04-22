import datetime
from random import random, randint, uniform

from psycopg2 import sql, Error, connect


def create_product_table(conn):
    cur = conn.cursor()
    sql_str = "create table if not exists product (product_id VARCHAR(255) PRIMARY KEY ,name VARCHAR(255), description VARCHAR(255), " \
              "start_date TIMESTAMP, elasticity VARCHAR(255), markup DECIMAL, cost DECIMAL, base_discount DECIMAL, " \
              "promotional_discount DECIMAL, product_classification VARCHAR(255), competitive_intensity VARCHAR(255))"
    sql_resp = cur.execute(sql_str)
    conn.commit()
    cur.close()

def create_price_table(conn):
    cur = conn.cursor()
    sql_str = "create table if not exists price (id VARCHAR(255) REFERENCES product(product_id),price DECIMAL, updated_time TIMESTAMP, " \
              "active BOOL, price_product_unique_id VARCHAR(255))"
    sql_resp = cur.execute(sql_str)
    conn.commit()
    cur.close()

def insert_into_product_table(conn):
    cur = conn.cursor()
    with open('product-names', 'r') as f:
        product_names = f.read().split('\n')
    elasticities = ['highly-elastic', 'medium-elastic', 'medium-inelastic', 'highly-inelastic']
    competitive_intensities = ['highly-competitive', 'competitive', 'captive', 'highly-captive']
    product_classifications = ['category-A', 'category-B', 'category-C', 'category-D']
    records = []
    for index, product_name in enumerate(product_names):
        new_record = {'elasticity': elasticities[randint(0, len(elasticities) - 1)],
                      'competitive_intensity': competitive_intensities[
                        randint(0, len(competitive_intensities) - 1)],
                      'product_id': "p" + str(index),
                      'description': "This describes " + product_name,
                      'markup': uniform(0, 10),
                      'base_discount': uniform(0, 10),
                      'promotional_discount': uniform(0, 10),
                      'product_classification': product_classifications[
                        randint(0, len(product_classifications) - 1)],
                      'cost': uniform(100, 5000),
                      'start_date': (datetime.datetime.now() - datetime.timedelta(days=randint(1, 1000))).strftime("%Y-%m-%d")}
        records.append(new_record)
    insert_the_records(conn, cur, records, 'product')

def insert_into_price_table(conn):
    cur = conn.cursor()
    with open('product-names', 'r') as f:
        product_names = f.read().split('\n')
    booleanValue = ['true', 'false']
    records = []
    for index, product_name in enumerate(product_names):
        product_id = "p" + str(index)
        price = uniform(100, 5000)
        price_product_unique_id = product_id+str(price)
        new_record = {'product_id': product_id,
                      'price': price,
                      'updated_time': (datetime.datetime.now() - datetime.timedelta(days=randint(1, 1000))).strftime("%Y-%m-%d"),
                      'active': booleanValue[
                        randint(0, len(booleanValue) - 1)],
                      'price_product_unique_id': price_product_unique_id
                      }
        records.append(new_record)
    insert_the_records(conn, cur, records, 'price')


def insert_the_records(conn, cur, records, table_name):
    insert_sql_statement = create_insert_records(records, table_name)
    cur.execute(insert_sql_statement)
    conn.commit()
    cur.close()


def create_insert_records( json_array, table_name ):
    columns = json_array[0].keys()
    print ("\ncolumns:", columns)
    sql_string = "INSERT INTO {}".format(table_name)
    sql_string = sql_string + " (" + ', '.join(columns) + ")\nVALUES "
    record_list = []

    for i, record in enumerate( json_array ):
        values = record.values()
        record = list(values)
        print(record)

        for i, val in enumerate(record):
            if type(val) == str:
                if "'" in val:
                    record[i] = "E'" + record[i].replace("'", "''") + "'"

        record = str(record).replace("[", '')
        record = record.replace("]", '')
        record = record.replace('"', '')
        record_list += [record]

    for i, record in enumerate(record_list):
        sql_string = sql_string + "(" + record + "),\n"

    sql_string = sql_string[:-2] + ";"
    return sql_string


try:
    conn = connect(
        dbname="pricing",
        user="postgres",
        host="localhost",
        password="password",
        # attempt to connect for 3 seconds then raise exception
        connect_timeout=3
    )

    # create_product_table(conn)
    # insert_into_product_table(conn)
    create_price_table(conn)
    insert_into_price_table(conn)


except Error as err:
    print("\npsycopg2 connect error:", err)
    conn = None
    cur = None
