import time
from nmml.model import Model

from runtime.control_api import ControlApi


class Execution:
    def __init__(self):
        self.control_server = ControlApi()

    def execute_model(self):
        self.__load_model()
        self.__fetch_data()
        self.__process_data()
        self.__predict()

        self.control_server.send_results(self.results)

    def __load_model(self):
        print('Loading model...')
        start = time.time()

        self.model = Model.load('repository/model.pickle')
        self.arguments = self.model.arguments

        print('Model loaded! Took:', time.time() - start)

    def __fetch_data(self):
        print('Fetching data...')
        start = time.time()

        self.data = self.model.fetch_data(self.arguments)

        print('Data fetched! Took:', time.time() - start)

    def __process_data(self):
        print('Processing data...')
        start = time.time()

        self.features = self.model.process_data(self.data, self.arguments)

        self.control_server.update_expected_results(len(self.features))

        print('Data processed! Took:', time.time() - start)

    def __predict(self):
        print('Predicting...')
        start = time.time()

        self.results = self.model.predict(self.features, self.arguments)

        print('Predicted! Took:', time.time() - start)
