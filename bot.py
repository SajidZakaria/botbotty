import os
import time
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands


SUPER_USERS = ['Admin', 'admin']

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to server")
    for guild in bot.guilds:
        print(f"members are ", (', ').join([member.name for member in guild.members]))


@bot.command(name='listen')
@commands.has_any_role(*SUPER_USERS)
async def respond(ctx):
    embed = discord.Embed(description="**Listening voss**", color=0x00ff00)
    await ctx.send(embed=embed)

    def chk(reply):
        return reply.author == ctx.author and reply.channel == ctx.channel

    try:
        reply = await bot.wait_for("message", check=chk, timeout=60)
        messages = reply.content.split('\n')
        print(messages)
        # await ctx.send('got your message: ' + messages)

        for msg in messages:
            print(msg)
            await ctx.send(msg)

    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        response = "User must have role " + '/'.join([f"'{x}'" for x in SUPER_USERS])
        await ctx.send(response)


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        f.write(f'Error occurred {event}: {args[0]}')
        print(f'Error {event}: Check log for details')

bot.run(TOKEN)
