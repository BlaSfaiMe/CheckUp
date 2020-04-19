import discord
import json
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '/')

async def loadWorks():
	with open("travaux.json", "r") as f:
		client.eleves = json.load(f)

client.loop.create_task(loadWorks())

matieres = dict({1: 'espagnol', 2: 'anglais', 3: 'snt', 4: 'francais', 5: 'mathematiques', 6: 'ses'})

works_channel = [689022870562537546, 688111026985631752, 688114293647867904, 688109834759045205, 688007352250531880, 688110860492865581]
prof_channel = [688111945856974863, 688111009898037256, 688114275730194496, 688021788709355530, 688109759001657366, 688110935382294597]
categories = dict({688111914194042930: 'e', 688110755010183248: 'a', 688114143190188074: 'sn', 688109713988386865: 'ma', 688111287946706969: 'se', 688109391689416735: "f"})
matiere_ab = ["m", "f", "a", "e", "se", "sn", "help"]
matiere_dict = dict({"m": "Mathématiques", "f": "Français", "a": "Anglais", "e": "Espagnol", "se": "SES", "sn": "SNT"})


@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Créé par Kestrel'))
	print('bot logged on as {0}!'.format(client.user))

@client.event
async def on_reaction_add(reaction, user):
	print(user.name)
	
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.message.delete(delay=0)
		m = await ctx.send("Cette commande n'existe pas.")
		await m.delete(delay=2)
@client.command(pass_context=True)
async def reset(ctx):
	if ctx.author.id != 295316854044622849:
		await ctx.send("🛑 Tu ne peux pas faire ceci. C'est très dangereux ! 🛑")
	else:
		with open ("travaux.json", "r") as f:
			client.eleves = json.load(f)
		with open("travaux.json", "w") as f:
			for user in ctx.guild.members:
				if ctx.guild.get_role(688125738121035778) in user.roles:
					user_id = user.id
					client.eleves[user_id] = {}
					client.eleves[user_id]["m"] = {
						"state": False,
						"link": ""
					}
					client.eleves[user_id]["f"] = {
						"state": False,
						"link": ""
					}
					client.eleves[user_id]["a"] = {
						"state": False,
						"link": ""
					}
					client.eleves[user_id]["e"] = {
						"state": False,
						"link": ""
					}
					client.eleves[user_id]["se"] = {
						"state": False,
						"link": ""
					}
					client.eleves[user_id]["sn"] = {
						"state": False,
						"link": ""
					}
					print("Initialisation pour "+user.name+" effectuée.")
			json.dump(client.eleves, f, indent=4)
			print("Initialisation complètemment effectuée.")
		await ctx.send("L'initialisation s'est correctement effectuée.")

@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send('Bot ping is {0}'.format(client.latency))

@client.command(pass_context=True)
async def work(ctx, title, *desc):
	msg = ctx.message
	embed = discord.Embed(title='by {0}'.format(ctx.message.author.name),colour=discord.Colour.red())
	output = ''
	for d in desc:
		output += d+' '
	embed.add_field(name='{0}'.format(title), value=output, inline=False)
	await ctx.send('J\'ai créé le travail ! Ajoute une réaction au message ci-dessous pour signaler que tu l\'as fini et rendu !')
	travail = await ctx.send(embed=embed)
	await travail.add_reaction('✅')
	
@client.command(pass_context=True)
async def erase(ctx):
	with open("travaux.json", "w") as f:
		f.truncate()

@client.command(pass_context=True)
async def fait(ctx, matiere):
	category_id = ctx.channel.category_id
	if category_id in categories:
		if matiere not in matiere_ab:
			await ctx.send("L'identifiant de la matière n'est pas bon. C'est la première lettre du nom de la matière que vous voulez.")
		else:
			with open("travaux.json", "w") as f:
				client.eleves[str(ctx.author.id)][str(matiere)] = {
					"state": True,
					"link": ctx.message.jump_url
				}
				json.dump(client.eleves, f, indent=4)
				m = await ctx.send("Ton travail a été marqué comme fait !")
				await m.delete(delay=2)
	else:
		await ctx.send("Tu ne peux pas faire ceci dans ce channel. Fait /matiere pour aller sur le channel concerné !")
	

