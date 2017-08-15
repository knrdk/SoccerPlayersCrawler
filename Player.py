class Player:
    def __init__(self, team, fullName, age, nationality, position):
        self.playingCountry = team.country
        self.leagueName = team.leagueName
        self.teamName = team.name
        self.full_name = fullName
        self.age = age
        self.nationality = nationality
        self.position = position
