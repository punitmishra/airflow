import datetime
from airflow import models
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.operators import dummy_operator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)


with models.DAG(
        dag_id='example-1',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:

    start = dummy_operator.DummyOperator(
      task_id='run_this_first',
      name='first-test',
      in_cluster=True,
      is_delete_operator_pod=True
    )

    passing = kubernetes_pod_operator.KubernetesPodOperator(
      task_id='passing-task',
      name='passing-test',
      namespace='default',
      image='python:3.6',
      cmds=["python","-c"],
      arguments=["print('hello world')"],
      in_cluster=True,
      is_delete_operator_pod=True
    )

    success = kubernetes_pod_operator.KubernetesPodOperator(
      task_id='success-task',
      name='success-test',
      namespace='default',
      image='python:3.6',
      cmds=["python","-c"],
      arguments=["print('hello By')"],
      in_cluster=True,
      is_delete_operator_pod=True
    )

    t1 = kubernetes_pod_operator.KubernetesPodOperator(
      task_id='t1-task',
      name='t1-test',
      namespace='default',
      image='python:3.6',
      cmds=["python","-c"],
      arguments=["print('hello t1')"],
      in_cluster=True,
      is_delete_operator_pod=True
    )

    t2 = kubernetes_pod_operator.KubernetesPodOperator(
      task_id='t2-task',
      name='t2-test',
      namespace='default',
      image='python:3.6',
      cmds=["python","-c"],
      arguments=["print('hello t2')"],
      in_cluster=True,
      is_delete_operator_pod=True
    )

    end = dummy_operator.DummyOperator(
      task_id='run_this_end',
      name='end-test',
      in_cluster=True,
      is_delete_operator_pod=True
    )

start >> [passing, success] >> [t1, t2]