from airflow import DAG
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash_operator import BashOperator


def testdag(dag, taskid, command):
    task = BashOperator(
            task_id=taskid,
            bash_command=command,
            dag=dag)
    return task

def default_options():
    default_args = {
        'owner': 'dbdv2',  
        'start_date': datetime(2020, 2, 2),  
        'retries': 1,  
        'retry_delay': timedelta(seconds=5)  
    }
    return default_args

with DAG(
        'hello',  
        default_args=default_options(),  
        schedule_interval="@once"  
) as d:
    task1 = testdag(d, 'first', 'ls') 
    task2 = testdag(d, 'second', 'date')
    task1 >> task2
    

