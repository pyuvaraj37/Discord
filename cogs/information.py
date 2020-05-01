import discord
from discord.ext import commands

command_info = [

    ('ping', 'Gets the ping of the user in ms\nPermission: All'),
    ('kill', 'Immediately disconnects the bot\nPermission: Admins'),
    ('join', 'Joins the current voice channel the user is connected to\nPermission: All'),
    ('leave', 'Leaves the current voice channel the user is connected to\nPermission: All')

]

def get_command_info(requested_command):
    title=''
    desc=''
    for a,b in command_info:
        if a == requested_command:
            title=a
            desc=b
    if (title != '' and desc != ''):
        return title, desc
    return 'No Command Found!', 'Use the options command to see a list of commands!'


class Information(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def info(self, ctx, requested_command):
        title, description = command_info.get_command_info(requested_command)
        info_tile = discord.Embed(title=title, description=description)
        await ctx.send('', embed=info_tile)


def setup(client):
    client.add_cog(Information(client))