from nmml.model import Model
from nmml import config
import time
import requests
import json

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
    f'http://{config.BASE_URL()}/api/machine_learning_model/{config.MODEL_IDENTIFIER()}/get_id/').json()
requests.patch(f'http://{config.BASE_URL()}/api/machine_learning_model/{model_id}/',
               json={'expected_results': len(features)})

print('Data processed! Took:', time.time() - start)
start = time.time()
print('Predicting...')

res = m.predict(features, arguments)

print('Predicted! Took:', time.time() - start)
print('Preparing sending results...')

result_data = json.loads(res.to_json(orient='records'))

prepared_results = []

for row in result_data:
    prepared_results.append({
        'subject_id': row['subject_id'],
        'result': row,
    })

print('Results prepared! Took:', time.time() - start)
start = time.time()
print('Sending results...')

requests.post(f'http://{config.BASE_URL()}/api/machine_learning_model/{config.MODEL_IDENTIFIER()}/save_results/',
              json=prepared_results)

print('Results sent! Took:', time.time() - start)
