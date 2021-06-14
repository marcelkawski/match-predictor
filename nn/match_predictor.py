from torch import nn


class MatchPredictor(nn.Module):
    def __init__(self):
        super(MatchPredictor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(57, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
            nn.Softmax(dim=0)
        )

    def forward(self, x):
        return self.network(x)
