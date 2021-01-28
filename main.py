import discord
import random
import os

from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = '.', help_command = None)
status = cycle(['Beep Boop', 'Boop Beep', 'Boop Boop Beep', 'Boop Beep Boop'])

###Events

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.idle)
    print('Bot is ready.')

    #welcomeEmbed = discord.Embed(title = "Welcome!", description = "Welcome to the Coronavirus Data Bot!")

    #await ctx.send(embed = welcomeEmbed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command does not exist!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permissions for this command!')


###HELP COMMAND

@client.group(invoke_without_command = True, aliases=['h'])
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use .help <command> to obtain information on a command.", colour = ctx.author.colour)
    em.add_field(name = "Command List", value = "stats, compare, fact, factlist")
    await ctx.send(embed = em)

@help.command(aliases=['stat', 's'])
async def stats(ctx):
  em = discord.Embed(title = "Stats", description = "Displays Coronavirus statistics for a given country.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".stats <country>, .stat, .s")
  await ctx.send(embed = em)

@help.command(aliases=['f'])
async def fact(ctx):
  em = discord.Embed(title = "Fact", description = "Displays a random fact about the Coronavirus.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".fact, .f")
  await ctx.send(embed = em)

@help.command(aliases=['fl'])
async def fact_list(ctx):
  em = discord.Embed(title = "Fact List", description = "Displays a sorted list of all Coronavirus facts in the database.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".factlist, .fl")
  await ctx.send(embed = em)

@help.command(aliases=['comp', 'c'])
async def compare(ctx):
  em = discord.Embed(title = "Compare", description = "Compares the coronavirus statistics of two different countries.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".compare <country1> <country2>, .comp, .c")
  await ctx.send(embed = em)


###FACT LIST COMMAND

#Reading the facts file and creating a list
factsFile = open('facts.txt', 'r')
allFacts = factsFile.read().strip()
factsList = allFacts.split("\n")
sortedFacts = factsList.copy()

sortedFacts.sort()

@client.command(aliases=['fl'])
async def factlist(ctx):
    
    await ctx.send("The full list of Coronavirus facts in alphabetical order (loads in increments due to Discord limitations):")

    for sortedFact in sortedFacts:
      await ctx.send(f"```{sortedFact}```")
    
    await ctx.send("List is complete!")


###Commands

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

###Tasks

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))



###Cog Setup and Client Running

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('TOKEN'))
