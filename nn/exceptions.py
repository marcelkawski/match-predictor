class NoClubStatsError(Exception):
    def __init__(self, club_name):
        self.__message = f"No statistics available for club: {club_name}"
        super().__init__(self.__message)