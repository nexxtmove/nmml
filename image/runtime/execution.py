import time
import pandas as pd
from nmml.model import Model
from runtime.scheduler_patch import Scheduler

from runtime.control_api import ControlApi


class Execution:
    def __init__(self):
        self.control_server = ControlApi()
        self.processing_limit = 60

    def start_scheduler(self):
        scheduler = Scheduler()
        scheduler.every(30).seconds.do(self.control_server.send_heartbeat)
        scheduler.run_continuously()

    def execute_model(self):
        self.control_server.send_heartbeat()
        self.start_scheduler()

        self.available_results = self.control_server.get_processed_results()

        self.__load_model()
        self.__fetch_data()
        self.__process_data()
        self.__predict()

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

        self.features = self.features[~self.features['subject_id'].isin(self.available_results)]

        print('Data processed! Took:', time.time() - start)

    def __predict(self):
        print('Predicting...')
        start = time.time()

        last_save = time.time()
        self.results = pd.DataFrame()

        for index in self.features.index:
            self.results = pd.concat([self.results, self.model.predict(self.features.iloc[[index]], self.arguments)])

            if (time.time() - last_save) > self.processing_limit:
                self.control_server.send_results(self.results)
                self.results = pd.DataFrame()
                last_save = time.time()

        print('Predicted! Took:', time.time() - start)

        self.control_server.send_results(self.results)
