from datetime import datetime, timedelta
from tasks_generator import *
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator

email = 'nanashi.owen@gmail.com'
year = '2019'
date = '03'
num = '23'

try:
    excel_config = Variable.get("excel_setting", deserialize_json=True)
    email = Variable.get("email")
    year = excel_config['year']
    date = excel_config['date']
    num = excel_config['num']
except:
    pass

def default_options():
    default_args = {
        'owner': 'dbdv2',  
        'start_date': days_ago(2),  
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

    task1 = loadExcel(d, year, date, num)
    task2 = getCookies(d)
    task3 = startScraping(d)

    taskf1 = failedEmail(d, task1)
    taskf2 = failedEmail(d, task2)
    taskf3 = failedEmail(d, task3)

    tasks = successEmail(d, 'monthly_scraping')

    task_start >> task1 >> task2 >> task3 >> tasks

    task1 >> taskf1
    task2 >> taskf2
    task3 >> taskf3






