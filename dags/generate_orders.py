import random
import uuid
import os
from datetime import datetime, timedelta

import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator


def generate_orders():
    conn = psycopg2.connect(
        host="postgres-1",
        database=os.getenv("POSTGRES_DB_1"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    cur = conn.cursor()

    currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF"]
    for _ in range(5000):
        order_id = uuid.uuid4()
        customer_email = f"customer_{random.randint(1, 1000)}@example.com"
        order_date = datetime.now() - timedelta(days=random.randint(0, 7))
        amount = round(random.uniform(1, 1000), 2)
        currency = random.choice(currencies)

        cur.execute(
            """
            INSERT INTO orders (order_id, customer_email, order_date, amount, currency)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (str(order_id), customer_email, order_date, amount, currency),
        )

    conn.commit()
    cur.close()
    conn.close()


with DAG(
        dag_id="generate_orders",
        schedule_interval="*/10 * * * *",
        start_date=datetime(2023, 10, 26),
        catchup=False,
) as dag:
    generate_orders_task = PythonOperator(
        task_id="generate_orders",
        python_callable=generate_orders,
    )
