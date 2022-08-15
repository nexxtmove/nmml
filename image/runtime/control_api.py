import json
import math
import time

import pandas as pd
import requests
from nmml import config


class ControlApi:
    def __init__(self):
        self.memory_limit_in_mb = 10
        self.url_prefix = 'https://'

        if 'local' in config.BASE_URL() or 'docker' in config.BASE_URL():
            self.url_prefix = 'http://'

        self.api_url = f'{self.url_prefix}{config.BASE_URL()}/api/machine_learning_model'

    def update_expected_results(self, expected_results: int):
        model_id = requests.get(f'{self.api_url}/{config.MODEL_IDENTIFIER()}/get_id/').json()

        requests.patch(f'{self.api_url}/{model_id}/', json={'expected_results': expected_results})

    def send_results(self, results: pd.DataFrame):
        print('Sending results...')
        start = time.time()

        memory_usage = ControlApi.get_memory_usage(results)
        result_count = len(results)

        if memory_usage < self.memory_limit_in_mb:
            batch_size = result_count
        else:
            batch_size = math.ceil(result_count / (math.ceil(memory_usage / self.memory_limit_in_mb) + 1))

        results.reset_index(inplace=True)

        for _, window in results.groupby(results.index // batch_size):
            result_data = json.loads(pd.DataFrame(window).to_json(orient='records'))

            prepared_results = []

            for row in result_data:
                prepared_results.append({
                    'subject_id': row['subject_id'],
                    'result': row,
                })

            requests.post(f'{self.api_url}/{config.MODEL_IDENTIFIER()}/save_results/', json=prepared_results)

        print(
            f'Results sent! Took: {time.time() - start}. Sent {result_count} results ({memory_usage} MB) in {math.ceil(result_count / batch_size)} batches.')

    @staticmethod
    def get_memory_usage(df: pd.DataFrame) -> int:
        """
        Returns the memory usage of a pandas DataFrame in megabytes.
        """
        usage = df.memory_usage(index=True, deep=True).sum()
        return usage / 1e6
