import discord
import os

from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = '.', help_command = None) #Disabling the default help command, bot prefix is .
status = cycle(['Beep Boop', 'Boop Beep', 'Boop Boop Beep', 'Boop Beep Boop'])

###Events

@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready.') #For testing purposes, does not affect the program


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
    em.add_field(name = "Command List", value = "african, asian, compare, fact, factlist, info, stats, western")
    await ctx.send(embed = em)

@help.command(aliases=['i'])
async def info_overview(ctx):
  em = discord.Embed(title = "Info", description = "Explains the full intents behind the creation of this bot.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".info, .i")
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

@help.command(aliases=['asia', 'a'])
async def asian_countries(ctx):
  em = discord.Embed(title = "Asian", description = "Generates a list of every Asian country supported by the bot.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".asian, .asia, .a")
  await ctx.send(embed = em)

@help.command(aliases=['west', 'w'])
async def western_countries(ctx):
  em = discord.Embed(title = "Western", description = "Generates a list of every Western country supported by the bot.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".western, .west, .w")
  await ctx.send(embed = em)

@help.command(aliases=['africa', 'af'])
async def african_countries(ctx):
  em = discord.Embed(title = "African", description = "Generates a list of every African country supported by the bot.", colour = ctx.author.colour)
  em.add_field(name = "**Syntax**", value = ".african, .africa, .af")
  await ctx.send(embed = em)


###FACT LIST COMMAND

#Reading the facts file and creating a list
facts_file = open('facts.txt', 'r')
all_facts = facts_file.read().strip()
facts_list = all_facts.split("\n")
sorted_facts = facts_list.copy()

#Sorts facts list into alphabetical order
sorted_facts.sort()

@client.command(aliases=['fl'])
async def factlist(ctx):
    await ctx.send("**The full list of Coronavirus facts in alphabetical order (loads in increments due to Discord limitations):**")

    for sorted_fact in sorted_facts:
      await ctx.send(f"```{sorted_fact}```")
    
    await ctx.send("**List is complete!**")


###ASIAN COUNTRIES LIST COMMAND

#Reading the asian countries file and creating a list
asian_file = open('asian.txt', 'r')
all_asian = asian_file.read().strip()
asian_list = all_asian.split("\n")
sorted_asian = asian_list.copy()

#Sorts asian countries list into alphabetical order
sorted_asian.sort()

@client.command(aliases=['asia', 'a'])
async def asian(ctx):
    await ctx.send("**The full list of Asian countries supported by the bot:**")
    await ctx.send(f"```{sorted_asian}```")


###WESTERN COUNTRIES LIST COMMAND

#Reading the western countries file and creating a list
western_file = open('western.txt', 'r')
all_western = western_file.read().strip()
western_list = all_western.split("\n")

@client.command(aliases=['west', 'w'])
async def western(ctx):
    await ctx.send("**The full list of Western countries supported by the bot:**")
    await ctx.send(f"```{western_list}```")
    

###AFRICAN COUNTRIES LIST COMMAND

#Reading the african countries file and creating a list
african_file = open('african.txt', 'r')
all_african = african_file.read().strip()
african_list = all_african.split("\n")

@client.command(aliases=['africa', 'af'])
async def african(ctx):
    await ctx.send("**The full list of African countries supported by the bot:**")
    await ctx.send(f"```{african_list}```")



###INFO COMMAND

@client.command(aliases=['i'])
async def info(ctx):
    info_embed = discord.Embed(title="Bot Info and Overview", color=0x7248d0, description="This bot was constructed in order to objectively showcase statistics related to the Coronavirus pandemic for various countries. \n \n A common issue that we (the development team) have noticed over time is the stigmatization of East Asian countries by Western media outlets. Especially when the pandemic first broke out, Western citizens with ethnicities coming from countries such as China, Japan and Korea were looked down upon by their peers. \n \n **However,** although this stigma is seemingly not as prevalent as it once was, **it is still very much alive.** Through this bot, we hope to make it clear that more often than not, East Asian countries have done an outstanding job when it comes to responsibly handling the Coronavirus when compared to their Western counterparts.")
    await ctx.send(embed=info_embed)



###Tasks

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


###Cog Setup and Client Running

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('TOKEN'))
