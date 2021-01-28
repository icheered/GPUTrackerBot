import asyncio
import requests
from bs4 import BeautifulSoup
from loguru import logger
from parameters import Parameters
from datetime import datetime

async def get_price(GPU):
    URL = 'https://www.gputracker.eu/nl/search/category/1/grafische-kaarten?onlyInStock=true&fv_gpu.chip=NVIDIA%20RTX%20'+GPU
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
    while True:
        price = await get_price(GPU)
        if price is not None:
            logger.info("Lowest current price: "+ str(price))
            if price < TARGET:
                logger.info("Sending message")

                s = "3080 price dropped below "+str(TARGET)+"EUR. It is available for " + str(price) + "!"
                s.replace(" ", "%20")
                url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
                msg = url + s
                ret = requests.get(msg)
                link = url + 'https://www.gputracker.eu/nl/search/category/1/grafische-kaarten?onlyInStock=true&fv_gpu.chip=NVIDIA%20RTX%20' + GPU
                retlink = requests.get(link)
                logger.info("Waiting with sending a message for 10 minutes")
                await asyncio.sleep(TIMEOUT)
        await asyncio.sleep(POLL_INTERVAL)


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
        asyncio.get_event_loop().run_until_complete(main(
            API_KEY=API_KEY, 
            CHAT_ID=CHAT_ID,
            GPU=GPU,
            TARGET=TARGET,
            POLL_INTERVAL=POLL_INTERVAL,
            TIMEOUT=TIMEOUT))
    except KeyboardInterrupt:
        logger.error("The bot was stopped")
        url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
        s = "The bot was manually shut down at " + str(datetime.now())
        s.replace(" ", "%20")
        msg = url + s
        requests.get(msg)
    except Exception as e:
        logger.error("An error occured")
        logger.error(e)
        url = "https://api.telegram.org/bot"+ API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text="
        s = "An error occured and the bot has stopped at " + str(datetime.now())
        s.replace(" ", "%20")
        msg = url + s
        requests.get(msg)