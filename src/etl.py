"""Class-based ETL for SpaceX launches"""
from typing import List, Dict
import requests
import pandas as pd
from io import BytesIO
import pyarrow as pa
import pyarrow.parquet as pq
import os
import boto3


class SpaceXETL:
    
    def __init__(self, s3_bucket: str, s3_key: str = "launches.parquet", s3_client=None):
        self.api_url = os.getenv('SpaceXETLURL')+"/v4/launches"
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_client = s3_client or boto3.client('s3')
    
    """Class-based ETL for SpaceX launches"""
    def fetch(self) -> List[Dict]:
        """Fetch launches JSON from SpaceX API."""
        resp = requests.get(self.api_url, timeout=30)
        resp.raise_for_status()
        return resp.json()


    def transform(self, data: List[Dict]) -> pd.DataFrame:
        """Apply rules: select & rename fields, extract nested links.webcast."""
        rows = []
        for item in data:
            row = {
                'flight_number': item.get('flight_number'),
                'mission_name': item.get('name'),
                'launch_date': item.get('date_utc'),
                'mission_successful': item.get('success'),
                'webcast_url': None,
            }
            # Extract nested link safely
            links = item.get('links') or {}
            row['webcast_url'] = links.get('webcast')
            rows.append(row)
        df = pd.DataFrame(rows)
        # enforce column order
        df = df[[
            'flight_number',
            'mission_name',
            'launch_date',
            'mission_successful',
            'webcast_url'
        ]]
        return df


    def to_parquet_bytes(self, df: pd.DataFrame) -> bytes:
        """Convert DataFrame to parquet bytes using pyarrow."""
        table = pa.Table.from_pandas(df)
        buf = BytesIO()
        pq.write_table(table, buf)
        buf.seek(0)
        return buf.read()


    def save_to_s3(self, parquet_bytes: bytes) -> None:
        """Upload parquet bytes to S3."""
        self.s3_client.put_object(Bucket=self.s3_bucket, Key=self.s3_key, Body=parquet_bytes)


    def run(self) -> pd.DataFrame:
        """Full pipeline: fetch -> transform -> upload. Returns DataFrame for convenience."""
        data = self.fetch()
        df = self.transform(data)
        parquet = self.to_parquet_bytes(df)
        self.save_to_s3(parquet)
        return df