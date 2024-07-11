import undetected_chromedriver
from match import Match
from tournament import Tournament
from mongo import Mongo

#from getPlayerMatches import getPlayerMatches
from helper import Helper

def getTournament(tournamentHeader: str):
    return tournamentHeader.split(":")[1].split(",")[0]

def getSurface(tournamentHeader: str):
    return tournamentHeader.split(":")[1].split(",")[1].split("-")[0]

def getRound(tournamentHeader: str):
    return tournamentHeader.split(":")[1].split(",")[1].split("-")[1]

def getTournamentCategory(tournamentHeader: str):
    return tournamentHeader.split(":")[0]

from datetime import datetime
def getMatchDetails(driver: undetected_chromedriver.Chrome, match):
    matchId = match["id"]
    matchLink = match["link"]
    """
    # 1. open the match
    # 2. check opponent if he/she is already in database
    # 3. if not, add him/her to the database and get his/her matches
    # 4. get the match details
    # 4.1 get the tournament, surface, round, date, time, score, winner
    # 4.2 get the sets
    # 4.3 get the duration
    # 4.4 get the odds
    # 5. insert the match details to the database
    """
    #matchLink = "https://www.flashscore.com/match/8zTq2Jo9"
    driver.get(matchLink)
    Helper.hideCookieBanner(None, driver)

    # get the players
    time = None
    try:
        time = driver.find_element("class name", "duelParticipant__startTime").text
        date_format = "%d.%m.%Y %H:%M"
        date_object = datetime.strptime(time, date_format)
        timestamp = datetime.timestamp(date_object)
        time = timestamp
    except:
        print("Couldnt get the time for match: ", matchLink)
        pass

    player_home = driver.find_element("class name", "duelParticipant__home")
    player_home = player_home.find_element("tag name", "a").get_attribute("href")

    player_away = driver.find_element("class name", "duelParticipant__away")
    player_away = player_away.find_element("tag name", "a").get_attribute("href")

    #print(Helper.parsePlayerId(player_home), Helper.parsePlayerId(player_away), time)

    new_tournament = Tournament()
    round = ""

    home_score = None
    away_score = None
    # get the score
    try:
        score = driver.find_element("class name", "duelParticipant__score").text
        home_score = score.split("\n")[0]
        away_score = score.split("\n")[2]

    except:
        print("Couldnt get the score for match: ", matchLink)
        pass


    try:
        tournament_header = driver.find_element("class name", "tournamentHeader__country")
        tournament_link = tournament_header.find_element("tag name", "a").get_attribute("href")

        new_tournament.link = tournament_link
        new_tournament.name = getTournament(tournament_header.text)

        #print(tournament_link)
        new_tournament.category = getTournamentCategory(tournament_header.text)
        new_tournament.name = getTournament(tournament_header.text).replace(" ", "", 1)
        round = getRound(tournament_header.text).replace(" ", "", 1)
        new_tournament.surface = getSurface(tournament_header.text).replace(" ", "", 1)
    except:
        print("No tournament info for:", new_tournament.link)
        pass

    # check if the tournament is already in the database
    mongo = Mongo("hamalenko", "tournaments")
    tournament = mongo.find_one({"link": new_tournament.link})
    if not tournament:
        newlyInsertedTournament = mongo.insert_one(new_tournament.to_dict())
        print("New tournament added:", new_tournament.link, newlyInsertedTournament.inserted_id)
        match["tournamentId"] = newlyInsertedTournament.inserted_id
    else:
        match["tournamentId"] = tournament["_id"]

    # get the sets
    homeGames = {}
    awayGames = {}
    homeTieBreaks = {}
    awayTieBreaks = {}

    try:
        for i in range(1, 6):
            games = driver.find_elements("class name", f"smh__part--{i}")
            for j, game in enumerate(games):
                if game.text == "":
                    continue
                gResult = None
                tbResult = None

                sup = game.find_element("tag name", "sup")
                if sup.text != "":
                    gResult = int(game.text.split("\n")[0])
                    tbResult = int(game.text.split("\n")[1])
                else:
                    gResult = int(game.text)
                    tbResult = 0

                if j == 0:
                    homeGames[str(i)] = gResult
                    homeTieBreaks[str(i)] = tbResult

                if j == 1:
                    awayGames[str(i)] = gResult
                    awayTieBreaks[str(i)] = tbResult
    except:
        print("Couldnt get the sets for match: ", matchLink)
        pass

    # get durations
    durations = {}
    try:
        durations[str(0)] = driver.find_element("class name", "smh__time--overall").text

        for i in range(0, len(homeGames)):
            durations[str(i + 1)] = driver.find_element("class name", f"smh__time--{i}").text
    except:
        print("Couldnt get the durations for match: ", matchLink)
        pass

    # get odds
    homeOdd = None
    awayOdd = None

    try:
        homeOdd = driver.find_element("class name", "o_1").find_element("class name", "oddsValueInner").text
        if homeOdd == "-":
            homeOdd = "0.0"
        else:
            homeOdd = float(homeOdd)

        awayOdd = driver.find_element("class name", "o_2").find_element("class name", "oddsValueInner").text
        if awayOdd == "-":
            awayOdd = "0.0"
        else:
            awayOdd = float(awayOdd)

    except:
        print("Couldnt get the odds for match: ", matchLink)
        pass

    dbMatch = Match()
    dbMatch.id = matchId
    dbMatch.link = matchLink
    dbMatch._id = match["_id"]
    dbMatch.playerId = match["playerId"]
    dbMatch.tournamentId = match["tournamentId"]

    dbMatch.date = time
    # check if the player is home or away
    if Helper.parsePlayerId(player_home) == match["playerId"]:
        dbMatch.opponentId = Helper.parsePlayerId(player_away)
        dbMatch.playerScore = home_score
        dbMatch.opponentScore = away_score
        dbMatch.playerSets = homeGames
        dbMatch.opponentSets = awayGames
        dbMatch.playerTieBreaks = homeTieBreaks
        dbMatch.opponentTieBreaks = awayTieBreaks
        dbMatch.playerOdd = homeOdd
        dbMatch.opponentOdd = awayOdd
    else:
        dbMatch.opponentId = Helper.parsePlayerId(player_home)
        dbMatch.playerScore = away_score
        dbMatch.opponentScore = home_score
        dbMatch.playerSets = awayGames
        dbMatch.opponentSets = homeGames
        dbMatch.playerTieBreaks = awayTieBreaks
        dbMatch.opponentTieBreaks = homeTieBreaks
        dbMatch.playerOdd = awayOdd
        dbMatch.opponentOdd = homeOdd

    dbMatch.round = round
    dbMatch.durations = durations

    mongo = Mongo("hamalenko", "matches")

    # update the match in the database
    print("Updating match:", dbMatch._id, dbMatch.to_dict())
    mongo.replace_one({"id": dbMatch.id}, dbMatch.to_dict())







# get matches from db
from mongo import Mongo
mongo = Mongo("hamalenko", "matches")
matches = mongo.find({})
matches = list(matches)

# run chrome
driver = undetected_chromedriver.Chrome()

for i in range(0, len(matches)):
    getMatchDetails(driver, matches[i])

# wait for 60 seconds
import time
time.sleep(60)
driver.close()
