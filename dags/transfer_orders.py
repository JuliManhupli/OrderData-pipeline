import os
from datetime import datetime

import psycopg2
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator


def transfer_and_convert_orders():
    conn_src = psycopg2.connect(
        host="postgres-1",
        database=os.getenv("POSTGRES_DB_1"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    cur_src = conn_src.cursor()

    conn_dest = psycopg2.connect(
        host="postgres-2",
        database=os.getenv("POSTGRES_DB_2"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur_dest = conn_dest.cursor()

    cur_src.execute("SELECT order_id, customer_email, order_date, amount, currency FROM orders")
    orders = cur_src.fetchall()

    api_key = os.getenv("OPENEXCHANGERATES_API_KEY")
    response = requests.get(
        f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    )
    rates = response.json()["rates"]

    for order in orders:
        order_id, customer_email, order_date, amount, currency = order

        if currency != "EUR":
            eur_rate = rates["EUR"] / rates[currency]
            amount_eur = round(amount * eur_rate, 2)
        else:
            amount_eur = amount

        cur_dest.execute(
            """
            INSERT INTO orders_eur (order_id, customer_email, order_date, amount_eur)
            VALUES (%s, %s, %s, %s)
            """,
            (order_id, customer_email, order_date, amount_eur),
        )

    conn_dest.commit()
    cur_src.close()
    conn_src.close()
    cur_dest.close()
    conn_dest.close()


with DAG(
        dag_id="transfer_and_convert_orders",
        schedule_interval="0 * * * *",
        start_date=datetime(2023, 10, 26),
        catchup=False,
) as dag:
    transfer_and_convert_orders_task = PythonOperator(
        task_id="transfer_and_convert_orders",
        python_callable=transfer_and_convert_orders,
    )
