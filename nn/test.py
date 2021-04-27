from .predict import check_streak


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

