import discord
import os
import sys
import io
from discord.ext import commands, tasks
# from itertools import cycle 
# from keep_alive import keep_alive
from discord.ext.commands import CommandNotFound
import discord.ext.commands
import nacl
import asyncio
import time
# import tracemalloc
import json
import random
import eyed3
import itertools
import more_itertools

# import requests
# import selenium

# req = requests.get('http://readycloud.netgear.com/client/index.html')
# print(dir(req))
# print(help(req))
# print(req.text)

# tracemalloc.start()
client = commands.Bot(command_prefix = ".")
member = discord.Client()
hub = os.listdir("C:/Users/LucaN/Downloads/music")
dirlen = len(hub)
msg = None
music = None
curr = None
detect = None
queue = None
check = False
toggle = None
counter = None
new_order = None
player = None
p2 = None
p3 = None
alpha = None
number = None
single_play = None
kur = None
queued = []
slot = {}
prev = None
loop = None
length = None
slot2 = {}
order_backup = None
queued2 = {}
update = {}
dummy = []

for test in hub:
	if test.endswith(".mp3"):
		dummy.append(test)
	else:
		pass

for test2 in dummy:
	update[test2] = dummy.index(test2)
	
def numbers():
	f = open("C:/Users/LucaN\Discord-Music-Bot/config.json", "r")
	data = json.load(f)
	mason = data["token"]
	f.close()
	return mason
	

@client.event
async def on_ready():
	print("bot is ready")

@client.command()
async def shutdown(ctx):
	if ctx.message.author.id == ctx.guild.owner_id or ctx.message.author.id == 592605224410152970: 
		try:
			await ctx.voice_client.disconnect()	
			client.remove_command(repeat)
			repeater.cancel()
			shuffling.cancel()
			ordering.cancel()
		except:
			pass		
		sys.exit()
	else:
		await ctx.send("You do not have permission to use this command")		

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		return
	raise error

@client.event
async def on_message(message):
	if message.content.startswith('.'):
		global msg
		await client.process_commands(message)
		msg = await client.get_context(message)
	else:
		pass		    

# @client.listen("on_message")
# async def on_message(message):
# 	if message.content.startswith('.skip') or message.content.startswith('.back'):
# 		global detect
# 		await client.process_commands(message)
# 		detect = True
# 	else:
# 		pass
# 	if message.content.startswith('.'):
# 		global msg
# 		await client.process_commands(message)
# 		msg = await client.get_context(message)
# 		ctx = msg
# 		x = 0
# 		print(len(client.all_commands))
# 		while x < (len(client.all_commands) - 1):
# 			if message == client.all_commands[x]:
# 				pass
# 			else:
# 				x += 1
# 				if x == (len(client.all_commands) - 1): 		
# 					await ctx.send("That command doesn't exist")	

@client.event
async def on_voice_state_update(member, before, after):
	if msg is not None:
		ctx = msg	
		voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
		member_count = len(voiceChannel.members)
		try:
			if before.channel is not None and after.channel is None and member_count == 1 and ctx.voice_client.is_connected() is True:
				if ctx.voice_client.is_playing() is True:
					ctx.voice_client.pause()
				elif ctx.voice_client.is_playing() is False:
					await ctx.voice_client.disconnect()
			elif before.channel is None and after.channel is not None and member_count > 1 and ctx.voice_client.is_connected() is True:
				if ctx.voice_client.is_paused() is True:
					ctx.voice_client.resume()		
			else:
				pass
		except AttributeError:
			pass			
	else:
		pass			

@client.command()
async def stop(ctx):
	if ctx.message.author.voice != None:
		try:
			client.remove_command(repeat)
			repeater.cancel()
			client.remove_command(back)
			client.remove_command(skip)
			ordering.cancel()
			shuffling.cancel()
		except:
			pass
		try:	
			await ctx.voice_client.stop()
		except:
			pass		
	else:
		await ctx.send("There is nothing playing")
		

