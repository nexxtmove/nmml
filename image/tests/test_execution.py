import os
import re
import json

import pandas as pd
from nmml.model import Model, Arguments

from runtime.execution import Execution


class TestExecution:
    def fetch_data(self, arguments: Arguments):
        return pd.DataFrame({
            "subject_id": [4, 123, 9],
            "result": [True, False, True]
        })

    def process_data(self, data, arguments: Arguments):
        return data

    def predict(self, data: pd.DataFrame, arguments: Arguments):
        return data

    def test_model_gets_executed_and_sends_results(self, tmp_path, requests_mock):
        os.chdir(tmp_path)
        os.mkdir("repository")

        requests_mock.get(re.compile('/get_id/'), text="13")
        requests_mock.get(re.compile('/heartbeat/'), text="{}")
        requests_mock.get(re.compile('/processed_results/'), text='{"available_results": []}')
        requests_mock.patch(re.compile('.*'), text="{}")
        requests_mock.post(re.compile('/save_results/'), text="{}")

        model_path = "repository/model.pickle"

        model = Model(self.fetch_data, self.process_data, self.predict)
        model.save(model_path)

        executor = Execution()
        executor.execute_model()

        results = json.loads(requests_mock.last_request.text)

        assert len(results) == 3
