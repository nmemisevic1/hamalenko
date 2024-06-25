class Score:
    def __init__(self):
        self.player: int = 0
        self.opponent: int = 0

    # to dict
    def to_dict(self):
        return {
            'player': self.player,
            'opponent': self.opponent
        }

    # from dict
    @staticmethod
    def from_dict(data):
        score = Score()
        score.home = data['player']
        score.away = data['opponent']
        return score

class Match:
    def __init__(self):
        self.id: str = None
        self.link: str = None
        self.date: str = None
        self.time: str = None # local time
        self.localTime: str = None
        self.playerId: str = None
        self.opponentId: str = None
        self.gender: bool = None # 0 - Males, 1 - Females
        self.score: Score = Score()
        self.sets: list[Score] = []
        self.tournamentId: str = None
        self.round: int = None
        self.city: str = None
        self.country: str = None
        self.surface: str = None
        self.duration: int = None
        self.durations: list[int] = []
        self.playerOdd: float = None
        self.opponentOdd: float = None

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