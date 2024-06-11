class Score:
    def __init__(self):
        self.home: int = 0
        self.away: int = 0

class Match:
    def __init__(self):
        self.id: str = None
        self.date: str = None
        self.time: str = None # local time
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