import time
import undetected_chromedriver

class Helper:
    def __init__(self):
        pass

    # hide the cookie banner
    @staticmethod
    def hideCookieBanner(self, driver: undetected_chromedriver.Chrome):
        try:
            cookiesBanner = driver.find_element("id", "onetrust-reject-all-handler")
            if cookiesBanner:
                cookiesBanner.click()
                time.sleep(2)
        except:
            pass

    # Print iterations progress
    @staticmethod
    def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    # parse link to get player id
    @staticmethod
    def parsePlayerId(link: str):
        return link.split("/")[-2]