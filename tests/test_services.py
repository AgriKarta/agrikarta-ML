import unittest

import pandas as pd
import torch

from app.services.ingestion import clean_outliers
from app.services.model import TransformerForecaster


class TestIngestionService(unittest.TestCase):
    def test_clean_outliers_empty(self) -> None:
        df = pd.DataFrame(columns=["price"])
        result = clean_outliers(df)
        self.assertTrue(result.empty)

    def test_clean_outliers_zero_iqr(self) -> None:
        df = pd.DataFrame({"price": [100, 100, 100]})
        result = clean_outliers(df)
        self.assertEqual(len(result), 3)


class TestTransformerForecaster(unittest.TestCase):
    def test_predict_next_7_days_empty(self) -> None:
        forecaster = TransformerForecaster.default()
        predictions = forecaster.predict_next_7_days(pd.Series(dtype=float))
        self.assertEqual(predictions, [0.0] * 7)

    def test_predict_next_7_days_short_history(self) -> None:
        forecaster = TransformerForecaster.default()
        predictions = forecaster.predict_next_7_days(pd.Series([120.0, 121.0]))
        self.assertEqual(predictions, [121.0] * 7)

    def test_predict_next_7_days_non_finite_model_output(self) -> None:
        forecaster = TransformerForecaster.default()

        class _NaNModel:
            def __call__(self, _features):
                return torch.tensor([float("nan")], dtype=torch.float32)

        forecaster.model = _NaNModel()
        series = pd.Series([float(v) for v in range(100, 115)])
        predictions = forecaster.predict_next_7_days(series)
        self.assertEqual(predictions, [114.0] * 7)


if __name__ == "__main__":
    unittest.main()