@client.command(pass_context=True)
async def react(ctx):
	msg = ctx.message
	await msg.add_reaction('😂')

def is_me(m):
	return m.author == client.user

@client.command(pass_context=True)
async def clear(ctx, amount=20):
	role = discord.utils.get(ctx.guild.roles, name='staff')
	if role in ctx.author.roles:
		channel = ctx.message.channel
		a = amount+1
		await channel.purge(limit=a)
		m = await ctx.send('J\'ai supprimé {0} messages !'.format(amount))
		await m.delete(delay=2)
	else:
		await ctx.send('🛑 Tu n\'as pas la permission de faire ça ! Contacte un administateur si c\'est anormal. 🛑')

@client.command(pass_context=True)
async def stop(ctx):
	msg = ctx.message
	if msg.author.id == 295316854044622849:
		await ctx.send('Extinction en cours...')
		await client.logout()
	else:
		await ctx.send("🛑 Tu ne peux pas faire ça ! 🛑")
		
@client.command(pass_context=True)
async def reload(ctx):
	if ctx.author.id == 295316854044622849:
		await ctx.send("Redémmarage en cours...")
		await client.logout()
		await client.login('NzAwNjE4MjMwOTY4MDkwNjg3.XplleQ.b7DfyX8NqrwBbbLBoEIQOc6MJd0')
		await client.connect()
		await ctx.send("Redémmarage fini !")

@client.command(pass_context=True)
async def matiere(ctx):
	embed = discord.Embed(title='Les matières disponibles', colour=discord.Colour.red())
	embed.set_footer(text="Robot créé par @Kestrel#1877", icon_url="https://cdn.discordapp.com/avatars/295316854044622849/4a571e4551c040367f51d2fad8d8e18f.png")
	print(matieres)
	for k,v in matieres.items():
		channel_id = works_channel[k-1]
		embed.add_field(name=v, value='<#{1}>'.format(v, channel_id), inline=False)
	await ctx.send(embed=embed)
@client.command(pass_context=True)
async def rendu(ctx, travail):
	if travail == "help":
		embed = discord.Embed(title="Aide concernant l'outils de rendu", colour=discord.Colour.red())
		embed.add_field(name="`Les matières disponibles`", value="Les matières disponibles doivent être rentrées après le `/rendu`. Elles sont identifiées avec leur première lettre. Exemple: /rendu m (pour la SES, l'identifiant est se et pour la SNT, sn)")
		await ctx.send(embed=embed)
	if travail != "help":
		if travail not in matiere_ab:
			await ctx.send("🛑 Vous n'avez pas saisi un indentifiant de matière correct ! `/rendu help` pour plus d'information.")
		else:
			embed = discord.Embed(title="élèves ayant rendu leur travail en "+matiere_dict[travail])
			embed.set_footer(text="Robot créé par @Kestrel#1877", icon_url="https://cdn.discordapp.com/avatars/295316854044622849/4a571e4551c040367f51d2fad8d8e18f.png")
			author = ctx.author
			with open("travaux.json", "r") as f:
				client.eleves = json.load(f)
				for eleve in ctx.guild.members:
					if ctx.guild.get_role(688125738121035778) in eleve.roles:
						eleve_id = str(eleve.id)
						rendu = client.eleves[eleve_id][travail]["state"]
						link = client.eleves[eleve_id][travail]["link"]
						
						if rendu == False:
							embed.add_field(name="`{0}`".format(eleve.display_name), value="🔴", inline=True)
						elif rendu == True:
							embed.add_field(name="`{0}`".format(eleve.display_name), value="🟢 [Son travail]({0})".format(link), inline=True)
			await ctx.send(embed=embed)

@client.event
async def on_message(message):
	await client.process_commands(message)
	if message.author.bot:
		return
			
			

client.run('NzAwNjE4MjMwOTY4MDkwNjg3.XplleQ.b7DfyX8NqrwBbbLBoEIQOc6MJd0')
