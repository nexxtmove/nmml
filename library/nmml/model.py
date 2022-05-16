import pandas
from typing import Callable, Any, Dict, Optional
import dill

Arguments = Optional[Dict]


class Model:
    def __init__(self, fetch_data: Callable[[Arguments], Any],
                 process_data: Callable[[Any, Arguments], pandas.DataFrame],
                 predict: Callable[[pandas.DataFrame, Arguments], pandas.DataFrame],
                 arguments: Arguments,
                 version: int = 0):
        self.fetch_data = fetch_data
        self.process_data = process_data
        self.predict = predict
        self.arguments = arguments
        self.version = version

    def save(self, name: str):
        if not name.endswith(".pickle"):
            name += ".pickle"

        dill.dump(self, open(name, "wb"), recurse=True)

    @staticmethod
    def load(name: str) -> "Model":
        return dill.load(open(name, "rb"))
