from torch import nn


class MatchPredictor(nn.Module):
    def __init__(self):
        super(MatchPredictor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(19, 11),
            nn.ReLU(),
            nn.Linear(11, 11),
            nn.ReLU(),
            nn.Linear(11, 3),
            nn.Softmax(dim=0)
        )

    def forward(self, x):
        return self.network(x)
