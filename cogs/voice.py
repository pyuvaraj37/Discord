import discord
from discord.ext import commands
import youtube_dl
import os

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'music/%(title)s.%(ext)s',

}

queue = {}
players = {}

def get_song_file(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download = False)
        song_title = meta['title']
        song_file = 'music/' + song_title + '.mp3'
    return song_title, song_file

def download(song_file, url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if os.path.isfile(song_file) is not True:
            ydl.download([url])
    
def check_queues(id):
    queue_list = queue.get(str(id))
    if queue_list != []: 
        song = queue_list.pop(0)
        download(song[1], song[2])
        players[str(id)].play(discord.FFmpegPCMAudio(song[1]), after=lambda x = id: check_queues(x))
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
    async def play(self, ctx, url=None):
        if(ctx.voice_client.is_connected()):
            print('Playing!')
            id = ctx.message.guild.id
            if url == None:
                if str(id) not in players:
                    players[str(id)] = ctx.voice_client
                check_queues(id)
            else: 
                song_file = get_song_file(url)
                download(url, song_file)
                ctx.voice_client.play(discord.FFmpegPCMAudio(song_file), after=lambda x = id: check_queues(x))
                players[str(id)] = ctx.voice_client
        else:
            print('Not connected to join!')

    @commands.command()
    async def add(self, ctx, url):
        id = ctx.message.guild.id
        song_title, song_file = get_song_file(url)
        if str(id) in queue:
            queue[str(id)].append((song_title, song_file, url))
            print(queue)
        else:
            queue[str(id)] = [(song_title, song_file, url)]
        print('Added song to queue!')

    @commands.command()
    async def viewq(self, ctx):
        id = ctx.message.guild.id
        if str(id) in queue:
            queue_list = queue[str(id)]
            title = 'Song Queue'
            description = ''
            for song in queue_list:
                description+=song[0] + '\n'
            queue_tile = discord.Embed(title=title, description=description)
            await ctx.send('', embed=queue_tile)
            
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
        print(queue[str(ctx.message.guild.id)])
        check_queues(ctx.message.guild.id)

def setup(client):
    client.add_cog(Voice(client))