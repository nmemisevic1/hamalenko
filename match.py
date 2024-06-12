class Score:
    def __init__(self):
        self.home: int = 0
        self.away: int = 0

    # to dict
    def to_dict(self):
        return {
            'home': self.home,
            'away': self.away
        }

    # from dict
    @staticmethod
    def from_dict(data):
        score = Score()
        score.home = data['home']
        score.away = data['away']
        return score

class Match:
    def __init__(self):
        self.id: str = None
        self.link: str = None
        self.date: str = None
        self.time: str = None # local time
        self.playerId: str = None
        self.gender: bool = None # 0 - ATP, 1 - WTA
        self.homePlayerId: str = None
        self.awayPlayerId: str = None
        self.score: Score = Score()
        self.sets: list[Score] = []
        self.tournamentId: str = None
        self.round: int = None
        self.city: str = None
        self.country: str = None
        self.surface: str = None
        self.duration: int = None


        self.homePlayerOdd: float = None
        self.awayPlayerOdd: float = None

    # to dict
    def to_dict(self):
        return {
            'id': self.id,
            'link': self.link,
            'date': self.date,
            'time': self.time,
            'gender': self.gender,
            'homePlayerId': self.homePlayerId,
            'awayPlayerId': self.awayPlayerId,
            'score': self.score.to_dict(),
            'sets': [set.to_dict() for set in self.sets],
            'tournamentId': self.tournamentId,
            'round': self.round,
            'city': self.city,
            'country': self.country,
            'surface': self.surface,
            'duration': self.duration,
            'homePlayerOdd': self.homePlayerOdd,
            'awayPlayerOdd': self.awayPlayerOdd,
            'playerId': self.playerId
        }