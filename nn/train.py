import torch
from torch import nn
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import DataLoader

from nn.match_predictor import MatchPredictor
from nn.dataset import create_matches_datasets

matches_csv_file = 'data/matches.csv'
learning_rate = 1e-3
batch_size = 32
epochs = 700


def plot_charts(_errors):
    _errors = np.array(_errors)
    plt.figure(figsize=(12, 5))
    plt.plot(_errors, '-')
    plt.title('Model error during learning')
    plt.xlabel('Epochs')
    plt.ylabel('Error')
    plt.savefig('error.png')
    plt.show()


def get_dataloader(td):
    return DataLoader(td, batch_size=batch_size, shuffle=True)


def train_loop(dataloader, model, loss_fn, optimizer):
    for batch, sample in enumerate(dataloader):
        inpt = sample['stats'].float()
        outpt = sample['result']
        prediction = model(inpt)
        loss = loss_fn(prediction, outpt)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    test_loss, correct = 0, 0
    with torch.no_grad():
        for sample in dataloader:
            inpt = sample['stats'].float()
            outpt = sample['result']
            prediction = model(inpt)
            test_loss += loss_fn(prediction, outpt).item()
            correct += (prediction.argmax(1) == outpt).type(torch.float).sum().item()

    test_loss /= size
    correct /= size
    print(f"Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

    return test_loss


if __name__ == '__main__':
    train_dataset, test_dataset = create_matches_datasets(matches_csv_file)
    train_dl = get_dataloader(train_dataset)
    test_dl = get_dataloader(test_dataset)
    
    network = MatchPredictor()
    lf = nn.CrossEntropyLoss()
    opt = torch.optim.SGD(network.parameters(), lr=learning_rate)

    errors = []

    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}\n----------------------------------")
        train_loop(train_dl, network, lf, opt)
        err = test_loop(test_dl, network, lf)
        errors.append(err)

    plot_charts(errors)

    torch.save(network.state_dict(), "model.pth")
