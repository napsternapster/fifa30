import json
from datetime import datetime

from requests_html import HTMLSession

TARGET_SCORES = [
        (0, 0),
        (0, 1), (1, 0),
        (1, 1), (1, 1),
        (1, 2), (2, 1)
        ]


class FifaLiveGame():

    def __init__(self, id=0, league=None, teams=None, score='0-0', time=0, data=None, cur_mirror='http://1xstavka.ru'):
        self._id = id
        self._data = data
        self._time = time
        self._teams = teams
        self._score = score
        self._league = league
        self._cur_mirror = cur_mirror

    @property
    def id(self):
        return self._id

    @property
    def teams(self):
        return self._teams

    @property
    def time(self):
        return self._time

    @property
    def score(self):
        return self._score

    @property
    def league(self):
        return self._league

    @property
    def target_coef(self):
        return self._target_coef

    @property
    def total(self):
        return self._total

    def is_second_half(self):
        return self._time >= 46

    def is_halftime(self):
        return any([self._data.get('SC').get('I') == 'Перерыв',
                    self._time_in_seconds in range(2701, 2850)])

    def fill_data_by_id(self):
        url = f"{self._cur_mirror}/LiveFeed/GetGameZip?id={self._id}"

        session = HTMLSession()
        try:
            json_data = session.get(url, timeout=10).text
        except Exception as e:
            print(e)
            print('Exception while getting data by id.')
            self._coef_data = []
            return

        data = json.loads(json_data)
        self._score = (data.get('Value').get('SC').get('FS').get('S1', 0), data.get('Value').get('SC').get('FS').get('S2', 0))
        self._time = int(int(data.get('Value').get('SC').get('TS', 0)) / 60)
        self._time_in_seconds = int(data.get('Value').get('SC').get('TS', 0))
        self._coef_data = data.get('Value').get('E')

    def fill_target_coef(self):
        if not self._coef_data:
            self._target_coef = -1
            return

        coefs = []
        for val in self._coef_data:
            if all([val.get('T') == 9,
                    val.get('G') == 17]):
                coefs.append(val)

        if len(coefs) < 2:
            self._target_coef = -1
            return

        self._target_coef = coefs[1].get('C')
        self._total = coefs[1].get('P')

    def is_target(self):
        return self.is_halftime() and self._score in TARGET_SCORES
