import time

from src.settings import logger


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        data = func(*args, **kwargs)
        logger.info(f"Duration for {func.__name__}: {round(time.time() - t1, 4)}")
        return data

    return wrapper


class DictObj:
    """
    We want to convert response of data layers to object instead of dict
    """

    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(
                    self, key, [DictObj(x) if isinstance(x, dict) else x for x in val]
                )
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)
