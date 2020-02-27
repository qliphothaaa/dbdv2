from datetime import datetime, timedelta
from tasks_generator import *
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator


excel_config = Variable.get("excel_setting", deserialize_json=True, default_var={"year":"2019", "month":"03", "num":"0"})

year = excel_config["year"]
month= excel_config["month"]
try:
    num = excel_config["num"]
except:
    num = '100000'

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

    task1 = loadExcel(d, year, month, num)
    task2 = getCookies(d)
    task3 = startMonthlyScraping(d)

    taskf1 = failedEmail(d, task1)
    taskf2 = failedEmail(d, task2)
    taskf3 = failedEmail(d, task3)

    task_finished = successEmail(d, 'monthly_scraping')

    task_start >> task1 >> task2 >> task3 >> task_finished

    task1 >> taskf1
    task2 >> taskf2
    task3 >> taskf3






