import base64
import json
import io

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
        self.s3.put_object(Body=image_bytes, Bucket=self.bucket_name, Key=object_name)
