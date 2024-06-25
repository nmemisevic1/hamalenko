import undetected_chromedriver
from match import Match

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

def getMatchDetails(driver: undetected_chromedriver.Chrome, matchId: str, matchLink: str):
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
    matchLink = "https://www.flashscore.com/match/8zTq2Jo9"
    driver.get(matchLink)
    Helper.hideCookieBanner(None, driver)
    # get the players
    time = driver.find_element("class name", "duelParticipant__startTime").text

    player_home = driver.find_element("class name", "duelParticipant__home")
    player_home = player_home.find_element("tag name", "a").get_attribute("href")

    player_away = driver.find_element("class name", "duelParticipant__away")
    player_away = player_away.find_element("tag name", "a").get_attribute("href")

    try:
        tournament_header = driver.find_element("class name", "tournamentHeader__country")
        tournament_link = tournament_header.find_element("tag name", "a").get_attribute("href")

        print(tournament_link)
        tournament_category = getTournamentCategory(tournament_header.text)
        tournament = getTournament(tournament_header.text).replace(" ", "", 1)
        surface = getSurface(tournament_header.text).replace(" ", "", 1)
        round = getRound(tournament_header.text).replace(" ", "", 1)

        print(Helper.parsePlayerId(player_home), Helper.parsePlayerId(player_away), time)
        print(tournament_category)
        print(tournament)
        print(surface)
        print(round)

        # get the score
        score = driver.find_element("class name", "duelParticipant__score").text
        print("Score:", score.split("\n")[0], score.split("\n")[2])
    except:
        pass

    # get the sets
    homeGames = {}
    awayGames = {}
    homeTieBreaks = {}
    awayTieBreaks = {}

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
                print(gResult, tbResult)
            else:
                gResult = int(game.text)
                tbResult = 0
                print(gResult, tbResult)

            if j == 0:
                homeGames[i] = gResult
                homeTieBreaks[i] = tbResult

            if j == 1:
                awayGames[i] = gResult
                awayTieBreaks[i] = tbResult

    print(homeGames)
    print(awayGames)
    print(homeTieBreaks)
    print(awayTieBreaks)

    # get durations
    durations = {}
    try:
        durations[0] = driver.find_element("class name", "smh__time--overall").text

        for i in range(0, 5):
            durations[i + 1] = driver.find_element("class name", f"smh__time--{i}").text
    except:
        pass
    print(durations)

    # get odds
    homeOdd = None
    awayOdd = None

    try:
        homeOdd = float(driver.find_element("class name", "o_1").find_element("class name", "oddsValueInner").text)
        awayOdd = float(driver.find_element("class name", "o_2").find_element("class name", "oddsValueInner").text)
    except:
        pass

    print("Odds:", homeOdd, awayOdd)

# get matches from db
from mongo import Mongo
mongo = Mongo("hamalenko", "matches")
matches = mongo.find({})
matches = list(matches)

# run chrome
driver = undetected_chromedriver.Chrome()

for i in range(0, 1):
    getMatchDetails(driver, matches[i]["id"], matches[i]["link"])

# wait for 60 seconds
import time
time.sleep(60)
driver.close()
