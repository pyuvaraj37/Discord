import discord
from discord.ext import commands
import passwords as keys
import sys
from twitter_connection import twitter_connection as t

class Twitter(commands.Cog):

    def __init__(self, client):
        self.client = client 


def setup(client):
    client.add_cog(Twitter(client))

token = keys.get_twitter_tokens()
twitter = t.twitter_connection(token[0], token[1], token[2], token[3])

json_response = twitter.standard_search(from_user='@realDonaldTrump', not_filters=['retweets'], since='2020-05-2')

statuses = json_response["statuses"]
#print(statuses)
text = []
for status in statuses:
    text.append(status["full_text"])
    
#print(text)