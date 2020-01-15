from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators import dummy_operator
from airflow.utils.dates import days_ago
import datetime
from airflow import models
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators import kubernetes_pod_operator

with models.DAG(
    dag_id = 'kubernetes_sample',
    schedule_interval = '0 0 * * *',
    start_date = days_ago(2),
    dagrun_timeout = timedelta(minutes = 60)) as dag:

  start = dummy_operator.DummyOperator(
    task_id = 'run_this_first',
    name = 'first-test',
    in_cluster = True
  )

passing = kubernetes_pod_operator.KubernetesPodOperator(
  task_id = 'passing-task',
  name = 'passing-test',
  in_cluster = True,
  namespace = 'default',
  image = 'python:3.6',
  cmds = ["python", "-c"],
  arguments = ["print('hello world')"],
  startup_timeout_seconds = 300
)

failing = kubernetes_pod_operator.KubernetesPodOperator(
  task_id = 'failing-task',
  name = 'failing-test',
  in_cluster = True,
  namespace = 'default',
  image = 'ubuntu:1604',
  cmds = ["python", "-c"],
  arguments = ["print('hello world')"],
  startup_timeout_seconds = 300
)

passing.set_upstream(start
failing.set_upstream(start)