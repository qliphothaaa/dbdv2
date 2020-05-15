from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.email import send_email
from datetime import datetime, timezone, timedelta

email = Variable.get("email", default_var="nanashi.owen@gmail.com")


def local_time():
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)
    tzutc_7 = timezone(timedelta(hours=7))
    local_dt = str(dt.astimezone(tzutc_7))
    return local_dt



def start(dag, dag_name):
    task = EmailOperator(
        task_id='start',  
        to=[email],
        subject="start the %s" % dag_name,
        html_content=f"<h3> Start the {dag_name} at {local_time()}</h3>",
        dag=dag)
    return task


#browser


def getCookies(dag):
    task = BashOperator(
            task_id='get_cookies',
            bash_command="cd /dbdv2 && python3 browser/cookie_browser.py",
            dag=dag)
    return task


#scrapy

def startMonthlyScraping(dag):
    task = BashOperator(
            task_id='monthly_scraping',
            bash_command="cd /dbdv2 && scrapy crawl monthly -a retry=0",
            dag=dag)
    return task

def startAnnuallyScraping(dag, start, end):
    if end and start:
        task = BashOperator(
                task_id='annually_scraping',
                bash_command=f"cd /dbdv2 && scrapy crawl annually -a retry=0 -a start={start} -a end={end}",
                dag=dag)

    else:
        task = BashOperator(
                task_id='annually_scraping',
                bash_command="cd /dbdv2 && scrapy crawl annually -a retry=0",
                dag=dag)
    return task

def datetimeAnnuallyScraping(dag, date):
    task = BashOperator(
            task_id='annually_scraping',
            bash_command=f"cd /dbdv2 && scrapy crawl annually -a retry=-1 -a date={date}",
            dag=dag)
    return task


def scrapingFailedDataAnnually(dag):
    task = BashOperator(
            task_id='retry_annually',
            bash_command="cd /dbdv2 && scrapy crawl annually -a retry=1",
            dag=dag)
    return task

def scrapingFailedData(dag):
    task = BashOperator(
            task_id='retry_monthly',
            bash_command="cd /dbdv2 && scrapy crawl monthly -a retry=1",
            dag=dag)
    return task


#data_access

def loadExcel(dag, url, num):
    task = BashOperator(
            task_id='load_file',
            bash_command=f"cd /dbdv2 && python3 data_access/main.py lf {url} {num}",#
            #on_failure_callback = notify_email,##
            dag=dag)
    return task

def readCSV(dag):
    task = BashOperator(
            task_id='read_csv',
            bash_command="cd /dbdv2 && python data_access/main.py lc 'mdbd.csv' 2000",
            dag=dag)
    return task

'''
def clearMdbd(dag):
    task = BashOperator(
            task_id='clear_mdbd',
            bash_command="cd /dbdv2 && python data_access/run_clear_mdbd.py",
            dag=dag)
    return task

def clearNewQuery(dag):
    task = BashOperator(
            task_id='clear_new_query',
            bash_command="cd /dbdv2 && python data_access/run_clear_new_query.py",
            dag=dag)
    return task
'''


def exportDBMonth(dag):
    task = BashOperator(
            task_id='export_new_data',
            bash_command="cd /dbdv2 && python3 data_access/main.py ed",
            dag=dag)
    return task

def exportDBYear(dag):
    task = BashOperator(
            task_id='export_all_data',
            bash_command="cd /dbdv2 && python3 data_access/main.py eda",
            dag=dag)
    return task



def failedEmail(dag, task):
    task = EmailOperator(
        task_id='%s_failed' % task.task_id,  
        trigger_rule=TriggerRule.ONE_FAILED,
        to=[email],
        subject="Task failed",
        html_content="<h3>task '%s' failed</h3>" % task.task_id,
        dag=dag)
    return task

def successEmail(dag, dag_name):
    task = EmailOperator(
        task_id='success',  
        trigger_rule=TriggerRule.ALL_SUCCESS,
        to=[email],
        subject="The %s success" % dag_name,
        html_content=f"""
        <h3>{dag_name} finished</h3>
        <p> time: {local_time()}<p>
        """,
        dag=dag)
    return task

def notify_email(contextDict, **kwargs):
    print(contextDict)

    title = "Ailter alert: {task_name} failed".format(**contextDict)

    body = """
    Hello, <br>
    <br>
        There is an error in the {task_name} job.<br>
    <br>
    """.format(**contextDict)

    send_email(email, title, body)
