import pandas as pd
from sklearn.preprocessing import LabelBinarizer


def do_one_hot_enc():
    matches = pd.read_csv('data/matches.csv')
    columns = ['HM2', 'HM3', 'HM4', 'HM5', 'AM1', 'AM2', 'AM3', 'AM4', 'AM5']
    lb = LabelBinarizer()

    lb.fit(matches['HM1'])
    transformed = lb.transform(matches['HM1'])
    ohe_df = pd.DataFrame(transformed)
    matches = pd.concat([matches, ohe_df], axis=1).drop(['HM1'], axis=1)
    matches = matches.rename(columns={0: 'HM1.1', 1: 'HM1.2', 2: 'HM1.3'})

    for col in columns:
        lb.fit(matches[col])
        transformed = lb.transform(matches[col])
        ohe_df = pd.DataFrame(transformed)
        matches = pd.concat([matches, ohe_df], axis=1).drop([col], axis=1)
        matches = matches.rename(columns={0: col+'.0', 1: col+'.1', 2: col+'.2', 3: col+'.3'})

    lb.fit(matches['FTR'])
    transformed = lb.transform(matches['FTR'])
    ohe_df = pd.DataFrame(transformed)
    matches = pd.concat([matches, ohe_df], axis=1).drop(['FTR'], axis=1)
    matches = matches.rename(columns={0: 'FTR.1', 1: 'FTR.2', 2: 'FTR.3'})

    matches.to_csv('data/matches.csv', index=None)


if __name__ == '__main__':
    do_one_hot_enc()
