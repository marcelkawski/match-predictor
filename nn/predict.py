import torch
from nn.train import MatchPredictor


def predict_match(stats):
    with torch.no_grad():
        pred = model(stats)
        print(pred)
        prediction = pred[0].argmax(0)
    return prediction


if __name__ == '__main__':
    model = MatchPredictor()
    model.load_state_dict(torch.load("model.pth"))
    model.eval()
    # stats = get_match_stats()
    # match_result = predict_match(stats)
