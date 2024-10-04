import boto3
from botocore.exceptions import ClientError
from config.settings import get_settings

settings = get_settings()


class FileManager:
    _client = boto3.client(
        "s3",
        endpoint_url=settings.OBJECT_STORAGE_URI,
        aws_access_key_id=settings.OBJECT_STORAGE_ACCESS_KEY,
        aws_secret_access_key=settings.OBJECT_STORAGE_SECRET_KEY,
        config=boto3.session.Config(signature_version="s3v4"),
    )

    @classmethod
    def upload(cls, file_data, bucket_name: str, file_name: str):
        """
        Uploads a file to the specified S3 bucket.
        :param file_data: File data (can be a file-like object or bytes)
        :param bucket_name: S3 bucket name
        :param file_name: Name to store the file as in S3
        """
        try:
            cls._client.upload_fileobj(file_data, bucket_name, file_name)
            return cls.detail(bucket_name, file_name)
        except ClientError as e:
            return f"Failed to upload file '{file_name}' to bucket '{bucket_name}': {str(e)}"

    @classmethod
    def detail(cls, bucket_name: str, file_name: str):
        """
        Retrieves metadata of a specific file from the S3 bucket.
        :param bucket_name: S3 bucket name
        :param file_name: Name of the file in S3
        """
        try:
            response = cls._client.head_object(Bucket=bucket_name, Key=file_name)
            return response
        except ClientError as e:
            return f"Failed to retrieve file details for '{file_name}' from bucket '{bucket_name}': {str(e)}"

    @classmethod
    def list(cls, bucket_name: str, prefix: str = ""):
        """
        Lists all files in a specified S3 bucket or with a specific prefix.
        :param bucket_name: S3 bucket name
        :param prefix: Prefix to filter files
        """
        try:
            response = cls._client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            return response.get("Contents", [])
        except ClientError as e:
            return f"Failed to list files in bucket '{bucket_name}': {str(e)}"

    # TODO: 사용자 직접 download 가능하도록 설정
    @classmethod
    def download(cls, bucket_name: str, file_name: str, download_path: str):
        """
        Downloads a file from the S3 bucket to the specified local path.
        :param bucket_name: S3 bucket name
        :param file_name: Name of the file in S3
        :param download_path: Local path where the file should be saved
        """
        try:
            cls._client.download_file(bucket_name, file_name, download_path)
            return f"File '{file_name}' downloaded successfully to '{download_path}'."
        except ClientError as e:
            return f"Failed to download file '{file_name}' from bucket '{bucket_name}': {str(e)}"

    @classmethod
    def get_object(cls, bucket_name: str, file_name: str):
        try:
            return cls._client.get_object(Bucket=bucket_name, Key=file_name)
        except ClientError as e:
            return f"Failed to download file '{file_name}' from bucket '{bucket_name}': {str(e)}"

    @classmethod
    def delete(cls, bucket_name: str, file_name: str):
        """
        Deletes a specific file from the S3 bucket.
        :param bucket_name: S3 bucket name
        :param file_name: Name of the file in S3
        """
        try:
            cls._client.delete_object(Bucket=bucket_name, Key=file_name)
            return f"File '{file_name}' deleted successfully from bucket '{bucket_name}'."
        except ClientError as e:
            return f"Failed to delete file '{file_name}' from bucket '{bucket_name}': {str(e)}"
