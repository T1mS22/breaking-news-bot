import os
import requests
import time
import discord
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.parser import parse

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_news():
    url = "https://www.tagesschau.de/api2/homepage/"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None
    
async def print_breaking_news_message(channel, news_data):
    if "news" in news_data:
        for news_item in news_data["news"]:
            breaking_news = news_item.get("breakingNews", False)
            date_str = news_item.get("date", None)
            if breaking_news and date_str:
                date_obj = parse(date_str)
                now = datetime.now(date_obj.tzinfo)
                if now - date_obj <= timedelta(minutes=5):
                    title = news_item.get("title", "No title available.")
                    firstsentence = news_item.get("firstSentence", "No data available.")
                    image = news_item.get("teaserImage", {}).get("imageVariants", {}).get("16x9-1920", news_item.get("teaserImage", {}).get("alttext", "No image and alttext available."))
                    link = news_item.get("detailsweb", "No link available.")

                    message = f":zap: **EILMELDUNG** :zap:\n**{title}**\n{firstsentence}\n{image}\n{link}"
                    await channel.send(message)
    else:
        await channel.send("No message found in the response.")

async def send_news_to_discord(client):
    while True:
        news_data = get_news()
        if news_data:
            news_channel = discord.utils.get(client.get_all_channels(), name='news')
            if news_channel:
                await print_breaking_news_message(news_channel, news_data)
            else:
                print("News channel not found.")
        await asyncio.sleep(300)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(send_news_to_discord(client))

client.run(TOKEN)