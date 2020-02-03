from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule

email = 'nanashi.owen@gmail.com'

def start(dag, dag_name):
    task = EmailOperator(
        task_id='start',  
        to=[email],
        subject="start the %s" % dag_name,
        html_content="<h3> Start the %s</h3>" %dag_name,
        dag=dag)
    return task


def loadExcel(dag, year, date, num):
    task = BashOperator(
            task_id='load_excel',
            bash_command="cd /dbdv2 && python3 data_access/load_excel_file.py %s %s %s"% (year, date, num),
            dag=dag)
    return task

def getCookies(dag):
    task = BashOperator(
            task_id='get_cookies',
            bash_command="cd /dbdv2 && python3 browser/cookie_browser.py",
            dag=dag)
    return task

def startScraping(dag):
    task = BashOperator(
            task_id='scraping',
            bash_command="cd /dbdv2 && scrapy crawl dbdv2",
            dag=dag)
    return task

def scrapingFailedData(dag):
    task = BashOperator(
            task_id='retry_scraping',
            bash_command="cd /dbdv2 && scrapy crawl retry",
            dag=dag)
    return task

def failedEmail(dag, task):
    task = EmailOperator(
        task_id='%s_failed' % task.task_id,  
        trigger_rule=TriggerRule.ONE_FAILED,
        to=[email],
        subject="The scraping failed",
        html_content="<h3>task '%s' failed</h3>" % task.task_id,
        dag=dag)
    return task

def successEmail(dag, dag_name):
    task = EmailOperator(
        task_id='success',  
        trigger_rule=TriggerRule.ALL_SUCCESS,
        to=[email],
        subject="The %s success" % dag_name,
        html_content="<h3>%s finished</h3>"% dag_name,
        dag=dag)
    return task
