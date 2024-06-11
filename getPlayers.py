import undetected_chromedriver
import time
from helper import Helper

from mongo import Mongo
from player import Player

def getPlayers(link):
    driver = undetected_chromedriver.Chrome()
    driver.get(link)
    time.sleep(2)
    Helper.hideCookieBanner(None, driver)
    driver.find_element("class name", "rankingTable__row--more").click()
    time.sleep(3)
    players = driver.find_elements("class name", "rankingTable__row")

    mongo = Mongo("hamalenko", "players")

    for i in range(1, len(players)):
        player = players[i]
        playerObj = Player()
        playerObj.name = player.find_element("tag name", "a").text
        playerObj.link = player.find_element("tag name", "a").get_attribute("href")
        playerObj.rank = int(player.find_element("class name", "rankingTable__cell--rank").text.split(".")[0])
        playerObj.points = int(player.find_element("class name", "rankingTable__cell--points").text)
        playerObj.country = player.find_element("class name", "rankingTable__nationality").text
        playerObj.tournaments = int(player.find_element("class name", "rankingTable__cell--tournament").text)
        playerObj.gender = 1
        # split link by "/" and get last element
        playerObj.id = playerObj.link.split("/")[-2]
        mongo.insert_one(playerObj.to_dict())
        print(playerObj.name, playerObj.rank)

    driver.close()

wtaPlayersLink = ("https://www.flashscore.com/tennis/rankings/wta/")
atpPlayersLink = ("https://www.flashscore.com/tennis/rankings/atp/")

# Get WTA players
getPlayers(wtaPlayersLink)

# Get ATP players
getPlayers(atpPlayersLink)


