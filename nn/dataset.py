from torch.utils.data.dataset import Dataset
import pandas as pd


class MatchesDataset(Dataset):
    def __init__(self, matches_csv_file, train):
        matches = pd.read_csv(matches_csv_file)
        print(matches[4499:4505]['MW'])
        if train is True:
            self.matches = matches.iloc[:4500]
        else:
            self.matches = matches.iloc[4500:]
        self.train = train

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, idx):
        data = self.matches.iloc[idx, :-3]
        result = self.matches.iloc[idx, -3:]
        return {"data": data, "result": result}
