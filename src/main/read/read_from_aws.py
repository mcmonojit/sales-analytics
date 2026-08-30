from src.main.utils.logger import Logger

logger = Logger()

class S3reader:

    def list_files_s3(self, s3_client, bucket_name,s3_source_directory):

        try:
            response = s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=s3_source_directory
            )
            if 'Contents' in response:
                files_with_absolute_path = [
                    f"s3://{bucket_name}/{obj['Key']}"
                    for obj in response['Contents'] if obj['Key'].endswith('.csv')]
                return files_with_absolute_path
            else:
                return []
        except Exception as e:
            err_msg = f"Error while reading files: {e}"
            logger.error(err_msg)
            raise

#TODO:
# 1. Get a better understanding of exception handling
# 2. Understand utility of raise