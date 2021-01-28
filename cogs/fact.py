import discord
import random
from discord.ext import commands

factsFile = open('facts.txt', 'r')
allFacts = factsFile.read().strip()
factsList = allFacts.split("\n")

class Facts(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['f'])
    async def fact(self, ctx):
      await ctx.send(f'Fun Fact: {random.choice(factsList)}')

def setup(client):
    client.add_cog(Facts(client))
