from airflow import DAG
import datetime

from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
import operators.createDatabaseConn as cdc
from airflow.hooks.postgres_hook import PostgresHook
from psycopg2.extras import execute_values



def loadToStagingTable(conn_id, prod_table, staging_table, *args, **kwargs):
    query = """
        SELECT *
        FROM %s
            """ % prod_table

    prod_conn = PostgresHook(postgres_conn_id='production_db',
                               schema='production_db').get_conn()
    staging_conn = PostgresHook(postgres_conn_id=conn_id,
                             schema=conn_id).get_conn()

    prod_cursor = prod_conn.cursor("prodCursor")
    prod_cursor.execute(query)
    staging_cursor = staging_conn.cursor()

    while True:
        records = prod_cursor.fetchmany(size=2000)
        if not records:
            break
        execute_values(staging_cursor,
                       f"INSERT INTO {staging_table} VALUES %s",
                       records)
        staging_conn.commit()

    prod_cursor.close()
    staging_cursor.close()
    prod_conn.close()
    staging_conn.close()


def loadToStagingTableLoop(conn_id, *args, **kwargs):
    analytics_db = {"public.address_analytic": "public.address", "public.account_analytics": "public.account",
                    "public.statement_analytics": "public.statement"}
    dev_db = {"public.address_dev": "public.address", "public.account_dev": "public.account",
              "public.statement_dev": "public.statement"}
    if conn_id == "analytics_staging_db":
        for key in analytics_db.keys():
            loadToStagingTable(conn_id, key, analytics_db[key])
    elif conn_id == "dev_staging_db":
        for key in dev_db.keys():
            loadToStagingTable(conn_id, key, dev_db[key])


args = {
    'owner': 'aselvendran',
    'start_date': datetime.datetime(2020, 1, 15),
    'depends_on_past': False,

}

main_dag_id = 'productionToStaging'

dag = DAG(
    main_dag_id,
    schedule_interval='23 9 * * *',
    catchup=False,
    start_date=datetime.datetime(2020, 2, 1),
    template_searchpath='/usr/local/airflow/sql',
    default_args=args
)

addConn = PythonOperator(
    task_id='addDBConnections',
    dag=dag,
    python_callable=cdc.updateOperators)

t1 = PostgresOperator(
    task_id='insert_analytics_staging_tb_snapshot',
    postgres_conn_id='production_db',
    sql='staging_analytics_insert.sql')

t2 = PostgresOperator(
    task_id='insert_dev_staging_tb_snapshot',
    postgres_conn_id='production_db',
    sql='staging_dev_insert.sql')

t4 = PostgresOperator(
    task_id='create_tables_staging_dev',
    postgres_conn_id='dev_staging_db',
    sql='create_dev_staging_tables.sql')

t5 = PostgresOperator(
    task_id='create_tables_staging_analytics',
    postgres_conn_id='analytics_staging_db',
    sql='create_analytics_staging_tables.sql')





analytics_unload = PythonOperator(
    task_id='unload_data_into_analytics_staging_db',
    provide_context=True,
    python_callable=loadToStagingTableLoop,
    op_args=['analytics_staging_db'],
    dag=dag)

dev_unload = PythonOperator(
    task_id='unload_data_into_cev_staging_db',
    provide_context=True,
    python_callable=loadToStagingTableLoop,
    op_args=['dev_staging_db'],
    dag=dag)

addConn >> t1 >> t2 >> [t4, t5] >> analytics_unload >> dev_unload
