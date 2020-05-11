import datetime
from random import randint, uniform
from psycopg2 import Error, connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

global cost_dict
global datetime_dict
datetime_dict = {}
cost_dict = {}

def create_product_table(connection):
    cursor = connection.cursor()
    sql_str = "create table if not exists product (product_id integer PRIMARY KEY ,name VARCHAR(255), description VARCHAR(255), " \
              "start_date TIMESTAMP, elasticity VARCHAR(255), markup DECIMAL, cost DECIMAL, base_discount DECIMAL, " \
              "promotional_discount DECIMAL, product_classification VARCHAR(255), competitive_intensity VARCHAR(255))"
    cursor.execute(sql_str)
    connection.commit()
    cursor.close()


def create_price_table(connection):
    cursor = connection.cursor()
    sql_str = "create table if not exists price (product_id integer REFERENCES product(product_id),price DECIMAL, updated_time TIMESTAMP, " \
              "active BOOL, price_product_unique_id VARCHAR(255))"
    cursor.execute(sql_str)
    connection.commit()
    cursor.close()


def create_customer_table(connection):
    cursor = connection.cursor()
    sql_str = "create table if not exists customer (customer_id VARCHAR(255) primary key, name VARCHAR(255))"
    cursor.execute(sql_str)
    connection.commit()
    cursor.close()

def insert_into_product_table(connection):
    cursor = connection.cursor()
    with open('product-names', 'r') as f:
        product_names = f.read().split('\n')
    elasticities = ['highly-elastic', 'medium-elastic', 'medium-inelastic', 'highly-inelastic']
    competitive_intensities = ['highly-competitive', 'competitive', 'captive', 'highly-captive']
    product_classifications = ['category-A', 'category-B', 'category-C', 'category-D']
    records = []
    for index, product_name in enumerate(product_names):
        product_id = index + 1
        cost = round(uniform(100, 5000), 2)
        cost_dict[product_id] = cost
        datetime_dict[product_id] = (datetime.datetime.now() - datetime.timedelta(days=randint(1, 1000)))
        new_record = {'elasticity': elasticities[randint(0, len(elasticities) - 1)],
                      'competitive_intensity': competitive_intensities[
                          randint(0, len(competitive_intensities) - 1)],
                      'product_id': list(datetime_dict.keys())[index],
                      'description': "This describes " + product_name,
                      'markup': round(uniform(0, 10), 2),
                      'base_discount': round(uniform(0, 10), 2),
                      'promotional_discount': round(uniform(0, 10), 2),
                      'product_classification': product_classifications[
                          randint(0, len(product_classifications) - 1)],
                      'cost': cost_dict[product_id],
                      'start_date': datetime_dict[product_id].strftime(
                          "%Y-%m-%d")}
        records.append(new_record)
    insert_the_records(connection, cursor, records, 'product')


def insert_into_price_table(connection):
    cursor = connection.cursor()
    with open('product-names', 'r') as f:
        product_names = f.read().split('\n')
    boolean_value = ['true', 'false']
    records = []
    for index in range(0, len(product_names)):
        product_id = index + 1
        price = round(uniform(100, 5000), 2)
        price_product_unique_id = str(product_id) + '-' + str(price)
        new_record = {'product_id': list(datetime_dict.keys())[index],
                      'price': (cost_dict[product_id]+randint(0, 50)),
                      'updated_time': (datetime_dict[product_id] + datetime.timedelta(days=randint(1, 1000))).strftime(
                          "%Y-%m-%d"),
                      'active': boolean_value[
                          randint(0, len(boolean_value) - 1)],
                      'price_product_unique_id': price_product_unique_id
                      }
        records.append(new_record)
    insert_the_records(connection, cursor, records, 'price')


def insert_into_customer_table(connection):
    cursor = connection.cursor()
    with open('customer-names', 'r') as f:
        customer_names = f.read().split('\n')
    records = []
    for index in range(0, len(customer_names)):
        new_record = {
            'customer_id' : "c" + str(index),
            'name' : customer_names[index]
        }
        records.append(new_record)
    insert_the_records(connection, cursor, records, 'customer')

    
def insert_the_records(connection, cursor, records, table_name):
    insert_sql_statement = create_insert_records(records, table_name)
    cursor.execute(insert_sql_statement)
    connection.commit()
    cursor.close()


def create_insert_records(json_array, table_name):
    columns = json_array[0].keys()
    sql_string = "INSERT INTO {}".format(table_name)
    sql_string = sql_string + " (" + ', '.join(columns) + ")\nVALUES "
    record_list = []

    for i, record in enumerate(json_array):
        values = record.values()
        record = list(values)

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


def create_pricing_database(connection):
    cursor = connection.cursor()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    sql_str = "create database pricing"
    cursor.execute(sql_str)
    cursor.close()


try:
    init_connection = connect(
        user="postgres",
        host="localhost",
        password="password",
        connect_timeout=3
    )
    create_pricing_database(init_connection)
    init_connection.close()

    pricing_connection = connect(
        dbname="pricing",
        user="postgres",
        host="localhost",
        password="password",
        connect_timeout=3
    )

    create_product_table(pricing_connection)
    insert_into_product_table(pricing_connection)
    create_price_table(pricing_connection)
    insert_into_price_table(pricing_connection)
    create_customer_table(pricing_connection)
    insert_into_customer_table
    pricing_connection.close()


except Error as err:
    print("\npsycopg2 connect error:", err)
