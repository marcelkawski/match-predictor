import pandas as pd


if __name__ == '__main__':
    matches = pd.read_csv('../data/ns_matches.csv')
    matches['MW'] = matches['MW'].astype(int)
    matches = matches[(matches['MW'] > 1) & (matches['MW'] < 32)]

    columns = ['HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HTGD', 'ATGD', 'DiffPts']
    for col in columns:
        matches[col] = matches[col].astype(float)
        matches[col] = matches[col] / (matches['MW'] - 1)

    matches = matches.drop('MW', axis=1)

    matches.to_csv('data/matches.csv', index=None)
