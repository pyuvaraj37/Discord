import discord 
from discord.ext import commands
import os
import sys
import passwords as keys

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

@client.event
async def on_ready():
    servers = client.guilds
    for server in servers:
        for channel in server.text_channels:
            if(channel.name == 'general'):
                await channel.send("I am online! Type !help for list of commands!")
    print('Bot is online!')

@client.event
async def on_member_join(member):
    servers = client.guilds
    for server in servers:
        for channel in server.text_channels:
            if(channel.name == 'general'):
                await channel.send(f'Welcome to {server.name}! You can see my commands by typing !help.')
    print(f'{member} has joined the server!')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(keys.get_test_token())
    