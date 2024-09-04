import torch
import torch.nn as nn

from utils import load_query


class CustomNet(nn.Module):
    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        hidden_layers: int,
        out_size: int,
        dropout=0.1,
    ):
        super(CustomNet, self).__init__()
        self.hidden_layers = hidden_layers
        self.hidden_size = hidden_size

        self.fc_in = nn.Linear(input_size, hidden_size)
        self.layers = nn.ModuleList(
            [
                nn.Sequential(
                    nn.Linear(hidden_size, hidden_size),
                    nn.BatchNorm1d(hidden_size),
                    nn.Dropout(dropout),
                )
                for _ in range(hidden_layers)
            ]
        )

        self.fc_out = nn.Linear(hidden_size, out_size)

        self.LeakyReLU = nn.LeakyReLU(0.2)

    def forward(self, x):
        x = self.LeakyReLU(self.fc_in(x))
        for i in range(self.hidden_layers):
            x = self.LeakyReLU(self.layers[i](x))
        x = self.fc_out(x)
        return x
