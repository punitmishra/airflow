from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount


volume_mount = VolumeMount('persist-disk',
                           mount_path='/files',
                           sub_path=None,
                           read_only=False)

volume_config= {
    'persistentVolumeClaim':
    {
        'claimName': 'persist-pods-disk-claim' # uses the persistentVolumeClaim given in the Kube yaml
    }
}
volume = Volume(name='persist-disk', configs=volume_config)


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


start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(namespace='default',
                          image="Python:3.6",
                          cmds=["Python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          name="passing-test",
                          task_id="passing-task",
						  volumes=[volume],
                          volume_mounts=[volume_mount],
                          get_logs=True,
                          dag=dag
                          )

passing.set_upstream(start)
