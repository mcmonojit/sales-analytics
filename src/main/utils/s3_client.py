import boto3
from resources.dev import config

class S3ClientManager:
    def __init__(self, aws_access_key=None, aws_secret_key=None, region_name=None):
        # Use provided keys or fall back to config values
        self.aws_access_key = aws_access_key or config.aws_access_key # Instance attribute
        self.aws_secret_key = aws_secret_key or config.aws_secret_key # Instance attribute
        self.region_name = region_name or config.aws_region_name # Instance attribute
        # Create a boto3 client using the instance attributes
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region_name
        )

    # Method to get the S3 client
    def get_client(self):
        return self.s3_client

    # def list_buckets(self):
    #     # Access the instance's s3_client
    #     return self.s3_client.list_buckets()



# Main Arguments for boto3.client()
# boto3.client(
#     service_name,  # Required: AWS service name (e.g., 's3', 'ec2', 'dynamodb')
#     region_name=None,  # AWS region (e.g., 'us-east-1', 'ap-south-2')
#     api_version=None,  # Specific API version
#     use_ssl=True,  # Use HTTPS (True by default)
#     verify=True,  # SSL verification
#     endpoint_url=None,  # Custom endpoint URL
#     aws_access_key_id=None,  # AWS Access Key ID
#     aws_secret_access_key=None,  # AWS Secret Access Key
#     aws_session_token=None,  # Temporary session token (for MFA or temporary credentials)
#     config=None  # Botocore config object
# )
