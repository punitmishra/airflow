from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators import dummy_operator
from airflow.utils.dates import days_ago
import datetime
from airflow import models
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators import kubernetes_pod_operator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)


with models.DAG(
        dag_id='kubernetes_sample',
        schedule_interval='0 0 * * *',
        start_date=days_ago(2),
        dagrun_timeout=timedelta(minutes=60)) as dag:

        start = dummy_operator.DummyOperator(
          task_id='run_this_first',
          name='first-test',
          is_delete_operator_pod=True,
          in_cluster=True
        )

        passing = kubernetes_pod_operator.KubernetesPodOperator(
          task_id='passing-task',
          name='passing-test',
          in_cluster=True,
          namespace='default',
          image='python:3.6',
          cmds=["python","-c"],
          arguments=["print('hello world')"],
          is_delete_operator_pod=True,
          startup_timeout_seconds=300
        )

        success = kubernetes_pod_operator.KubernetesPodOperator(
          task_id='success-task',
          name='success-test',
          in_cluster=True,
          namespace='default',
          image='python:3.6',
          cmds=["python","-c"],
          arguments=["print('hello abhi')"],
          is_delete_operator_pod=True,
          startup_timeout_seconds=300
        )

passing.set_upstream(start)
success.set_upstream(start)       