
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode
from datetime import datetime, timezone
import nest_asyncio
import re
nest_asyncio.apply()
from loguru import logger
TOKEN = '7427431349:AAHIC6cgPcK9h4-ysvA-SrKGqZzwROKtF2Y'
CHANNEL_ID = '@newpairpump'

url_pattern = re.compile(
    r'^(https?:\/\/)?'  # Optional scheme (http or https)
    r'((([\w\d\-_]+\.)+[a-z]{2,})'  # Domain name
    r'|localhost'  # Localhost
    r'|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))'  # IP address
    r'(:\d+)?'  # Optional port
    r'(\/[\w\d\-._~:\/?#[\]@!$&\'()*+,;=]*)?$'  # Optional path
)

def is_url(string):
    return url_pattern.match(string) is not None

def convert_timestamp_to_human_readable(timestamp):
    timestamp_in_seconds = timestamp / 1000
    readable_date = datetime.fromtimestamp(timestamp_in_seconds, tz=timezone.utc)
    readable_date_str = readable_date.strftime('%Y-%m-%d %H:%M:%S')
    return readable_date_str

async def send_to_telegram(data):
    twitter_ = '✅' if data['twitter'] is not None else '❌'
    telegram_ = '✅' if data['twitter'] is not None else '❌'
    website_ =  '✅' if data['twitter'] is not None else '❌'
    message = f"""

*Mint*: `{escape_markdown(data['mint'], version=2)}`

*Market Cap:* {escape_markdown(data['usd_marketcap'], version=2)}
*Name*: {escape_markdown(data["name"], version=2)} \({escape_markdown(data['symbol'], version=2)}\)
*Description*: {escape_markdown(data["description"][:500], version=2)}

*Twitter* {escape_markdown(twitter_, version=2)} \| *Telegram* {escape_markdown(telegram_, version=2)} \| *Website* {escape_markdown(website_, version=2)}

*Open time*: {escape_markdown(convert_timestamp_to_human_readable(data['created_timestamp']), version=2)}

"""
    new_image = data['image_uri'].replace('https://cf-ipfs.com/', 'https://pump.mypinata.cloud/')

    bot_button = [
        InlineKeyboardButton("Bullx", url='https://bullx.io/terminal?chainId=1399811149&address=' + data['mint']),
        InlineKeyboardButton("Photon", url='https://photon-sol.tinyastro.io/en/lp/' + data['mint'])
    ]
    bot_button2 = [
        InlineKeyboardButton("Plonk", url='https://t.me/PlonkBot_bot?start=a_' + data['mint']),
        InlineKeyboardButton("Dogee", url='https://t.me/dogeebot_bot?start=rs-pumpearly-' + data['mint']),
        InlineKeyboardButton("Pepe", url='https://t.me/pepeboost_sol_bot?start=ref_02ppbg_ca_' + data['mint']),
    ]
    bot_button3 = [
        InlineKeyboardButton("Pumpfun", url='https://pump.fun/' + data['mint']),
    ]
    keyboard = []
    if data.get('twitter') and is_url(data.get('twitter')):
        keyboard.append(InlineKeyboardButton("Twitter", url=data['twitter']))

    if data.get('telegram') and is_url(data.get('telegram')):
        keyboard.append(InlineKeyboardButton("Telegram", url=data['telegram']))

    if data.get('website') and (is_url(data.get('website'))):
        keyboard.append(InlineKeyboardButton("Website", url=data['website']))

    reply_markup = InlineKeyboardMarkup([bot_button3, bot_button2, bot_button, keyboard])
    bot = Bot(token=TOKEN)
    logger.info(f"{data['name']} - {data['mint']}")
    return await bot.send_photo(chat_id=CHANNEL_ID, photo=new_image, caption=message, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=reply_markup)