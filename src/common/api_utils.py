import json

from pydantic import ValidationError

from src.common.exceptions import FileS3NotFound, AlreadyExist, NotFound, InvalidData
from src.common.func_responses import make_error_response, make_success_response
from src.services.image import logger


def exception_handler(func):
    def wrapper(event, context):
        try:
            data = func(event, context)
            return make_success_response(data)
        except (AlreadyExist, InvalidData) as e:
            logger.exception(e)
            return make_error_response(str(e), 400)
        except NotFound as e:
            logger.exception(e)
            return make_error_response(str(e), 404)
        except FileS3NotFound as e:
            logger.exception(e)
            return make_error_response(str(e), 500)
        except ValidationError as e:
            logger.exception(e)
            json_data = json.loads(e.json())[0]
            msg = json_data["loc"][0] + " " + json_data["msg"]
            return make_error_response(msg, 400)
        except Exception as e:
            logger.exception(e)
            return make_error_response(str(e), 500)

    return wrapper
