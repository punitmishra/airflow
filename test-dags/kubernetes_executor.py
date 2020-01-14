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

        kubernetes_secret_vars_ex = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-kube-secrets',
        name='ex-kube-secrets',
        in_cluster=True,
        namespace='default',
        image='ubuntu',
        startup_timeout_seconds=300)

        passing = kubernetes_pod_operator.KubernetesPodOperator(
          task_id='passing-task',
          name='passing-test',
          in_cluster=True,
          namespace='default',
          image='python:3.6',
          cmds=["python","-c"],
          arguments=["print('hello world')"],
          startup_timeout_seconds=300
        )

        