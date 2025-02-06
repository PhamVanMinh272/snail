from abc import ABC, abstractmethod


class BaseService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_list(self, **kwargs) -> list:
        pass

    @abstractmethod
    def create(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def update(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def delete(self, **kwargs) -> dict:
        pass
