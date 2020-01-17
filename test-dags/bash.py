import datetime
from airflow import models
from airflow.contrib.operators import kubernetes_pod_operator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)


with models.DAG(
        dag_id='example-1',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:

    passing = kubernetes_pod_operator.KubernetesPodOperator(
      task_id='passing-task',
      name='passing-test',
      namespace='default',
      image='python:3.6',
      cmds=["python","-c"],
      arguments=["print('hello world')"],
      in_cluster=True
    )