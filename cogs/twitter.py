import discord
from discord.ext import commands
import passwords as keys

class Twitter(commands.Cog):

    def __init__(self, client):
        self.client = client 


def setup(client):
    client.add_cog(Twitter(client))


twitter = twitter_connection(keys.get_twitter_tokens)

json_response = twitter.standard_search(search_terms=['View'],from_user='@realDonaldTrump', not_filters=['retweets'], since='2020-05-2')

statuses = json_response["statuses"]
#print(statuses)
text = []
for status in statuses:
    text.append(status["full_text"])
    
print(text)