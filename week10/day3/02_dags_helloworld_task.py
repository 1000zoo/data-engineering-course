## 01_dags_helloworld.py와 동일한 일을 하는 코드

from airflow import DAG
from airflow.decorators import task
from datetime import datetime

@task
def print_hello():
    print("hello!")
    return "hello!"

@task
def print_goodbye():
    print("goodbye!")
    return "goodbye!"

with DAG(
    dag_id = 'HelloWorld_v2',
    start_date = datetime(2022,5,5),
    catchup=False,
    tags=['example'],
    schedule = '0 2 * * *'
) as dag:


    print_hello() >> print_goodbye()