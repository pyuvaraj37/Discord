import discord
from discord.ext import commands

class Developer(commands.Cog):

    def __init__(self, client):
        self.client = client 
    
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.{extension}')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        self.client.load_extension(f'cogs.{extension}')

    @commands.command()
    @commands.is_owner()
    async def kill(self, ctx):
        servers = self.client.guilds
        for server in servers:
            for channel in server.text_channels:
                if(channel.name == 'general'):
                    await channel.send("See ya!")
        await ctx.bot.logout()


def setup(client):
    client.add_cog(Developer(client))