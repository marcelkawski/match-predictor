import torch
from torch import nn
from torch.utils.data import DataLoader
from nn.dataset import MatchesDataset

matches_csv_file = 'data/matches.csv'
learning_rate = 1e-3
batch_size = 30
epochs = 20


class MatchPredictor(nn.Module):
    def __init__(self):
        super(MatchPredictor, self).__init__()
        self.stack = nn.Sequential(
            nn.Linear(57, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.stack(x)


def get_training_data():
    return MatchesDataset(
        train=True,
        matches_csv_file=matches_csv_file,
    )


def get_test_data():
    return MatchesDataset(
        train=False,
        matches_csv_file=matches_csv_file,
    )


def get_train_dataloader(td):
    return DataLoader(td, batch_size=batch_size, shuffle=True)


def get_test_dataloader(td):
    return DataLoader(td, batch_size=batch_size, shuffle=True)


def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    for batch, sample in enumerate(dataloader):
        X = sample['stats'].float()
        y = sample['result']
        prediction = model(X)
        loss = loss_fn(prediction, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        #
        if batch % 30 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}    [{current:>5d}/{size:>5d}]")


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for sample in dataloader:
            X = sample['stats'].float()
            y = sample['result']
            prediction = model(X)
            test_loss += loss_fn(prediction, y).item()
            correct += (prediction.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= size
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


if __name__ == '__main__':
    tr_data = get_training_data()
    te_data = get_test_data()
    train_dl = get_train_dataloader(tr_data)
    test_dl = get_test_dataloader(te_data)
    
    network = MatchPredictor()
    lf = nn.CrossEntropyLoss()
    opt = torch.optim.SGD(network.parameters(), lr=learning_rate)

    for e in range(epochs):
        print(f"Epoch {e + 1}\n-------------------------------")
        train_loop(train_dl, network, lf, opt)
        test_loop(test_dl, network, lf)

    torch.save(network.state_dict(), "model.pth")