@commands.command(aliases = ['f'])
async def forward(ctx):
	repeater.stop()
	client.remove_command(forward)	
	

@commands.command(aliases = ['re'])
async def repeat(ctx):
	repeater.start(ctx)
	client.add_command(forward)

@tasks.loop(count=None)
async def repeater(ctx):
	if ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))

@client.command()
async def cmds(ctx):
	await ctx.send("Here's the list of commands")
	for cmd in client.commands:
		await ctx.send(str(cmd)+"\n")

@client.command(aliases = ['o'])
async def order(ctx):
	global queued2
	global music
	global curr
	global counter

	counter = 0
	queue2 = []
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	curr = 0

	try:
		queued2.clear()
	except:
		pass	
	
	try:
		if ctx.voice_client.is_playing() == True or ctx.voice_client.is_paused() == True:
			ctx.voice_client.stop()
	except:
		pass	

	try:
		shuffling.cancel()
	except:
		pass	

	if ctx.message.author.voice != None:
		if ctx.voice_client is None:
			await voiceChannel.connect()
	else:
		await ctx.send("You are not in the channel")

	for b in hub:
		if b.endswith(".mp3"):
				queue2.append(b)
		else:
			pass
	for x in queue2:
		queued2[x] = queue2.index(x)

	try:	
		client.add_command(back)
		client.add_command(skip)
		client.add_command(add)
	except:
		pass	

	ordering.start(ctx)
											

@tasks.loop(count=None)
async def ordering(ctx):
	global curr
	global counter
	global music

	if ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
		queue2 = list(queued2)
		music = queue2[curr]
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
		music2 = music.replace(".mp3", "")
		if counter == 0:
			await ctx.send("Now playing "+ str(music2))
		else:
			await ctx.send(str(music2))
		curr += 1	
		counter += 1
		if curr > (len(queued2)-1):	
			curr = 0
		else:
			pass	
	else:
		await asyncio.sleep(.1)

@client.command(aliases = ['s'])
async def shuffle(ctx):
	global queued2
	global music
	global curr
	global counter

	counter = 0
	queue2 = []
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	curr = 0

	try:
		queued2.clear()
	except:
		pass	
	
	try:
		if ctx.voice_client.is_playing() == True or ctx.voice_client.is_paused() == True:
			ctx.voice_client.stop()
	except:
		pass		

	try:
		ordering.cancel()
	except:
		pass	

	if ctx.message.author.voice != None:
		if ctx.voice_client is None:
			await voiceChannel.connect()
	else:
		await ctx.send("You are not in the channel")

	for b in hub:
		if b.endswith(".mp3"):
				queue2.append(b)
		else:
			pass

	random.shuffle(queue2)

	for x in queue2:
		queued2[x] = queue2.index(x)


	try:	
		client.add_command(back)
		client.add_command(skip)
		client.add_command(add)
	except:
		pass	

	shuffling.start(ctx)

@tasks.loop(count=None)
async def shuffling(ctx):
	global curr
	global counter
	global music

	if ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
		queue2 = list(queued2)
		music = queue2[curr]
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
		music2 = music.replace(".mp3", "")
		if counter == 0:
			await ctx.send("Now playing "+ str(music2))
		else:
			await ctx.send(str(music2))
		curr += 1	
		counter += 1
		if curr > (len(queued2)-1):	
			curr = 0
		else:
			pass		
	else:
		await asyncio.sleep(.1)

@commands.command(aliases = ['>'])
async def skip(ctx):
	global curr
	if ctx.voice_client.is_playing() is True or ctx.voice_client.is_paused() is True:
		ctx.voice_client.stop()
	else:
		await ctx.send("Nothing is playing right now")	

@commands.command(aliases = ['<'])
async def back(ctx):
	global curr
	if ctx.voice_client.is_playing() is True or ctx.voice_client.is_paused() is True:
		ctx.voice_client.stop()
		curr -= 2
	else:
		await ctx.send("Nothing is playing right now")

