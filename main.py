from bs4 import BeautifulSoup
from requests_html import HTMLSession
from webdriver import keep_alive
import discord
import time
import requests

from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=""))
	print(f'Logged in as {bot.user.name}')

@commands.command(name="views")
@commands.cooldown(1, 3600, commands.BucketType.user)
async def views(ctx, arg, arg2):
	try:
		cooless = discord.Embed(title='Processing...', description="currently adding {} views to your listing".format(str(arg)), color=0x32a852)
		await ctx.send(embed = cooless)
		try:
			arg1 = int(arg)
		except:
			ctx.send("Not a Valid Argument. Please send a Whole Number")
		try:
			arg2 = str(arg2)
		except:
			ctx.send("Not a valid String please try again...")

		with open('proxies.txt', 'r') as working:
			proxwy = working.read().splitlines()
		for i in range(arg1):
			try:
				proxi2es = {
						"http": "http://" + str(proxwy[0])			
						}
				requests.get(arg2, proxies = proxi2es)
			except:
				print("proxy failed")
		msg = '{0.author.mention}'.format(ctx)
		cooless = discord.Embed(title='Success!', description="Added {} views to your listing\n\n **Your Listing: **{}".format(str(arg), str(arg2)), color=0x32a852)
		cooless.set_thumbnail(url="https://s5.gifyu.com/images/ezgif.com-optimized7ce94c5d4a783cb.gif")
		await ctx.send(msg, embed = cooless)
	except commands.errors.CommandOnCooldown:
		embed = discord.Embed(title='Failure!', description="**Woah! Slow down there. Try adding views later \n\n Note - Cooldown for views is an hour", color=0x32a852)
		embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2YaAu9Al0HqymPNvpYmpKOnSI3Cr8j9iJzPChqwsaBA/https/images-ext-1.discordapp.net/external/q8Z7X_zsd-t0HOQUX8l1wz69GXJM_iPu43UzRAd7_dE/https/i.lensdump.com/i/iUcB9k.png")
		ctx.send(embed=embed)

@views.error
async def views_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(title='Failure!', description="**Woah! Slow down there. Cooldown time left: `{} seconds`".format(str(error.retry_after)), color=0x32a852)
		embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2YaAu9Al0HqymPNvpYmpKOnSI3Cr8j9iJzPChqwsaBA/https/images-ext-1.discordapp.net/external/q8Z7X_zsd-t0HOQUX8l1wz69GXJM_iPu43UzRAd7_dE/https/i.lensdump.com/i/iUcB9k.png")
		await ctx.send(embed=embed)
	else:
		raise error

@commands.command(name="fees")
async def fees(ctx, arg):
	inp = int(arg)
	ebay = inp * 0.90
	amazon = inp * 0.85

	await ctx.send("Amazon: $" + str(amazon))
	await ctx.send("Ebay: $" + str(ebay))


@commands.command(name="ebay")
async def ebay(ctx, *args):
	session = HTMLSession()
	url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={}".format('+'.join(args))
	url2 = "&_sacat=0&LH_TitleDesc=0&rt=nc&LH_Sold=1&LH_Complete=1" 
	mainurl = str(url) + url2
	print(mainurl)
	nice = discord.Embed(title='Processing...', description="**Please wait. This could take up to 30 seconds**\n\n **Your Item:** __{}__".format(' '.join(args)), color=0x32a852)
	await ctx.send(embed=nice)
	response = session.get(mainurl)
	soup = BeautifulSoup(response.content, 'html.parser')
	question = soup.select('.s-item__price')
	question = str(question)
	soup = BeautifulSoup(question,'html.parser')
	a_tag=soup('span')
	cool = []
	for tag in a_tag:
		coolness = tag.text.strip()
		cool.append(coolness)
	ool = []
	for item in cool:
		nice = item.replace('$', '' )
		coosl = nice.replace(',', '' )
		if 'to' in coosl:
			print("'to' detected....ignoring")
		else:
			ool.append(float(coosl))
	items = len(ool)
	total = sum(map(float, ool))
	average = total/items
	average = round(average, 2)
	cooless = discord.Embed(title='Success!', description="**Average Price on Ebay**: ${}\n\n**Items Indexed:** __{}__ **Your Item:** __{}__\n\n **Listing Page: **{}".format(average, items, ' '.join(args), mainurl), color=0x32a852)
	await ctx.send(embed = cooless)

bot.add_command(ebay)
bot.add_command(fees)
bot.add_command(views)

keep_alive()

bot.run('')


