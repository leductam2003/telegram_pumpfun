from loguru import logger
import requests
import telegram_helper
import asyncio
import time

class PUMPFUN:
    def __init__(self) -> None:
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'origin': 'https://pump.fun'
        }
        self.processed_mints = set()
        self.validated_websites = {}

    def fetch_new_token(self):
        got_response = False
        while not got_response:
            try:
                response = requests.get('https://frontend-api.pump.fun/coins/latest', headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(response.reason)
            except Exception as err:
                logger.error(err)
            # sleep added for rate limiting
            time.sleep(1)

    def fetch_sol_price(self):
        got_response = False
        while not got_response:
            try:
                response = requests.get('https://frontend-api.pump.fun/sol-price', headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(response.reason)
            except Exception as err:
                logger.error(err)
            time.sleep(1)

    async def new_launch(self):
        try:
            data = self.fetch_new_token()
            if not data:
                return
            solPrice = self.fetch_sol_price()
            if not solPrice:
                return
            if data['mint'] not in self.processed_mints:
                self.processed_mints.add(data['mint'])
                usd_marketcap = solPrice['solPrice'] * data['market_cap']
                data['usd_marketcap'] = "${:,.0f}".format(usd_marketcap)
                await telegram_helper.send_to_telegram(data)
        except Exception as err:
            logger.error(err)

async def main():
    pumpfun = PUMPFUN()
    while True:
        await pumpfun.new_launch()

if __name__ == "__main__":
    asyncio.run(main())
