import asyncio
import discord
from discord.ext.commands import Bot
from discord import Game
import random
import aiohttp
import json
from token import token

BOT_PREFIX = ("!","?")

TOKEN = token

client = Bot(command_prefix = BOT_PREFIX)


#8 ball function
@client.command(name='8ball',
                brief='answers from the beyond',
                description='answers a question',
                pass_context=True,
                aliases=['eightball','eight_ball', '8-ball'])
async def eight_ball(context):
    possible_responses = [
        "NOPE",
        "Not looking good",
        "Youre screwed :laughing:",
        "More likely than me breaking a demodisk",
        "Yes",
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

# todo add png of coins
@client.command(brief= 'i\'ll flip a disk',
                description='flips a coin')
async def coinflip():
    coin_sides = [
        "heads",
        "tails",
    ]
    await client.say(random.choice(coin_sides))

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print(" Logged in as " + client.user.name)
    print(" With ID: " + client.user.id)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current Servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

#SUMMON COMMAND
@client.command()
async def summon(channel: discord.Channel):
    voice = discord.VoiceClient
    if voice.is_connected() == True:
        await discord.VoiceClient.disconnect()
    else:
        await client.join_voice_channel(channel= channel)


#INFO COMMAND
@client.command(pass_context=True)
async def info(ctx, user: discord.Member): #user: is used to declare the user class
    embed = discord.Embed(title=f"{user.name}'s info:",description= "all i could find",color=0x0000ff)
    embed.add_field(name="Name:",value=(user.name), inline=True)
    embed.add_field(name="ID:",value=(user.id),inline=True)
    embed.add_field(name="Current Status:",value=(user.status),inline=True)
    embed.add_field(name="User Joined @: ",value=(user.joined_at),inline=True)
    embed.add_field(name="Bot", value=user.bot,inline=True)
    embed.add_field(name="Role",value=user.top_role,inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)


"""Todo allow phrases to start at 0 and end at 2 then reset and put ping on psuedo cooldown"""
@client.command()
async def ping():
    await client.say('Ping me again i dare you!')



client.loop.create_task(list_servers())

client.run(TOKEN)





