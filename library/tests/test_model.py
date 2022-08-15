from nmml.model import Model, Arguments
import pandas as pd
import os.path


class TestModel:
    def fetch_data(self, arguments: Arguments):
        return pd.DataFrame({
            "ids": [4, 123, 9]
        })

    def process_data(self, data, arguments: Arguments):
        return data

    def predict(self, data: pd.DataFrame, arguments: Arguments):
        return data

    def test_model_can_be_serialised(self, tmp_path):
        # Serialise a model and test that the file gets created
        model_path = str(tmp_path.absolute()) + "/model.pickle"

        assert not os.path.isfile(model_path)

        model = Model(self.fetch_data, self.process_data, self.predict)
        model.save(model_path)

        assert os.path.isfile(model_path)

    def test_model_can_be_deserialised(self, tmp_path):
        # Serialise a model, load it again and test if the functions still output the same
        model_path = str(tmp_path.absolute()) + "/model.pickle"

        model = Model(self.fetch_data, self.process_data, self.predict)
        model.save(model_path)

        loaded_model = Model.load(model_path)

        results = loaded_model.fetch_data({})

        assert len(results) == 3
