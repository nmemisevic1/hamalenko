class Tournament:
    def __init__(self):
        self.name: str = None
        self.link: str = None
        self.category: str = None
        self.surface: str = None
        self.city: str = None
        self.country: str = None

    def __str__(self):
        return self.name

    # to dict
    def to_dict(self):
        return {
            'name': self.name,
            'link': self.link,
            'category': self.category,
            'surface': self.surface,
            'city': self.city,
            'country': self.country
        }

    # from dict
    @staticmethod
    def from_dict(data):
        tournament = Tournament()
        tournament.name = data['name']
        tournament.link = data['link']
        tournament.category = data['category']
        tournament.surface = data['surface']
        tournament.city = data['city']
        tournament.country = data['country']
        return tournament