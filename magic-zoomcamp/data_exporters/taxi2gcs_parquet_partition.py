from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/gcp_service_account_key.json'
project_id = os.getenv('GCP_PROJECT_ID', None)
bucket_name = os.getenv('GCP_BUCKET_NAME', None)
table_name = 'ny_taxi_data'

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data_to_google_cloud_storage(data: DataFrame, **kwargs) -> None:
    """
    """
    data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date

    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table=table,
        root_path=root_path,
        partition_cols=['tpep_pickup_date'],
        filesystem=gcs
    )
