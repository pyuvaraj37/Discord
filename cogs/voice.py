import discord
from discord.ext import commands
import youtube_dl
import os
import shutil
from django.core.validators import URLValidator
from cogs.music_player import music_player
import sys
sys.path.insert(0,'..')
import search_yt as syt

validate = URLValidator()

def get_song_file(url):
    with youtube_dl.YoutubeDL() as ydl:
        meta = ydl.extract_info(url, download = False)
        song_title = meta['title']
        song_file = 'music/' + song_title + '.mp3'
    return song_title, song_file

class Voice(commands.Cog):
    
    def __init__(self, client):
        self.client = client 
        self.music_player = {}

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        id = str(ctx.message.guild.id) 
        await channel.connect()
        self.music_player.update({id: music_player(id, ctx)})

    @commands.command()
    async def leave(self, ctx):
        shutil.rmtree('music')
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, input=None):
        id = str(ctx.message.guild.id)
        self.music_player[id].update_context(ctx)
        isURL = True

        #checks url
        try:
            validate(input)
        except:
            isURL = False
            #print('Cache Index!')

        if input != None:
            if isURL:
                song_title, song_file = get_song_file(input)
                self.music_player[id].download(song_title, song_file, input)
            else:
                song_title, song_file = self.music_player[id].get_cached_song(input)
            
            self.music_player[id].play(song_title, song_file)
        else:
            self.music_player[id].check_queue()
    
    @commands.command()
    async def add(self, ctx, input):
        id = str(ctx.message.guild.id)
        self.music_player[id].update_context(ctx)
        isURL = True
        
        try:
            validate(input)
        except:
            isURL = False

        if isURL:
            song_title, song_file = get_song_file(input)
            self.music_player[id].download(song_title, song_file, input)
            self.music_player[id].add_to_queue(song_title, song_file)
        else:
            if input.isdigit():
                song_title, song_file = self.music_player[id].get_cached_song(input)
                self.music_player[id].add_to_queue(song_title, song_file)
            else:
                url = syt.search(input)
                song_title, song_file = get_song_file(url)
                self.music_player[id].download(song_title, song_file, url)
                self.music_player[id].add_to_queue(song_title, song_file)
                await ctx.send(f'Found "{song_title}" from YT and added it to queue!')
                

    @commands.command()
    async def viewq(self, ctx):
        id = str(ctx.message.guild.id)
        self.music_player[id].update_context(ctx)
        queue_list = self.music_player[id].get_queue()
        title = 'Song Queue'
        description = ''
        for song in queue_list:
            description+=song[0] + '\n'
        queue_tile = discord.Embed(title=title, description=description)
        await ctx.send('', embed=queue_tile)
        

    @commands.command()
    async def viewc(self, ctx):
        id = str(ctx.message.guild.id)
        self.music_player[id].update_context(ctx)
        cached_songs = self.music_player[id].get_cache()
        title = 'Cached Songs'
        description = ''
        i = 1 
        for song_file in cached_songs:
            description+= str(i)+ '. ' + song_file+'\n'
            i+=1
        cache_tile = discord.Embed(title=title, description=description)
        await ctx.send('', embed=cache_tile)
        

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()

def setup(client):
    client.add_cog(Voice(client))