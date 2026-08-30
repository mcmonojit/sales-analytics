import sys
from fileinput import filename

from pyspark.sql.functions import bucket

from resources.dev import config
from src.main.utils.s3_client import S3ClientManager
from src.main.utils.logger import Logger
from src.main.utils.mysql_client import MySQLClientManager
from src.main.read.read_from_aws import S3reader
import os

# Initialize logger
logger = Logger()

aws_access_key = config.aws_access_key
aws_secret_key = config.aws_secret_key
region_name = config.aws_region_name

s3_client_provider = S3ClientManager(aws_access_key, aws_secret_key, region_name)
s3_client = s3_client_provider.get_client()

response=s3_client.list_buckets()
logger.info(response)
# print(response) #returns the entire response from the list_buckets API call, which includes metadata about each bucket such as creation date and owner information.

# for bucket in response['Buckets']:
#     print(bucket['Name']) #returns just the bucket names in the S3 account


#TODO:
# 1. Check if the local_directory contains files. These files were downloaded from s3 for previous runs of the job.
# 2. Check if any of these files are also present in process_run_status table with status 'I'.
# 3. If they are present in process_run_status with status 'I' - it means last run was unsuccessful and hence those files are still present in local_directory. Log message should be 'Files already present in local_directory. Last run unsuccessful.'
# 4. If they are present in process_run_status with status 'A' - it means last run was successful and those files are still present in local_directory because of some issue in deleting those files after successful run. Log message should be 'Last run successful, but files still present in local_directory. Investigate!'
# 5. If local_directory is empty - it means last run was successful and put log message as 'No files in local_directory. Last run successful.'

local_directory = config.local_directory

if not os.path.exists(local_directory):
    logger.error(f"{local_directory} does not exist. Please check the path. Exiting gracefully...")
    sys.exit(1)

local_files = os.listdir(local_directory)
local_csv_files = [file for file in local_files if os.path.isfile(os.path.join(local_directory, file)) and file.endswith('.csv')]

if local_csv_files:
    query = f"""
                SELECT file_name
                FROM {config.mysql_database}.{config.mysql_table}
                WHERE file_name IN ({str(local_csv_files)[1:-1]}) AND status = 'I'
            """
    logger.info(f"Dynamically prepared query: \n{query}")
    db_client=MySQLClientManager()
    cursor = db_client.get_cursor()
    cursor.execute(query)
    response = cursor.fetchall()
    if response:
        logger.info(f"Files already present in local_directory. Last run unsuccessful.")
    else:
        logger.info(f"Files not found in DB.")

else:
    logger.info("No files in local_directory. Last run successful.")


#TODO:
# 1. get all the absolute path of csv files present in the specific directory of the s3 bucket
# 2. create a spearate class to download the csv files from the s3 bucket location
# 3. next get a list of all files present in local directory after download
# 4. filter only csv files and create their absolute path

try:
    s3_reader = S3reader()
    s3_files_list = s3_reader.list_files_s3(s3_client, config.bucket_name, config.s3_source_directory)
    if s3_files_list:
        logger.info(f"List of csv files in S3 bucket: {s3_files_list}")
    else:
        logger.info(f"No csv files present in folder {config.s3_source_directory}.")
        raise Exception("No data available to process.")
except Exception as e:
    logger.error(f"Process stopped with exception {e}")