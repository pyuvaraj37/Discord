import discord
from discord.ext import commands

command_info = [

    ('ping', 'Gets the ping of the user in ms\nPermission: All'),
    ('kill', 'Immediately disconnects the bot\nPermission: Admins'),
    ('load', 'Loads the specifigy cog\nPermission: Admins'),
    ('reload', 'Reloads the specifigy cog\nPermission: Admins'),
    ('unload', 'Unloads the specifigy cog\nPermission: Admins'),
    ('join', 'Joins the current voice channel the user is connected to\nPermission: All'),
    ('leave', 'Leaves the current voice channel the user is connected to and wipes the song cache\nPermission: All'),
    ('play', 'Plays the youtube link or cached song number provided by the user after the command or plays the next song in queue\nEX:!play https://www.youtube.com/watch?v=-lbbHQbZNKg\n!play 1\nPermission: All'),
    ('add', 'Add the provided youtube link or cached song number to the queue\nPermission: All'),
    ('viewq', 'Provides a list of queued songs\nPermission: All'),
    ('viewc', 'Provides a list of cached songs, in a numbered order. You can add or play these by using the command with the songs number\nPermission: All'),
    ('stop', 'Stops the player (not pause). Can only be started again by play command\nPermission: All'),
    ('pause', 'Pauses the song player (not stop). Can be started again with resume, or play\nPermission: All'),
    ('resume', 'Resumes the paused song\nPermission: All'),
    ('help', 'Retrieves a list of commands, or if provided a command gives more information about the command\nEX:!help play\nPermission: All')

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
    return 'No Command Found!', 'Use !help to see a list of commands!'

def format_command_list():
    command_list=''
    for a, b in command_info:
        command_list += a + '\n'
    command_list+= 'Type !help followed by a specific command to learn more.' 
    return command_list

class Information(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def help(self, ctx, requested_command=None):

        if requested_command != None:
            title, description = get_command_info(requested_command)
            info_tile = discord.Embed(title=title, description=description)
            await ctx.send('', embed=info_tile)
        else:
            title = 'List of commands!'
            description = format_command_list()
            info_tile = discord.Embed(title=title, description=description)
            await ctx.send('', embed=info_tile)


def setup(client):
    client.add_cog(Information(client))