import datetime
from airflow import models
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.operators import dummy_operator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)


with models.DAG(
        dag_id='example-1',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:

    

    passing = kubernetes_pod_operator.KubernetesPodOperator(
      task_id='passing-task',
      name='passing-test',
      namespace='default',
      image='eu.gcr.io/taiyo-239217/dag:fae4885',
      in_cluster=True,
      is_delete_operator_pod=True
    )
