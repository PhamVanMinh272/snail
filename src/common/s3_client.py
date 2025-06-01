import base64
import json
from typing import Any

import boto3


class S3Client:
    def __init__(self, bucket_name: str = None):
        # self.region = 1
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name

    def get_object_content(self, object_name: str) -> dict:
        """
        Get file data without download
        :param object_name: file path
        """
        data = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
        data = data["Body"].read().decode("utf-8")
        data = json.loads(data)
        data = data.get("data")
        return data

    def put_object_content(self, object_name: str, body):
        """
        edit file with new content
        :param object_name: file path
        :param body: b-data
        """
        json_data = json.dumps(body)
        self.s3.put_object(
            Body=json_data.encode("utf-8"), Bucket=self.bucket_name, Key=object_name
        )

    def put_image(self, object_name: str, body: bytes):
        image_bytes = base64.b64decode(body)
        # image_bytes = io.BytesIO(image_bytes)
        # image_bytes = body
        self.s3.put_object(
            Body=image_bytes,
            Bucket=self.bucket_name,
            Key=object_name,
            ContentType="image/png",
        )

    def get_image(self, object_name: str) -> bytes:
        """
        object_name: partial s3 url
        Example: /public/f8d43da3-766d-4834-ad3f-3d010245fbbb.jpg
        """
        response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
        image_data = response["Body"].read()
        return image_data

    def remove_image(self, object_name: str):
        """Remove a file on s3"""
        self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)
