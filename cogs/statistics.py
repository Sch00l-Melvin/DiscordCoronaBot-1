import discord
from discord.ext import commands
import requests
from datetime import datetime

#Reading the east asian countries file and creating a list
eastern_file = open('eastern.txt', 'r')
all_eastern = eastern_file.read().strip()
eastern_list = all_eastern.split("\n")


class Statistics(commands.Cog):

    def __init__(self, client):
        self.client = client

    def get_stat(self, country):
        # KNOWN ISSUE
        # Canada is not part of the api for some reason
        country = country.replace(" ", "-").lower()
        # Can use any start date in the past as enough time has passed for data to be generated
        reference = "2021-01-21T00:00:00Z"
        # Current day
        current = datetime.now().replace().isoformat()
        url = f'https://api.covid19api.com/total/country/{country}?from={reference}&to={current}Z'
        response = requests.get(url)
        
        # Response exists
        if response.status_code == 200:
            return response.json()
        # Error
        else:
            return None

    @commands.command(aliases=['stat', 's'])
    async def stats(self, ctx, country):
        data = self.get_stat(country)
        # Error
        if data is None or len(data) == 0:
            await ctx.send("Error: This country is either not found in the database, or it was not spelt correctly.")
        # Country exists and is found in the database
        else:
            # Always access latest date with -1 index
            latest = data[-1]
            confirmed = latest["Confirmed"]
            deaths = latest["Deaths"]
            recovered = latest["Recovered"]
            active = latest["Active"]

            # Convert iso format to readable date
            date = datetime.fromisoformat(latest["Date"].replace("Z", ""))
            emb = discord.Embed(title=f'COVID Statistics for {country.title()}', color=0x7248d0, description=f'Date: {date}')

            emb.add_field(name="Confirmed", value=f'{confirmed:,}')
            emb.add_field(name="Deaths", value=f'{deaths:,}')
            emb.add_field(name="Recovered", value=f'{recovered:,}')
            emb.add_field(name="Active", value=f'{active:,}')
            
           
            if str(country) in eastern_list:
              #If an east asian country is being called, add in a message to reduce the stigma around east asians
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name="Eastern Asia Stigma", value="Beware! Although western media has ostracized east asian countries the most when it comes to Coronavirus, they have statistically handled it much better than western countries such as the USA.")
            elif str(country) == "usa":
              #If the USA is being compared, add in a message to point out USA's blunders
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name="America's Blunders", value="The USA has statistically proven itself to be the most irresponsible country when it comes to handling Coronavirus, as much as they would like you not to believe so.")
            else:
              pass

            await ctx.send(embed=emb)

    @commands.command(aliases=['comp', 'c'])
    async def compare(self, ctx, country1, country2):
        data1 = self.get_stat(country1)
        data2 = self.get_stat(country2)
        # Error
        if data1 is None or len(data1) == 0 or data2 is None or len(data2) == 0:
            await ctx.send("Error: At least one given country is either not found in the database, or it was not spelt correctly.")
        # Both countries exist and are found in the database
        else:
            # Always access latest date with -1 index
            latest1 = data1[-1]
            latest2 = data2[-1]
            confirmed1 = latest1["Confirmed"]
            confirmed2 = latest2["Confirmed"]
            deaths1 = latest1["Deaths"]
            deaths2 = latest2["Deaths"]
            recovered1 = latest1["Recovered"]
            recovered2 = latest2["Recovered"]
            active1 = latest1["Active"]
            active2 = latest2["Active"]

            # Convert iso format to readable date
            # Either date is fine
            date = datetime.fromisoformat(latest1["Date"].replace("Z", ""))
            emb = discord.Embed(title=f'{country1.title()} VS {country2.title()}', color=0x7248d0, description=f'Date: {date}')

            emb.add_field(name="Confirmed", value=f'{confirmed1:,} | {confirmed2:,}')
            emb.add_field(name="Deaths", value=f'{deaths1:,} | {deaths2:,}')
            emb.add_field(name="Recovered", value=f'{recovered1:,} | {recovered2:,}')
            emb.add_field(name="Active", value=f'{active1:,} | {active2:,}')
            
            
            if str(country1) in eastern_list or str(country2) in eastern_list:
              #If an east asian country is being compared, add in a message to reduce the stigma around east asians
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name="Eastern Asia Stigma", value="Beware! Although western media has ostracized east asian countries the most when it comes to Coronavirus, they have statistically handled it much better than western countries such as the USA.")
            elif str(country1) == "usa" or str(country2) == "usa":
              #If the USA is being compared, add in a message to point out USA's blunders
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name = chr(173), value = chr(173))
              emb.add_field(name="America's Blunders", value="The USA has statistically proven itself to be the most irresponsible country when it comes to handling Coronavirus, as much as they would like you not to believe so.")
            else:
              #If neither of these conditions are fulfilled, just send the embed
              pass
            
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(Statistics(client))
