import abc
import json
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            return {}

    def save_state(self, state: dict) -> None:
        states: dict = self.retrieve_state()
        states.update(state)
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(states, f)
        except FileNotFoundError:
            pass


class State:

    def __init__(self, storage: BaseStorage):
        self.storage: BaseStorage = storage

    def set_state(self, key: str, value: Any) -> None:
        if value:
            self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        states: dict = self.storage.retrieve_state()

        return states.get(key)
