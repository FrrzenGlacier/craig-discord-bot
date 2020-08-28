from discord.ext import commands
import ease_of_use as eou
import discord
import json
import sys



# create the bot
bot = commands.Bot(command_prefix="c.")



# define getData() and setData()
def getData():
	with open("data.json", "r") as dataFile:
		return json.loads(dataFile.read())

def setData(_in):
	with open("data.json", "w") as dataFile:
		dataFile.write(json.dumps(_in, indent=4))



# clear the console and load all the cogs
eou.clear()
cogs = getData()["cogs"]
for cog in cogs:
	bot.load_extension(cog)
	eou.log(text=("%s loaded" % cog.title()))


# define a function for checking if a user is an owner of the bot
async def is_owner(ctx):
	return ctx.author.id in [184474965859368960, 696087051619008612]


# when connected, say so
@bot.event
async def on_connect():
	eou.log(text="Connected")


# when disconnected, say so
@bot.event
async def on_disconnect():
	eou.log(text="Disconnected")


# when ready, say so, and set game activity
@bot.event
async def on_ready():
	eou.log(text="Ready")
	game = discord.Activity(type=discord.ActivityType.listening, name="c.help")
	await bot.change_presence(status=discord.Status.online, activity=game)


# c.reload [cog] - reload one or more of the bots cogs
@bot.command(name="reload", brief="Reload one or all of the bots cogs")
@commands.check(is_owner)
async def _reload(ctx, cog="all"):
	try:
		await ctx.message.delete()
	except:
		pass
	log = []
	cogs = getData()["cogs"]
	if cog == "all":
		for extension in cogs:
			try:
				bot.reload_extension(extension)
				log.append(f"**{extension.title()}** reloaded successfully.")
			except:
				bot.load_extension(extension)
				log.append(f"**{extension.title()}** loaded successfully.")

		embed = eou.makeEmbed(title="Reloaded Cogs" % ctx.author.name, description="\n".join(log))
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		eou.log(text="Reloded all modules", ctx=ctx)
	else:
		try:
			bot.reload_extension(cog)
			embed = eou.makeEmbed(title=f"Reloaded {cog.title()}", description="Successfully reloaded!")
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
		except:
			bot.load_extension(cog)
			embed = eou.makeEmbed(title=f"Loaded {cog.title()}", description="Successfully loaded!")
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
		eou.log(text="Reloaded %s" % cog.title(), ctx=ctx)


# if reload gets an error, say that the invoker wasnt an owner of the bot
@_reload.error
async def _reload_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		try:
			await ctx.message.delete()
		except:
			pass
		embed = eou.makeEmbed(title="Whoops!", description="Only the bot owner can do that command.")
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		eou.log(text="Attempted to reload cog(s) - Missing permissions", ctx=ctx)


# c.ping - just check if craig is online
@bot.command(brief="Check if the bot is online")
async def ping(ctx):
	embed = eou.makeEmbed(title="Pong!", description="Craig is online.")
	embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)
	eou.log(text="Pinged the bot", ctx=ctx)


# c.invite - get an invite link for craig
@bot.command(brief="Get an invite link fron Craig")
async def invite(ctx):
	embed = eou.makeEmbed(title="Want to add me?", description="[Invite me with this link!](https://discord.com/api/oauth2/authorize?client_id=748956804582735992&permissions=0&scope=bot)")
	embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)
	eou.log(text="Got an invite link", ctx=ctx)


# load craig from a text file
with open("T:/all 2/tokens/craig.txt", "r") as token:
	bot.run(token.read())
