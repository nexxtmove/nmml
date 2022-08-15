import re

import pandas as pd
import numpy as np

from runtime.control_api import ControlApi


class TestControlApi:
    def test_send_results_sends_small_results_in_one_batch(self, requests_mock):
        requests_mock.post(re.compile('/save_results/'), text="{}")

        control_api = ControlApi()

        df = pd.DataFrame(np.random.randint(0, 100, size=(100, 2)), columns=["subject_id", "result"])

        assert ControlApi.get_memory_usage(df) < control_api.memory_limit_in_mb

        control_api.send_results(df)

        assert requests_mock.call_count == 1

    def test_send_results_batches_results_when_too_big(self, requests_mock):
        requests_mock.post(re.compile('/save_results/'), text="{}")

        control_api = ControlApi()

        df = pd.DataFrame(np.random.randint(0, 100, size=(1_000_000, 2)), columns=["subject_id", "result"])

        assert (control_api.memory_limit_in_mb * 2) > ControlApi.get_memory_usage(df) > control_api.memory_limit_in_mb

        control_api.send_results(df)

        assert requests_mock.call_count == 3
