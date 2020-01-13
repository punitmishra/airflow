from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='kubernetes_sample',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60)
)

volume_mount = VolumeMount('airflow-logs',
                           mount_path='/',
                           sub_path=None,
                           read_only=False)

volume_config= {
    'persistentVolumeClaim':
    {
        'claimName': 'airflow-logs' # uses the persistentVolumeClaim given in the Kube yaml
    }
}

volume = Volume(name="airflow-logs", configs=volume_config)


start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(namespace='default',
                          image="Python:3.6",
                          cmds=["Python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          name="passing-test",
                          task_id="passing-task",
                          volume=[volume],
                          volume_mounts=[volume_mount],
                          get_logs=True,
                          dag=dag
                          )

failing = KubernetesPodOperator(namespace='default',
                          image="ubuntu:1604",
                          cmds=["Python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          name="fail",
                          task_id="failing-task",
                          get_logs=True,
                          dag=dag
                          )

passing.set_upstream(start)
failing.set_upstream(start)
