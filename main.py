import asyncio
import requests
from bs4 import BeautifulSoup
from loguru import logger
from parameters import Parameters
from datetime import datetime
import os
import time

gpus = [
    {
        "gpu": "3080",
        "suffix": "&fv_gpu.chip=NVIDIA%20RTX%203080",
        "price": 0,
        "prevprice": 0,
        "target": 850
    },
    {
        "gpu": "6800xt",
        "suffix": "&fv_gpu.chip=AMD%20RX%206800%20XT",
        "price": 0,
        "prevprice": 0,
        "target": 850
    }
]

async def get_price(suffix):
    URL = 'https://www.gputracker.eu/nl/search/category/1/grafische-kaarten?onlyInStock=true'+suffix
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='facet-search-results')
    job_elems = results.find_all('div', class_='font-weight-bold text-secondary w-100 d-block h1 mb-2')
    prices = []
    for job_elem in job_elems:
        price = str(job_elem.find('span'))
        price = price[6:-7]
        prices.append(int(price))

    if prices:
        return min(prices)
    else:
        return None


async def main(API_KEY, CHAT_ID, GPU, TARGET, POLL_INTERVAL, TIMEOUT):
    polls = 0
    previous_price = 0
    while True:
        price = None
        try:
            for gpu in gpus:
                gpu["price"] = await get_price(gpu["suffix"])
        except requests.exceptions.ConnectionError:
            logger.info("Can't connect to internet, waiting for connect...")
            resp = os.system("ping -c 1 google.com")
            while resp != 0:
                logger.info("Waiting for connection...")
                time.sleep(10)
                resp = os.system("ping -c 1 google.com")
            logger.info("Online again")
            time.sleep(3)
        except Exception as e:
            logger.error("Can't get the price")
            logger.error(e)
        
        for gpu in gpus:
            if gpu["price"] is not None:
                price = gpu["price"]
                logger.info("Poll "+ str(polls) +"- Lowest current "+gpu["gpu"]+" price: "+ str(price))
                if price < gpu["target"]:
                    logger.info("Sending message")

                    s = gpu["gpu"] + "price dropped below "+str(gpu["target"])+"EUR. It is available for " + str(price) + "!"
                    s.replace(" ", "%20")
                    url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
                    msg = url + s
                    ret = requests.get(msg)
                    link = url + 'https://www.gputracker.eu/nl/search/category/1/grafische-kaarten?onlyInStock=true'+gpu["suffix"]
                    try:
                        retlink = requests.get(link)
                        logger.info("Waiting with sending a message for 10 minutes")
                        await asyncio.sleep(TIMEOUT)
                    except requests.exceptions.ConnectionError:
                        logger.info("Can't connect to internet, waiting for connect...")
                        resp = os.system("ping -c 1 google.com")
                        while resp != 0:
                            logger.info("Waiting for connection...")
                            time.sleep(10)
                            resp = os.system("ping -c 1 google.com")
                        logger.info("Online again")
                        time.sleep(3)
                
                elif gpu["prevprice"] is not None and gpu["price"] < gpu["prevprice"]:
                    logger.info("Sending message")

                    s = gpu["gpu"]+ " restocked. Lowest price: " + str(price) + "EUR !"
                    s.replace(" ", "%20")
                    url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
                    msg = url + s
                    ret = requests.get(msg)
                    link = url + 'https://www.gputracker.eu/nl/search/category/1/grafische-kaarten?onlyInStock=true'+gpu["suffix"]
                    try:
                        retlink = requests.get(link)
                        logger.info("Waiting with sending a message for 10 minutes")
                        await asyncio.sleep(TIMEOUT)
                    except requests.exceptions.ConnectionError:
                        logger.info("Can't connect to internet, waiting for connect...")
                        resp = os.system("ping -c 1 google.com")
                        while resp != 0:
                            logger.info("Waiting for connection...")
                            time.sleep(10)
                            resp = os.system("ping -c 1 google.com")
                        logger.info("Online again")
                        time.sleep(3)
            gpu["prevprice"] = gpu["price"]
        await asyncio.sleep(POLL_INTERVAL)
        
        polls += 1


if __name__ == "__main__":
    parameters = Parameters()
    config = parameters.get_dict()
    API_KEY = config["API_KEY"]
    CHAT_ID = config["CHAT_ID"]
    GPU = config["GPU"]
    TARGET = config["TARGET"]
    POLL_INTERVAL = config["POLL_INTERVAL"] * 60
    TIMEOUT = config["TARGET_HIT_TIMEOUT"] * 60
    try:
        logger.info("Starting the bot")
        resp = os.system("ping -c 1 google.com")
        while resp != 0:
            print("Waiting for connection...")
            time.sleep(10)
            resp = os.system("ping -c 1 google.com")
        url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
        s = "The bot was started at " + str(datetime.now())
        s.replace(" ", "%20")
        msg = url + s
        try:
            requests.get(msg)
        except Exception as e:
            logger.error("Can't start bot: "+str(e))

        asyncio.get_event_loop().run_until_complete(main(
            API_KEY=API_KEY, 
            CHAT_ID=CHAT_ID,
            GPU=GPU,
            TARGET=TARGET,
            POLL_INTERVAL=POLL_INTERVAL,
            TIMEOUT=TIMEOUT)
        )
    except KeyboardInterrupt:
        logger.error("The bot was stopped")
        url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
        s = "The bot was manually shut down at " + str(datetime.now())
        s.replace(" ", "%20")
        msg = url + s
        requests.get(msg)
    except Exception as e:
        logger.error("An error occured: "+str(e))
        resp = os.system("ping -c 1 google.com")
        while resp != 0:
            print("Waiting for connection...")
            time.sleep(10)
            resp = os.system("ping -c 1 google.com")
        url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
        s = "An error occured and the bot has stopped at " + str(datetime.now()+". Error: " +str(e))
        s.replace(" ", "%20")
        msg = url + s
        requests.get(msg)