import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor, Lambda
from nn.dataset import MatchesDataset

matches_csv_file = 'data/matches.csv'
learning_rate = 1e-3
batch_size = 64
epochs = 10


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
    return DataLoader(td, batch_size=64)


def get_test_dataloader(td):
    return DataLoader(td, batch_size=64)


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
            nn.ReLU()
            # nn.Softmax(dim=1)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.linear_relu_stack(x)


def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    for batch, (X, y) in enumerate(dataloader):
        # compute prediction and loss
        prediction = model(X)
        loss = loss_fn(prediction, y)

        # backpropagation
        optimizer.zero_grad()
        loss.backward()  # Collects gradients.
        optimizer.step()  # Adjusts the parameters.

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}    [{current:>5d}/{size:>5d}]")


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            prediction = model(X)
            test_loss += loss_fn(prediction, y).item()
            correct += (prediction.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= size
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


def predict(test_data):
    classes = [
        "T-shirt/top",
        "Trouser",
        "Pullover",
        "Dress",
        "Coat",
        "Sandal",
        "Shirt",
        "Sneaker",
        "Bag",
        "Ankle boot",
    ]

    model = NeuralNetwork()
    model.load_state_dict(torch.load("model.pth"))

    model.eval()
    x, y = test_data[0][0], test_data[0][1]
    with torch.no_grad():
        pred = model(x)
        print(pred)
        predicted, actual = classes[pred[0].argmax(0)], classes[y]
        print(f'Predicted: "{predicted}", Actual: "{actual}"')


if __name__ == '__main__':
    tr_data = get_training_data()
    te_data = get_test_data()
    # train_dl = get_train_dataloader(tr_data)
    # test_dl = get_test_dataloader(te_data)
    # mod = NeuralNetwork()
    # lf = nn.CrossEntropyLoss()  # Initialize the loss function
    # opt = torch.optim.SGD(mod.parameters(), lr=learning_rate)  # stochastic gradient descent optimizer
    #
    # for e in range(epochs):
    #     print(f"Epoch {e + 1}\n-------------------------------")
    #     train_loop(train_dl, mod, lf, opt)
    #     test_loop(test_dl, mod, lf)
    # print('Done!')
    #
    # torch.save(mod.state_dict(), "model.pth")
    # print("Saved PyTorch Model State to model.pth")

    # predict(te_data)



