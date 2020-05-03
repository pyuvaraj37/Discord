import discord
from discord.ext import commands
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'music/test.'
}

queue = {}
players = {}

def check_queues(id):
    if queue[id] != []: 
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(queue[id].pop(0))
        players[id].play(discord.FFmpegPCMAudio('./music/test.mp3'), after=lambda x = id: check_queues(x))
    else:
        print('No more songs!')

class Voice(commands.Cog):
    
    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        id = ctx.message.guild.id
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        ctx.voice_client.play(discord.FFmpegPCMAudio('./music/test.mp3'), after=lambda x = id: check_queues(x))
        players[id] = ctx.voice_client

    @commands.command()
    async def add(self, ctx, url):
        id = ctx.message.guild.id
        if id in queue:
            queue[id].append(url)
        else:
            queue[id] = [url]
        print('Added song to queue!')

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        check_queues(ctx.guild.id)

def setup(client):
    client.add_cog(Voice(client))