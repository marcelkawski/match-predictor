import pandas as pd


def encode_result(result):
    if result == 'H':
        return 0
    elif result == 'D':
        return 1
    elif result == 'A':
        return 2
    else:
        raise Exception('Illicit match result value. Permitted values: "H"|"D"|"A".')


if __name__ == '__main__':
    matches = pd.read_csv('../data/matches.csv')
    matches['FTR'] = matches['FTR'].apply(encode_result)
    matches.to_csv('../data/matches.csv', index=None)
