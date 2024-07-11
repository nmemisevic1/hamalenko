import bson

class Match:
    def __init__(self):
        self._id: bson.ObjectId = None
        self.id: str = None
        self.link: str = None
        self.date: str = None
        self.time: str = None # local time
        self.localTime: str = None

        self.playerId: str = None
        self.opponentId: str = None

        self.playerScore: int = None
        self.opponentScore: int = None

        self.playerSets: dict[str] = {}
        self.opponentSets: dict[str] = {}

        self.playerTieBreaks: dict[str] = {}
        self.opponentTieBreaks: dict[str] = {}

        self.tournamentId: str = None
        self.round: int = None
        self.city: str = None
        self.country: str = None
        self.durations: dict[str] = {}

        self.playerOdd: float = None
        self.opponentOdd: float = None

    # to dict
    def to_dict(self):
        return {
            '_id': self._id,
            'id': self.id,
            'link': self.link,
            'date': self.date,
            'time': self.time,
            'localTime': self.localTime,
            'playerId': self.playerId,
            'opponentId': self.opponentId,
            'playerScore': self.playerScore,
            'opponentScore': self.opponentScore,
            'playerSets': self.playerSets,
            'opponentSets': self.opponentSets,
            'playerTieBreaks': self.playerTieBreaks,
            'opponentTieBreaks': self.opponentTieBreaks,
            'tournamentId': self.tournamentId,
            'round': self.round,
            'city': self.city,
            'country': self.country,
            'durations': self.durations,
            'playerOdd': self.playerOdd,
            'opponentOdd': self.opponentOdd
        }

    # from dict
    @staticmethod
    def from_dict(data):
        match = Match()
        match._id = data['_id']
        match.id = data['id']
        match.link = data['link']
        match.date = data['date']
        match.time = data['time']
        match.localTime = data['localTime']
        match.playerId = data['playerId']
        match.opponentId = data['opponentId']
        match.playerScore = data['playerScore']
        match.opponentScore = data['opponentScore']
        match.playerSets = data['playerSets']
        match.opponentSets = data['opponentSets']
        match.playerTieBreaks = data['playerTieBreaks']
        match.opponentTieBreaks = data['opponentTieBreaks']
        match.tournamentId = data['tournamentId']
        match.round = data['round']
        match.city = data['city']
        match.country = data['country']
        match.durations = data['durations']
        match.playerOdd = data['playerOdd']
        match.opponentOdd = data['opponentOdd']
        return match
