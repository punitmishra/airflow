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
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:

        start = dummy_operator.DummyOperator(task_id='run_this_first', dag=dag)

        passing = kubernetes_pod_operator.KubernetesPodOperator(
          task_id='passing-task',
          name='passing-test',
          in_cluster=True,
          namespace='default',
          image='Python:3.6',
          cmds=['Python','-c'],
          arguments=['print('hello world')'],
          startup_timeout_seconds=300
        )


passing.set_upstream(start)

