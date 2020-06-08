import discord
from discord.ext import commands
import youtube_dl
import os
import shutil

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'music/%(title)s.%(ext)s',
}

class music_player(commands.Cog):

    def __init__(self, id, ctx):
        self.id = id
        self.context = ctx
        self.cached_songs = {}
        self.queue = []

    def update_context(self, new_context):
        self.context = new_context

    def play(self, song_title, song_file):
        print(f'Playing {song_title}!')
        self.context.voice_client.play(discord.FFmpegPCMAudio(song_file), after=lambda e:self.check_queue(e))
    
    def check_queue(self, e=None):
        if len(self.queue) != 0:
            song = self.queue.pop(0)
            song_title = song[0]
            song_file = song[1]
            print(f'Playing {song_title}!')
            self.context.voice_client.play(discord.FFmpegPCMAudio(song_file), after=lambda e:self.check_queue(e))
    
    def add_to_queue(self, song_title, song_file):
        print(f'Added {song_title}!')
        self.queue.append((song_title, song_file))

    def download(self, song_title, song_file, url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if song_title not in self.cached_songs:
                self.cached_songs.update({song_title : song_file})
                ydl.download([url])

    def get_cached_song(self, index):
        index = int(index)
        if index <= len(self.cached_songs) and index > 0:
            song_titles = list(self.cached_songs)
            song_title = song_titles[index - 1]
            song_file = self.cached_songs.get(song_title)
            return song_title, song_file

    def get_cache(self):
        return self.cached_songs

    def get_queue(self):
        return self.queue

def setup(client):
    print('')