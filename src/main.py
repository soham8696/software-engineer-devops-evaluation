from etl import SpaceXETL
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    bucket = os.getenv('S3_BUCKET', 'candidate-test-bucket2k25')
    key = os.getenv('AWS_ACCESS_KEY_ID', 'launches.parquet')
    etl = SpaceXETL(s3_bucket=bucket)
    df = etl.run()
    print(f"Uploaded {len(df)} rows to s3://{bucket}/{key}")

if __name__ == '__main__':
    main()