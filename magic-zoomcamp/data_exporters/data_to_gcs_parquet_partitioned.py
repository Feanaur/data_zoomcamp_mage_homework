from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/personal.json'
project_id = 'datacamp-413216'
bucket_name = 'datacamp-21937-mage'
table_name = 'ny_green_taxi_data'

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data_to_google_cloud_storage(data: DataFrame, **kwargs) -> None:

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table=table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
