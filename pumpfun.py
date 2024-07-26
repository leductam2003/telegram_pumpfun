from loguru import logger
from utils import *
import aiohttp
import asyncio
import telegram_helper

class PUMPFUN:
    def __init__(self) -> None:
        self.headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'origin':'https://pump.fun'
        }
        self.processed_mints = set()
        self.validated_websites = {}

    async def fetch_new_token(self):
        got_response = False
        while not got_response:
            try:
                async with aiohttp.ClientSession() as session:
                    r = await session.get('https://frontend-api.pump.fun/coins/latest')
                    if r.status == 200:
                        return await r.json()
                    else:
                        logger.error(r.reason)
            except Exception as err:
                logger.error(err)
            #await asyncio.sleep(1)

    async def fetch_dev_created(self, dev):
        got_response = False
        while not got_response:
            try:
                async with aiohttp.ClientSession() as session:
                    r= await session.get(f'https://frontend-api.pump.fun/coins/user-created-coins/{dev}?offset=0&limit=10&includeNsfw=false')
                    if r.status == 200:
                        data = await r.json()
                        return data
                    else:
                        logger.error(r.reason)
            except Exception as err:
                logger.error(err)
            await asyncio.sleep(2)

    async def fetch_coin_info(self, token_address):
        got_response = False
        while not got_response:
            try:
                async with aiohttp.ClientSession() as session:
                    r= await session.get('https://frontend-api.pump.fun/coins/' + token_address)
                    if r.status == 200:
                        return await r.json()
                    else:
                        logger.error(r.reason)
            except Exception as err:
                logger.error(err)
            await asyncio.sleep(2)

    async def fetch_holder(self, token_address):
        got_response = False
        while not got_response:
            try:
                async with aiohttp.ClientSession() as session:
                    r = await session.post('https://pump-fe.helius-rpc.com/?api-key=1b8db865-a5a1-4535-9aec-01061440523b',json=
                                  {"method": "getTokenLargestAccounts", "jsonrpc": "2.0", "params": [token_address, { "commitment": "confirmed" }], "id": "633310da-8246-4a63-a250-311b2bc92d5b" }, headers=self.headers)
                    if r.status == 200:
                        data = await r.json()
                        if data:
                            return data['result']['value']
            except Exception as err:
                logger.error(err)
            await asyncio.sleep(2)

    async def fetch_account_info(self, token_address):
        max_retry = 5
        for _ in range(max_retry):
            try:
                async with aiohttp.ClientSession() as session:
                    r = await session.post('https://pump-fe.helius-rpc.com/?api-key=1b8db865-a5a1-4535-9aec-01061440523b',json=
                                 { "method": "getAccountInfo", "jsonrpc": "2.0", "params": [token_address, { "encoding": "jsonParsed", "commitment": "confirmed" }], "id": "633310da-8246-4a63-a250-311b2bc92d5b"  }, headers=self.headers)
                    if r.status == 200:
                        data = await r.json()
                        if data:
                            return data['result']['value']['data']['parsed']['info']['owner']
            except Exception as err:
                logger.error(err)
            await asyncio.sleep(2)

    async def check_website(self, website_url, token_address):
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                r = await session.get(url=website_url)
                if r.status == 200:
                    text = await r.text()
                    return token_address in text
                else:
                    logger.error(f"HTTP error: {r.status} - {r.reason}")
        except Exception as err:
            logger.error(f"Request failed: {err}")
        return False
    
    async def new_launch(self):
        data = await self.fetch_new_token()
        if not data:
            return
        if data['mint'] not in self.processed_mints:
            self.processed_mints.add(data['mint'])  
            await telegram_helper.send_to_telegram(data)

if __name__ == "__main__":
    async def main():
        pumpfun = PUMPFUN()
        while True:
            await pumpfun.new_launch()
    asyncio.run(main())