import random
from discord.ext import commands

#Reading the facts file and creating a list
facts_file = open('facts.txt', 'r')
all_facts = facts_file.read().strip()
facts_list = all_facts.split("\n")

class Facts(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['f'])
    async def fact(self, ctx):
      await ctx.send(f'```Fun Fact: {random.choice(facts_list)}```') #Generating a random fact from the list

def setup(client):
    client.add_cog(Facts(client))
