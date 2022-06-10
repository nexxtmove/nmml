from nmml.model import Model
from nmml import config
import time
import requests
import json
import math
import pandas as pd

memory_limit_in_mb = 10


def get_memory_usage(df: pd.DataFrame) -> int:
    """
    Returns the memory usage of a pandas DataFrame in megabytes.
    """
    usage = df.memory_usage(index=True, deep=True).sum()
    return usage / 1e6


url_prefix = 'https://'

if 'local' in config.BASE_URL() or 'docker' in config.BASE_URL():
    url_prefix = 'http://'

print('Loading model...')
start = time.time()

m = Model.load('repository/model.pickle')

print('Model loaded! Took:', time.time() - start)
start = time.time()

arguments = m.arguments

print('Fetching data...')

data = m.fetch_data(arguments)

print('Data fetched! Took:', time.time() - start)
start = time.time()
print('Processing data...')

features = m.process_data(data, arguments)

model_id = requests.get(
    f'{url_prefix}{config.BASE_URL()}/api/machine_learning_model/{config.MODEL_IDENTIFIER()}/get_id/').json()
requests.patch(f'{url_prefix}{config.BASE_URL()}/api/machine_learning_model/{model_id}/',
               json={'expected_results': len(features)})

print('Data processed! Took:', time.time() - start)
start = time.time()
print('Predicting...')

res = m.predict(features, arguments)

print('Predicted! Took:', time.time() - start)
print('Sending results...')

batch_size = math.ceil(len(res) / (math.ceil(get_memory_usage(res) / memory_limit_in_mb) + 1))

res.reset_index(inplace=True)

for _, window in res.groupby(res.index // batch_size):
    result_data = json.loads(pd.DataFrame(window).to_json(orient='records'))

    prepared_results = []

    for row in result_data:
        prepared_results.append({
            'subject_id': row['subject_id'],
            'result': row,
        })

    requests.post(
        f'{url_prefix}{config.BASE_URL()}/api/machine_learning_model/{config.MODEL_IDENTIFIER()}/save_results/',
        json=prepared_results)

print(f'Results sent! Took: {time.time() - start}. Sent {len(res)} results ({get_memory_usage(res)} MB) in {math.ceil(len(res) / batch_size)} batches.')
