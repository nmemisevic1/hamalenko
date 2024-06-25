class Player:
    def __init__(self):
        self.id: str = None
        self.name: str = None
        self.link: str = None
        self.gender: bool = None  # 0 - Male, 1 - Female
        self.country: str = None
        self.rank: int = None
        self.points: int = None
        self.tournaments: int = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    # to dict
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'link': self.link,
            'gender': self.gender,
            'country': self.country,
            'rank': self.rank,
            'points': self.points,
            'tournaments': self.tournaments
        }

    # from dict
    @staticmethod
    def from_dict(data):
        player = Player()
        player.id = data['id']
        player.name = data['name']
        player.link = data['link']
        player.gender = data['gender']
        player.country = data['country']
        player.rank = data['rank']
        player.points = data['points']
        player.tournaments = data['tournaments']
        return player
