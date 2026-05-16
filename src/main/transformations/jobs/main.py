from resources.dev import config
from src.main.utils.s3_client import S3ClientManager
from src.main.utils.logger import Logger

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


# TODO:
# 1. Check if the local_directory contains files. These files were downloaded from s3 for previous runs of the job.
# 2. Check if any of these files are also present in process_run_status table with status 'I'.
# 3. If they are present in process_run_status with status 'I' - it means last run was unsuccessful and hence those files are still present in local_directory. Log message should be 'Files already present in local_directory. Last run unsuccessful.'
# 4. If they are present in process_run_status with status 'A' - it means last run was successful and those files are still present in local_directory because of some issue in deleting those files after successful run. Log message should be 'Last run successful, but files still present in local_directory. Investigate!'
# 5. If local_directory is empty - it means last run was successful and put log message as 'No files in local_directory. Last run successful.'