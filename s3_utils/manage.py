from typing import Optional
from uuid import uuid4
import secrets
import boto3


class S3:
    __client__ = None
    __resource__ = None

    endpoint: str | None = None
    access_key: str | None = None
    secret_key: str | None = None

    def __init__(
        self, endpoint: str, access_key: str, secret_key: str, bucket_name: str
    ) -> None:
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name or secrets.token_hex(6)

        self.__client__ = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        self.__resource__ = boto3.resource(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        self.__bucket__ = self.__resource__.Bucket(self.bucket_name)

    def upload(
        self,
        file: Optional[bytes] = None,
        file_path: Optional[str] = None,
        object_name: Optional[str] = None,
        bucket_name: Optional[str] = None,
        upload_dir: Optional[str] = "",
        ACL: str = "public-read",
        file_path_posix: Optional[str] = "",
    ) -> str:
        if not bucket_name:
            bucket_name = self.bucket_name

        if not object_name:
            object_name = str(uuid4()) + file_path_posix

        destination = upload_dir + object_name
        try:
            if not file and file_path:
                file = open(file_path, "r+").read()
            elif not file and not file_path:
                raise Exception(f"file or file path does not provided.")

            self.__client__.put_object(
                ACL=ACL, Body=file, Key=destination, Bucket=bucket_name
            )
        except Exception as e:
            raise Exception(f"Faild to upload file. {e}")

        return object_name

    def generate_public_link_for_objects(self, object_name: str, exp: int = 3600):
        """
        Paramaeters:
        ------------
        object_name: str
            object name in the bucket with parent directory (if its on sub-directory)
        exp : int
            expires time as seconds
        """
        return self.__client__.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": object_name},
            ExpiresIn=exp,
        )
