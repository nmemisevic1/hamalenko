from mongo import Mongo

import undetected_chromedriver
import time
from helper import Helper
from match import Match


def getPlayerMatches(driver: undetected_chromedriver.Chrome, playerId: str, playerLink: str):
    playerLink = playerLink + "results/"
    driver.get(playerLink)
    time.sleep(1)
    Helper.hideCookieBanner(None, driver)

    # click on show more until there are no more matches to show
    numMatches = 0
    try:
        showMore = driver.find_element("class name", "event__more")
        if showMore:
            while numMatches != len(driver.find_elements("class name", "event__match")):
                numMatches = len(driver.find_elements("class name", "event__match"))
                showMore.click()
                time.sleep(1)
    except:
        pass

    matches = driver.find_elements("class name", "event__match")

    mongo = Mongo("hamalenko", "matches")

    for match in matches:
        m = Match()
        m.id = match.get_attribute("id")
        m.link = match.find_element("tag name", "a").get_attribute("href")
        m.playerId = playerId
        mongo.insert_one(m.to_dict())

    print(f"Player {playerLink} has {len(matches)} matches")


driver = undetected_chromedriver.Chrome()

mongo = Mongo("hamalenko", "players")
players = mongo.find({})
players = list(players)

for i in range(1428, len(players)):
    #print(f"Getting matches for player {players[i]['name']}")
    getPlayerMatches(driver, players[i]["id"], players[i]["link"])

driver.close()
