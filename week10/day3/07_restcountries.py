from airflow import DAG
from airflow.decorators import task
# from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import datetime

import requests
import json
import logging


def get_Redshift_connection(autocommit=True):
    hook = ... #PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


@task
def get_countries_info():
    ## Extract + Transform
    data = requests.get("https://restcountries.com/v3/all").text
    countries = json.loads(data)
    records = []

    for country in countries:
        temp = {
            "name" : country["name"]["official"],
            "population" : country["population"],
            "area" : country["area"]
        }
        records.append(temp)
    return records


@task
def load(schema, table, records):
    logging.info("load")
    cur = get_Redshift_connection()

    try:
        cur.execute("BEGIN;")
        _create_table(cur, schema, table, False)
        cur.execute(f"CREATE TEMP TABLE t AS SELECT * FROM {schema}.{table};")
        
        for record in records:
            sql = f"""
                INSERT INTO t (country_name, population, area) VALUES
                (%s, %s, %s)
            """
            values = (record["name"], record["population"], record["area"])
            print(cur.mogrify(sql, values))
            cur.execute(sql, values)
        
        _create_table(cur, schema, table, True)
        cur.execute(f"INSERT INTO {schema}.{table} SELECT DISTINCT * FROM t;")
        cur.execute("COMMIT;")
    except Exception as error:
        print(error)
        cur.execute("ROLLBACK;")
        raise

    logging.info("load done")

def _create_table(cur, schema, table, drop_first):
    if drop_first:
        cur.execute(f"DROP TABLE IF EXISTS {schema}.{table};")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.{table} (
            country_name varchar(100),
            population bigint,
            area float
        );
        """)

with DAG(
    dag_id = 'RestCountry',
    start_date = datetime(2024, 4, 30),
    catchup=False,
    tags=["API"],
    schedule='30 6 * * 6'
) as dag:
    
    results = get_countries_info()
    load("cjswldn99", "rest_country", results)