@client.command(aliases = ['a'])
async def add(ctx, song_name):
	global music
	global curr
	global queued2
	global update
	# music = song_name
	song_list = []
	dup_list = []
				
	word2 = [char for char in song_name]
	try:
		if len(word2) <= 0 or str(word2[0]) == " ":
			await ctx.send("Sorry I couldn't find that song")
		else:
			pass
	except IndexError:
		pass				

	if song_name.endswith(".mp3"):
		song_name = song_name.replace(".mp3", "")	
	song = song_name.lower().split()
	for b in hub:
		if b.endswith(".mp3"):
			b = b.replace(".mp3","")
			song_list.append(b)			

	count = 0
	for x in song_list:
		z = x
		x = x.lower()
		for y in song:
			if y in x:
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0

		if count == len(song):
			dup_list.append(z)
			count = 0
		else:
			count = 0

	if len(dup_list) > 1 and len(dup_list) < 76:
		num = 0
		while num < (len(dup_list)):
			if len(dup_list[num]) == len(song_name):			
				nxt = dup_list[num]+".mp3"
				update = queued2
				og = update[nxt]
				if curr != og:
					if curr == len(update):
						update[nxt] = 0
					elif curr > -1 and curr < og:
						update[nxt] = curr	
						for kur in update:
							if curr <= update[kur] < og and kur != nxt:
								update[kur] = update[kur]+1
							else:
								pass
					else: 
						if curr > og:
							update[nxt] = curr -1
							for kur in update:
								if og < update[kur] < curr and kur != nxt:
									update[kur] = update[kur]-1
								else:
									pass
							curr -= 1
						elif (len(update)-abs(curr)) > og:
							update[nxt] = (len(update)-abs(curr)) -1 
							for kur in update:
								if og < update[kur] < (len(update)-abs(curr)) and kur != nxt:
									update[kur] = update[kur]-1
								else:
									pass
							curr = (len(update)-abs(curr)) - 1							
					await asyncio.sleep(.1)	
					queue2 = sorted(update.items(), key=lambda x:x[1])
					queued2 = dict(queue2)
				else:
					pass	
				break
			else:
				num+=1

		if num == (len(dup_list)):
			await ctx.send("Here are a couple of songs that share a similar name. Can you specify which one?")
			for l in dup_list:
				await ctx.send(str(l))			

	elif len(dup_list) > 75:
		await ctx.send("Sorry I couldn't find that song")

	elif len(dup_list) == 1:		
		nxt = dup_list[0]+".mp3"
		update = queued2
		og = update[nxt]
		if curr != og:
			if curr == len(update):
				update[nxt] = 0
			elif curr > -1 and curr < og:
				update[nxt] = curr	
				for kur in update:
					if curr <= update[kur] < og and kur != nxt:
						update[kur] = update[kur]+1
					else:
						pass
			else: 
				if curr > og:
					update[nxt] = curr - 1
					for kur in update:
						if og < update[kur] < curr and kur != nxt:
							update[kur] = update[kur]-1
						else:
							pass
					curr -= 1
				elif (len(update)-abs(curr)) > og:
					update[nxt] = (len(update)-abs(curr)) -1
					for kur in update:
						if og < update[kur] < (len(update)-abs(curr)) and kur != nxt:
							update[kur] = update[kur]-1
						else:
							pass
					curr = (len(update)-abs(curr)) - 1									
			await asyncio.sleep(.1)	
			queue2 = sorted(update.items(), key=lambda x:x[1])
			queued2 = dict(queue2)		
		else:
			pass					
	else:
		await ctx.send("Sorry I couldn't find that song")

@client.command()
async def songs(ctx):
	try:
		os.remove("songs.txt")
	except:
		pass	
	f = open("songs.txt", "w", encoding='utf8')
	x = 0

	for x in range(dirlen):
		song = str(hub[x])
		if song.endswith(".mp3"):
			z = ''.join(('"',song,'"'))
			f.write(z+"\n")
		else:
			continue
	f.close()		
	with open("songs.txt", "rb") as file:
		await ctx.send("Ayo! Here's the list of songs:", file=discord.File(file, "songs.txt"))
	f.close()

