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
epochs = 500


def plot_error_chart(_errors):
    _errors = np.array(_errors)
    plt.figure(figsize=(12, 10))
    plt.plot(_errors, '-')
    plt.title('Błąd modelu podczas uczenia')
    plt.xlabel('liczba epok')
    plt.ylabel('błąd')
    plt.savefig('error.png')
    plt.show()


def plot_accuracy_chart(_accuracy):
    _accuracy = np.array(_accuracy)
    plt.figure(figsize=(12, 10))
    plt.plot(_accuracy, '-')
    plt.title('Dokładność modelu podczas uczenia')
    plt.xlabel('liczba epok')
    plt.ylabel('dokładność [%]')
    plt.savefig('accuracy.png')
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

    return test_loss, 100*correct


if __name__ == '__main__':
    train_dataset, test_dataset = create_matches_datasets(matches_csv_file)
    train_dl = get_dataloader(train_dataset)
    test_dl = get_dataloader(test_dataset)
    
    network = MatchPredictor()
    lf = nn.CrossEntropyLoss()
    opt = torch.optim.SGD(network.parameters(), lr=learning_rate)

    errors, accuracy = [], []

    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}\n----------------------------------")
        train_loop(train_dl, network, lf, opt)
        err, acc = test_loop(test_dl, network, lf)
        errors.append(err)
        accuracy.append(acc)

    plot_error_chart(errors)
    plot_accuracy_chart(accuracy)

    torch.save(network.state_dict(), "model.pth")
