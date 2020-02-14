import json
import log
import discord
import datetime
from discord.ext import commands


def get_discord_token():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data["discord_token"]


def get_prefix():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data["command_prefix"]


bot = commands.Bot(command_prefix=get_prefix())


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("red!help"))
    log.info("Logged in as " + bot.user.name)
    # Displaying all the guilds the bot is connected to
    for guild in bot.guilds:
        log.info("Connected to: " + guild.name)


@bot.command(description="Returns pong and the time taken to anwser !")
async def ping(context):
    await context.send(":ping_pong: Pong !")


@bot.command(description="Hello there !")
async def hello(context):
    await context.send("Wazaa !")


@bot.command(description="Stops the bot")
@commands.is_owner()
async def stop(context):
    await context.send("Stopping bot !")
    log.info("Stopping bot !")
    bot.loop.stop()


@bot.command(description="Returns your avatar or the avatar of the given members")
async def avatar(context, members: commands.Greedy[discord.Member]):
    if len(members) == 0:
        await context.send(context.author.avatar_url)
    else:
        for member in members:
            await context.send(member.avatar_url)


@bot.command(description="Delete x messages that are before 14 days in the current channel")
async def clear(context, number: int):
    channel = context.message.channel
    messages = await channel.history(limit=number, after=datetime.datetime.now() - datetime.timedelta(days=13)).flatten()
    if len(messages) == 0:
        await context.send("No messages found before 14 days.")
    else:
        await channel.delete_messages(messages)
        await context.send(context.author.name + " deleted " + str(len(messages)) + " messages")


@bot.command(description="Test association command via private message")
async def asso(context):
    channel = context.get_channel(669640695912464434)
    await channel.send("Coucou")

log.info("Discord version: " + str(discord.version_info))
bot.run(get_discord_token())