@client.command(aliases = ['pl'])
async def play(ctx, song_name):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	value = None
	global music
	music = song_name
	song_list = []
	dup_list = []

	try:
		shuffling.stop()
	except:
		pass

	try:
		ordering.stop()
	except:
		pass		

	client.remove_command(skip)
	client.remove_command(back)
	client.remove_command(add)

	if ctx.message.author.voice != None:
		if ctx.voice_client is None:
			await voiceChannel.connect()
	else:
		await ctx.send("You are not in the channel")				

	word2 = [char for char in song_name]
	try:
		if len(word2) <= 0 or str(word2[0]) == " ":
			await ctx.send("Sorry I couldn't find that song")
		else:
			pass
	except IndexError:
		pass				

	if song_name.endswith(".mp3"):
		song_name = song_name.replace(".mp3", "")	
	song = song_name.lower().split()
	for b in hub:
		if b.endswith(".mp3"):
			b = b.replace(".mp3","")
			song_list.append(b)			

	count = 0
	for x in song_list:
		z = x
		x = x.lower()
		for y in song:
			if y in x:
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0

		if count == len(song):
			dup_list.append(z)
			count = 0
		else:
			count = 0

	if len(dup_list) > 1 and len(dup_list) < 76:
		num = 0
		while num < (len(dup_list)):
			if len(dup_list[num]) == len(song_name):
				try:
					value = ctx.voice_client.is_playing()
					if value == True:
						ctx.voice_client.stop()
				except:
					pass		
				music = dup_list[num]+".mp3"
				ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
				await ctx.send("Now playing "+ str((dup_list[num])))
				try:
					client.add_command(repeat)
				except:
					pass
				break
			else:
				num+=1

		if num == (len(dup_list)):
			await ctx.send("Here are a couple of songs that share a similar name. Can you specify which one?")
			for l in dup_list:
				await ctx.send(str(l))

	elif len(dup_list) > 75:
		await ctx.send("Sorry I couldn't find that song")

	elif len(dup_list) == 1:
		try:
			value = ctx.voice_client.is_playing()
			if value == True:
				ctx.voice_client.stop()
		except:
			pass		
		music = dup_list[0]+".mp3"
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
		await ctx.send("Now playing "+ str((dup_list[0])))
		try:
			client.add_command(repeat)
		except:
			pass
	else:
		await ctx.send("Sorry I couldn't find that song")
											

@client.command()
async def leave(ctx):
	if ctx.message.author.voice != None:
		if ctx.voice_client != None:
			try:
				client.remove_command(repeat)
				repeater.cancel()
				await ctx.voice_client.stop()
			except:
				pass				
			await ctx.voice_client.disconnect()
		else:
			await ctx.send("I'm not there")		
	else:
		await ctx.send("You are not in the channel")				

@client.command(aliases = ['p'])
async def pause(ctx):
	if ctx.message.author.voice != None:
		try:
			if ctx.voice_client.is_paused() == False:
				ctx.voice_client.pause()
				# while ctx.voice_client.is_paused() == True:
				# 	await asyncio.sleep(.1)
			else:
				await ctx.send("The song is already paused")	
		except:
			await ctx.send("There is nothing playing")
	else:
		await ctx.send("You are not in the channel")			

@client.command(aliases = ['r'])
async def resume(ctx):
	if ctx.message.author.voice != None:
		try:
			if ctx.voice_client.is_playing() is True:
				await ctx.send("The song is already playing")
			elif ctx.voice_client.is_paused() == True:
				ctx.voice_client.resume()
		except:
			await ctx.send("There is nothing playing")
	else:
		await ctx.send("You are not in the channel")

client.run(numbers())


