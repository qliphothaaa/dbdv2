from datetime import datetime, timedelta
from tasks_generator import *
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator


def default_options():
    default_args = {
        'owner': 'dbdv2',  
        'start_date': datetime(2020, 2, 2),  
        'retries': 1,  
        'retry_delay': timedelta(seconds=5)  
    }
    return default_args

def testdag(dag, taskid, command):
    task = BashOperator(
            task_id=taskid,
            bash_command=command,
            dag=dag)
    return task

with DAG(
        'export_database_monthly',  
        default_args=default_options(),  
        schedule_interval="@once"  
) as d:

    task_start = start(d, 'export_database')

    task1 = readCSV(d)
    task2 = exportDBMonth(d)

    taskf1 = failedEmail(d, task1)
    taskf2 = failedEmail(d, task2)

    task_finished = successEmail(d, 'export_database')

    task_start >> task1 >> task2 >> task_finished

    task1 >> taskf1
    task2 >> taskf2


