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


def encode_win(result):
    if result == 'W':
        return 0
    elif result == 'D':
        return 1
    elif result == 'L':
        return 2
    elif result == 'M':
        return 3
    else:
        raise Exception('Illicit match result value. Permitted values: "W"|"D"|"L"|"M".')


if __name__ == '__main__':
    matches = pd.read_csv('data/ns_matches.csv')
    matches['MW'] = matches['MW'].astype(int)
    matches = matches[matches['MW'] > 1]

    columns = ['HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HTGD', 'ATGD', 'DiffPts']
    for col in columns:
        matches[col] = matches[col].astype(float)
        matches[col] = matches[col] / (matches['MW'] - 1)

    matches['FTR'] = matches['FTR'].apply(encode_result)

    columns = ['HM1', 'HM2', 'HM3', 'HM4', 'HM5', 'AM1', 'AM2', 'AM3', 'AM4', 'AM5']
    for col in columns:
        matches[col] = matches[col].apply(encode_win)

    matches.to_csv('data/matches.csv', index=None)





