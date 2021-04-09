class CountryNotFoundInApiError(Exception):
    def __init__(self, country_name):
        self.__country_name = country_name
        self.__message = f'Error: Country "{self.__country_name}" not found in the API.'
        super().__init__(self.__message)


class LeagueNotFoundInApiError(Exception):
    def __init__(self, country_name, league_name):
        self.__country_name = country_name
        self.__league_name = league_name
        self.__message = f'Error: League "{self.__league_name}" in the country "{self.__country_name}" not found in ' \
                         f'the API.'
        super().__init__(self.__message)


class CurrentSeasonNotFoundInApiError(Exception):
    def __init__(self, country_name, league_name):
        self.__country_name = country_name
        self.__league_name = league_name
        self.__message = f'Error: Current season of the "{self.__league_name}" league in the country ' \
                         f'"{self.__country_name}" not found in the API.'
        super().__init__(self.__message)


class CurrentSeasonNotFoundError(Exception):
    def __init__(self, league_name):
        self.__league_name = league_name
        self.__message = f'Error: Current season of the "{self.__league_name}" not found.'
        super().__init__(self.__message)


class MultipleCurrentSeasonsError(Exception):
    def __init__(self, league_name):
        self.__league_name = league_name
        self.__message = f'Error: Multiple current seasons for the "{self.__league_name}" were found.'
        super().__init__(self.__message)
