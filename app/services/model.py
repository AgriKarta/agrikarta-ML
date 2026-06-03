from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
import torch.nn as nn


class PriceTransformer(nn.Module):
    def __init__(self, d_model: int = 32, nhead: int = 4, num_layers: int = 2, dropout: float = 0.1):
        super().__init__()
        self.input_projection = nn.Linear(1, d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 2,
            dropout=dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output = nn.Linear(d_model, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.input_projection(x)
        x = self.encoder(x)
        return self.output(x[:, -1, :])


@dataclass
class TransformerForecaster:
    model: PriceTransformer
    lookback: int = 14

    @classmethod
    def default(cls) -> "TransformerForecaster":
        model = PriceTransformer()
        model.eval()
        return cls(model=model)

    def predict_next_7_days(self, prices: pd.Series) -> list[float]:
        values = prices.dropna().astype(float).to_numpy()
        if values.size == 0:
            return [0.0] * 7

        if values.size < self.lookback:
            baseline = float(values[-1])
            return [baseline] * 7

        history = values[-self.lookback :].astype(np.float32)
        predictions: list[float] = []
        rolling = history.copy()

        with torch.no_grad():
            for _ in range(7):
                features = torch.tensor(rolling, dtype=torch.float32).view(1, self.lookback, 1)
                next_price = float(self.model(features).item())
                if not np.isfinite(next_price):
                    next_price = float(rolling[-1])
                predictions.append(round(next_price, 2))
                rolling = np.roll(rolling, -1)
                rolling[-1] = next_price

        return predictions
