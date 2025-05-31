import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ENV
ENV = os.getenv("ENV")
if not ENV:
    ENV = "local"
logger.info(f"ENV is {ENV}")

# load Env vars
logger.info(f"./config/{ENV}.env")
load_dotenv(f"./config/{ENV}.env")

FILE_PATH_TMP = os.getenv("FILE_PATH_TMP")
logger.info(FILE_PATH_TMP)

S3_BUCKET = "snail-minh"
REGION = "us-west-2"
S3_BUCKET_IMAGES_URL = "https://s3.us-west-2.amazonaws.com/www.snail.com/public/"
