from .predict import check_streak, get_match_stats


def test_check_streak():
    streak1 = check_streak(['win', 'win', 'win'], 'win', 3)
    streak2 = check_streak(['win', 'win', 'win', 'win', 'win'], 'win', 5)
    streak3 = check_streak(['loss', 'loss', 'loss'], 'loss', 3)
    streak4 = check_streak(['loss', 'loss', 'loss', 'loss', 'loss'], 'loss', 5)

    assert streak1 == 1
    assert streak2 == 1
    assert streak3 == 1
    assert streak4 == 1

    streak5 = check_streak(['win', 'loss', 'win', 'win', 'win'], 'win', 3)
    streak6 = check_streak(['win', 'win', 'win', 'win', 'loss'], 'win', 5)
    streak7 = check_streak(['loss', 'loss', 'draw'], 'loss', 3)
    streak8 = check_streak(['win', 'loss', 'loss', 'loss', 'loss'], 'loss', 5)

    assert streak5 == 0
    assert streak6 == 0
    assert streak7 == 0
    assert streak8 == 0

    streak9 = check_streak([], 'win', 5)
    streak10 = check_streak(['loss', 'loss'], 'loss', 3)

    assert streak9 == 0
    assert streak10 == 0


def test_get_match_stats():
    ht_stats = {'GS': 76,
                'GC': 29,
                'P': 71,
                'M1.1': 0, 'M1.2': 0, 'M1.3': 1,
                'M2.0': 0, 'M2.1': 0, 'M2.2': 0, 'M2.3': 1,
                'M3.0': 0, 'M3.1': 1, 'M3.2': 0, 'M3.3': 0,
                'M4.0': 0, 'M4.1': 0, 'M4.2': 0, 'M4.3': 1,
                'M5.0': 0, 'M5.1': 0, 'M5.2': 0, 'M5.3': 1,
                'WinStreak3': 0,
                'WinStreak5': 0,
                'LossStreak3': 0,
                'LossStreak5': 0,
                'last_5_games_points': 12,
                'league_position': 3}

    at_stats = {'GS': 60,
                'GC': 22,
                'P': 73,
                'M1.1': 0, 'M1.2': 1, 'M1.3': 0,
                'M2.0': 0, 'M2.1': 0, 'M2.2': 0, 'M2.3': 1,
                'M3.0': 0, 'M3.1': 0, 'M3.2': 0, 'M3.3': 1,
                'M4.0': 1, 'M4.1': 0, 'M4.2': 0, 'M4.3': 0,
                'M5.0': 0, 'M5.1': 1, 'M5.2': 0, 'M5.3': 0,
                'WinStreak3': 0,
                'WinStreak5': 0,
                'LossStreak3': 0,
                'LossStreak5': 0,
                'last_5_games_points': 7,
                'league_position': 1}

    match_stats = get_match_stats(ht_stats, at_stats)

    assert match_stats['HTGS'] == 76
    assert match_stats['ATGS'] == 60
    assert match_stats['HTGC'] == 29
    assert match_stats['ATGC'] == 22
    assert match_stats['HTP'] == 71
    assert match_stats['ATP'] == 73

    assert match_stats['HM1.1'] == 0
    assert match_stats['HM1.2'] == 0
    assert match_stats['HM1.3'] == 1

    assert match_stats['HM2.0'] == 0
    assert match_stats['HM2.1'] == 0
    assert match_stats['HM2.2'] == 0
    assert match_stats['HM2.3'] == 1

    assert match_stats['HM3.0'] == 0
    assert match_stats['HM3.1'] == 1
    assert match_stats['HM3.2'] == 0
    assert match_stats['HM3.3'] == 0

    assert match_stats['HM4.0'] == 0
    assert match_stats['HM4.1'] == 0
    assert match_stats['HM4.2'] == 0
    assert match_stats['HM4.3'] == 1

    assert match_stats['HM5.0'] == 0
    assert match_stats['HM5.1'] == 0
    assert match_stats['HM5.2'] == 0
    assert match_stats['HM5.3'] == 1

    assert match_stats['AM1.1'] == 0
    assert match_stats['AM1.2'] == 1
    assert match_stats['AM1.3'] == 0

    assert match_stats['AM2.0'] == 0
    assert match_stats['AM2.1'] == 0
    assert match_stats['AM2.2'] == 0
    assert match_stats['AM2.3'] == 1

    assert match_stats['AM3.0'] == 0
    assert match_stats['AM3.1'] == 0
    assert match_stats['AM3.2'] == 0
    assert match_stats['AM3.3'] == 1

    assert match_stats['AM4.0'] == 1
    assert match_stats['AM4.1'] == 0
    assert match_stats['AM4.2'] == 0
    assert match_stats['AM4.3'] == 0

    assert match_stats['AM5.0'] == 0
    assert match_stats['AM5.1'] == 1
    assert match_stats['AM5.2'] == 0
    assert match_stats['AM5.3'] == 0

    assert match_stats['HTWinStreak3'] == 0
    assert match_stats['HTWinStreak5'] == 0
    assert match_stats['HTLossStreak3'] == 0
    assert match_stats['HTLossStreak5'] == 0

    assert match_stats['ATWinStreak3'] == 0
    assert match_stats['ATWinStreak5'] == 0
    assert match_stats['ATLossStreak3'] == 0
    assert match_stats['ATLossStreak5'] == 0

    assert match_stats['HTGD'] == 47
    assert match_stats['ATGD'] == 38
    assert match_stats['DiffPts'] == -2
    assert match_stats['DiffFormPts'] == 5
    assert match_stats['DiffLP'] == 2



