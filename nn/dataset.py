import pandas as pd
import torch
from torch.utils.data.dataset import Dataset


class MatchesDataset(Dataset):
    def __init__(self, matches_csv_file, train):
        matches = pd.read_csv(matches_csv_file)
        if train is True:
            self.matches = matches.iloc[:4500]
        else:
            self.matches = matches.iloc[4500:]
        self.train = train

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, idx):
        stats = torch.tensor(self.matches.iloc[idx, 1:])
        result = torch.tensor(self.matches.iloc[idx, 0])
        return {"stats": stats, "result": result}
