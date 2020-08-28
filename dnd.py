from discord.ext import commands
import ease_of_use as eou
from importlib import *
from random import *
import requests as r
import discord
import json



# define getData() and setData()
def getData():
	with open("data.json", "r") as dataFile:
		return json.loads(dataFile.read())

def setData(_in):
	with open("data.json", "w") as dataFile:
		dataFile.write(json.dumps(_in, indent=4))



class DND(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	def cog_unload(self):
		eou.log(text="Offline", cog="DND", color="red")



	@commands.command(brief="")
	async def getexact(self, ctx, section, name):
		try:
			await ctx.message.delete()
		except:
			pass


		valid_sections_r = r.get(url="https://www.dnd5eapi.co/api/").json()
		valid_sections = valid_sections_r.keys()
		if section not in valid_sections:
			embed = eou.makeEmbed(title="That wasn't a valid section!", description="__Valid Sections are:__\n- %s" % ("\n- ".join(valid_sections)))
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return eou.log(text="Attempted to search dnd (invalid section)", ctx=ctx)



		request = r.get(url="https://www.dnd5eapi.co/api/%s/%s" % (section, name)).json()
		if "error" in request:
			embed = eou.makeEmbed(title="Whoops!", description="I couldn't find that!")
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return eou.log(text="Attempted to search dnd (invalid name)", ctx=ctx)


		embed = eou.makeEmbed(title=request["name"], description="")


		if section == "monsters":
			# output_string = "Size: %s\nType: %s\nAlignment: %s\nAC: %s\nHP: %s\nSpeed: %s" % (request["size"], request["type"], request["alignment"], request["armor_class"], request["hit_points"], ", ".join(["%s %sing" % (value[value], value) for key, value in request["speed"]]))
			for stat in ["size", "type", "alignment", "armor_class"]:
				embed.add_field(name=stat.replace("_", " ").title(), value=request[stat], inline=True)
			embed.add_field(name="Hit Points", value="%s (%s)" % (request["hit_points"], request["hit_dice"]))
			embed.add_field(name="Speed", value="\n".join(["%s %sing" % (request["speed"][key], key) for key in request["speed"]]))
		else:
			output_string = "```json\n" + json.dumps(request, indent=4) + "```"
			if len(output_string) > 2000:
				output_string = output_string[:1750] + "...```\n\n(longer than 2000 characters)"
			embed = eou.makeEmbed(title=request["name"], description=output_string)


		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		return eou.log(text="Searched dnd (section = %s, terms=[%s])" % (section, name), ctx=ctx)



	@commands.command(brief="")
	async def searchdnd(self, ctx, section, *, search_terms=""):
		try:
			await ctx.message.delete()
		except:
			pass


		valid_sections_r = r.get(url="https://www.dnd5eapi.co/api/").json()
		valid_sections = valid_sections_r.keys()
		if section not in valid_sections:
			embed = eou.makeEmbed(title="That wasn't a valid section!", description="__Valid Sections are:__\n- %s" % ("\n- ".join(valid_sections)))
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return eou.log(text="Attempted to search dnd (invalid section)", ctx=ctx)


		if search_terms == "" or search_terms.startswith("page="):
			request = r.get(url="https://www.dnd5eapi.co/api/%s" % section).json()
			results_array = request["results"]
			results = [item["index"] for item in results_array]
			if "page" in search_terms:
				page = int(search_terms.split("=")[1])
			else:
				page = 0
			output_string = "- %s" % "\n- ".join(results)[(1750*page):]
			print(len(output_string))
			if len(output_string) > 2000:
				output_string = output_string[:(1750*(page+1))] + "...\n\n(longer than 2000 characters)"
			embed = eou.makeEmbed(title=section.title() + " (%s results)" % request["count"], description=output_string)
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return eou.log(text="Searched dnd (section = %s)" % section, ctx=ctx)


		split_terms = search_terms.split(", ")
		fixed_terms = "&".join(split_terms)
		request = r.get(url="https://www.dnd5eapi.co/api/%s/?%s" % (section, fixed_terms)).json()
		results_array = request["results"]


		if request["count"] == 1:
			result = results_array[0]
			request = r.get(url="https://www.dnd5eapi.co%s" % result["url"]).json()


			output_string = ""
			embed = eou.makeEmbed(title=request["name"], description=output_string)


			if section == "monsters":
				# output_string = "Size: %s\nType: %s\nAlignment: %s\nAC: %s\nHP: %s\nSpeed: %s" % (request["size"], request["type"], request["alignment"], request["armor_class"], request["hit_points"], ", ".join(["%s %sing" % (value[value], value) for key, value in request["speed"]]))
				for stat in ["size", "type", "alignment", "armor_class"]:
					embed.add_field(name=stat.replace("_", " ").title(), value=request[stat], inline=True)
				embed.add_field(name="Hit Points", value="%s (%s)" % (request["hit_points"], request["hit_dice"]))
				embed.add_field(name="Speed", value="\n".join(["%s %sing" % (request["speed"][key], key) for key in request["speed"]]))

			else:
				output_string = "```json\n" + json.dumps(request, indent=4) + "```"
				if len(output_string) > 2000:
					output_string = output_string[:1750] + "...```\n\n(longer than 2000 characters)"


			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return eou.log(text="Searched dnd (section = %s, terms=[%s])" % (section, search_terms), ctx=ctx)


		else:
			results = [item["index"] for item in results_array]
			output_string = "- %s" % "\n- ".join(results)
			if len(output_string) > 2000:
				output_string = output_string[:1750] + "...\n\n(longer than 2000 characters)"
			embed = eou.makeEmbed(title="I got %s results for \"%s\"" % (request["count"], search_terms), description=output_string)
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return eou.log(text="Searched dnd (section = %s, terms=[%s])" % (section, search_terms), ctx=ctx)



def setup(bot):
	eou.log(text="Online", cog="DND", color="red")
	bot.add_cog(DND(bot))
	reload(eou)
