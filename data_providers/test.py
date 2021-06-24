from data_providers.nn.get_clubs_statistics import check_streak, get_match_stats, normalize_match_stats


def test_check_streak():
    streak1 = check_streak(['W', 'W', 'W'], 'W', 3)
    streak2 = check_streak(['W', 'W', 'W', 'W', 'W'], 'W', 5)
    streak3 = check_streak(['L', 'L', 'L'], 'L', 3)
    streak4 = check_streak(['L', 'L', 'L', 'L', 'L'], 'L', 5)

    assert streak1 == 1
    assert streak2 == 1
    assert streak3 == 1
    assert streak4 == 1

    streak5 = check_streak(['W', 'L', 'W', 'W', 'W'], 'W', 3)
    streak6 = check_streak(['W', 'W', 'W', 'W', 'L'], 'W', 5)
    streak7 = check_streak(['L', 'L', 'D'], 'L', 3)
    streak8 = check_streak(['W', 'L', 'L', 'L', 'L'], 'L', 5)

    assert streak5 == 0
    assert streak6 == 0
    assert streak7 == 0
    assert streak8 == 0

    streak9 = check_streak([], 'W', 5)
    streak10 = check_streak(['L', 'L'], 'L', 3)

    assert streak9 == 0
    assert streak10 == 0


def test_get_match_stats():
    ht_stats = {'GS': 76,
                'GC': 29,
                'P': 71,
                'WinStreak3': 0,
                'WinStreak5': 0,
                'LossStreak3': 0,
                'LossStreak5': 0,
                'last_5_games_points': 12,
                'league_position': 3,
                'matches_played': 32}

    at_stats = {'GS': 60,
                'GC': 22,
                'P': 73,
                'WinStreak3': 0,
                'WinStreak5': 0,
                'LossStreak3': 0,
                'LossStreak5': 0,
                'last_5_games_points': 7,
                'league_position': 1,
                'matches_played': 33}

    match_stats, _, _ = get_match_stats(ht_stats, at_stats)

    assert match_stats['HTGS'] == 76
    assert match_stats['ATGS'] == 60
    assert match_stats['HTGC'] == 29
    assert match_stats['ATGC'] == 22
    assert match_stats['HTP'] == 71
    assert match_stats['ATP'] == 73

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


def test_normalize_match_stats():
    ht_stats = {'GS': 76,
                'GC': 29,
                'P': 71,
                'WinStreak3': 0,
                'WinStreak5': 0,
                'LossStreak3': 0,
                'LossStreak5': 0,
                'last_5_games_points': 12,
                'league_position': 3,
                'matches_played': 32}

    at_stats = {'GS': 60,
                'GC': 22,
                'P': 73,
                'WinStreak3': 0,
                'WinStreak5': 0,
                'LossStreak3': 0,
                'LossStreak5': 0,
                'last_5_games_points': 7,
                'league_position': 1,
                'matches_played': 33}

    match_stats, ht_mp, at_mp = get_match_stats(ht_stats, at_stats)
    match_stats = normalize_match_stats(match_stats, ht_mp, at_mp)

    assert match_stats['HTGS'] == 2.375
    assert match_stats['ATGS'] == 1.8181818181818181
    assert match_stats['HTGC'] == 0.90625
    assert match_stats['ATGC'] == 0.6666666666666666
    assert match_stats['HTP'] == 2.21875
    assert match_stats['ATP'] == 2.212121212121212

    assert match_stats['HTWinStreak3'] == 0
    assert match_stats['HTWinStreak5'] == 0
    assert match_stats['HTLossStreak3'] == 0
    assert match_stats['HTLossStreak5'] == 0

    assert match_stats['ATWinStreak3'] == 0
    assert match_stats['ATWinStreak5'] == 0
    assert match_stats['ATLossStreak3'] == 0
    assert match_stats['ATLossStreak5'] == 0

    assert match_stats['HTGD'] == 1.46875
    assert match_stats['ATGD'] == 1.1515151515151516
    assert match_stats['DiffPts'] == -0.0625
    assert match_stats['DiffFormPts'] == 5
    assert match_stats['DiffLP'] == 2
