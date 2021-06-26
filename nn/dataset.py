import pandas as pd
import torch
from torch.utils.data.dataset import Dataset
from sklearn.model_selection import train_test_split


test_size = 0.3


class MatchesDataset(Dataset):
    def __init__(self, matches):
        self.matches = matches

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, idx):
        stats = torch.tensor(self.matches.iloc[idx, 1:])
        result = torch.tensor(self.matches.iloc[idx, 0])
        return {"stats": stats, "result": result}


def create_matches_datasets(matches_csv_file):
    matches = pd.read_csv(matches_csv_file)
    train_data, test_data = train_test_split(matches, test_size=test_size, shuffle=True)
    train_dataset = MatchesDataset(train_data)
    test_dataset = MatchesDataset(test_data)
    return train_dataset, test_dataset
