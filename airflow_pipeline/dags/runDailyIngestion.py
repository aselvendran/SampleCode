from airflow import DAG
import datetime

from airflow.operators.python_operator import PythonOperator
import operators.runSurveyData as rsd



#
args = {
    'owner': 'aselvendran',
    'start_date': datetime.datetime(2020, 10, 21),
    'catchup':False,
    'depends_on_past': False,

}

main_dag_id = 'userSurvey'

dag = DAG(
    main_dag_id,
    schedule_interval='23 9 * * *',
    default_args=args, )

getAndFormatData = PythonOperator(
    task_id='get_and_format_data',
    dag=dag,
    python_callable=rsd.getAndFormatDataSaveS3)



getAndFormatData
