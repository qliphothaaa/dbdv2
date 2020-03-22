from datetime import datetime, timedelta
from tasks_generator import *
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator


excel_config = Variable.get("file_setting", deserialize_json=True, default_var={"filename":"", "num":"0"})


filename = excel_config["filename"]

try:
    num = excel_config["num"]
except:
    num = '0'

try:
    column = excel_config["column"]
except:
    column = ''

def default_options():
    default_args = {
        'owner': 'dbdv2',  
        'start_date': datetime(2020, 2, 2),  
        'retries': 1,  
        'retry_delay': timedelta(seconds=5)  
    }
    return default_args

with DAG(
        'monthly_scraping',  
        default_args=default_options(),  
        schedule_interval="@once"  
) as d:

    task_start = start(d, 'monthly_scraping')

    task0 = clearNewQuery(d)
    task1 = loadExcel(d, filename, num, column)
    task2 = getCookies(d)
    task3 = startMonthlyScraping(d)

    taskf0 = failedEmail(d, task0)
    taskf1 = failedEmail(d, task1)
    taskf2 = failedEmail(d, task2)
    taskf3 = failedEmail(d, task3)

    task_finished = successEmail(d, 'monthly_scraping')

    task_start >>task0 >>  task1 >> task2 >> task3 >> task_finished
    #task_start>>task1>> task2>>task3>>task_finished

    task0 >> taskf0
    task1 >> taskf1
    task2 >> taskf2
    task3 >> taskf3






