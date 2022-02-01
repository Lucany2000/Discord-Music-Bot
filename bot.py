from asyncore import read
from xml.etree.ElementInclude import include
import discord
import os
import sys
import io
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
import discord.ext.commands
import nacl
import asyncio
import time
# import tracemalloc
import json
import random
import itertools
import more_itertools
import openpyxl
from tinytag import TinyTag

# import requests
# import selenium

# tracemalloc.start()
client = commands.Bot(command_prefix = ".")
member = discord.Client()
hub = os.listdir("C:/Users/LucaN/Downloads/music")
dirlen = len(hub)
msg = None
music = None
curr = None
tog = None
n_toggle = 0
counter = None
order_backup = None
queued = {}
update = {}
q_counter = 0

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
			client.remove_command(back)
			client.remove_command(skip)
			client.remove_command(add)
			client.remove_command(nxt)
		except:
			pass
		try:
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

@client.command(aliases = ['st'])
async def stop(ctx):
	if ctx.message.author.voice != None:
		try:
			client.remove_command(repeat)
			repeater.cancel()
			client.remove_command(back)
			client.remove_command(skip)
			client.remove_command(add)
			client.remove_command(nxt)
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

# @client.command()
# async def help(ctx):
# 	await ctx.send("Here's the list of commands")
# 	for cmd in client.commands:
# 		await ctx.send(str(cmd)+"\n")

@client.command(aliases = ['o'])
async def order(ctx):
	global queued
	global music
	global curr
	global counter

	counter = 0
	queue = []
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	curr = 0

	try:
		queued.clear()
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
				queue.append(b)
		else:
			pass
	for x in queue:
		queued[x] = queue.index(x)

	print(queued)	

	try:	
		client.add_command(back)
		client.add_command(skip)
		client.add_command(add)
		client.add_command(nxt)
	except:
		pass	

	ordering.start(ctx)
											

@tasks.loop(count=None)
async def ordering(ctx):
	global curr
	global counter
	global music
	global q_counter
	global n_toggle

	if ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
		queue = list(queued)
		if curr < 0:
			curr = (len(queue)-abs(curr))
		else:
			pass
		music = queue[curr]
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
		music2 = music.replace(".mp3", "")
		if counter == 0:
			await ctx.send("Now playing "+ str(music2))
		else:
			await ctx.send(str(music2))
		curr += 1	
		counter += 1
		if q_counter > 0:
			q_counter -= 1
			if q_counter == 0:
				n_toggle = 0
			else:
				pass
		else:	
			pass
		if curr > (len(queued)-1):	
			curr = 0
		else:
			pass	
	else:
		await asyncio.sleep(.1)

@client.command(aliases = ['s'])
async def shuffle(ctx):
	global queued
	global music
	global curr
	global counter

	counter = 0
	queue = []
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	curr = 0

	try:
		queued.clear()
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
			queue.append(b)
		else:
			pass

	random.shuffle(queue)

	for x in queue:
		queued[x] = queue.index(x)

	try:	
		client.add_command(back)
		client.add_command(skip)
		client.add_command(add)
		client.add_command(nxt)
	except:
		pass	

	shuffling.start(ctx)

@tasks.loop(count=None)
async def shuffling(ctx):
	global curr
	global counter
	global music
	global q_counter
	global n_toggle

	if ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
		queue = list(queued)
		if curr < 0:
			curr = (len(queue)-abs(curr))
		else:
			pass
		music = queue[curr]
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
		music2 = music.replace(".mp3", "")
		if counter == 0:
			await ctx.send("Now playing "+ str(music2))
		else:
			await ctx.send(str(music2))
		curr += 1	
		counter += 1
		if q_counter > 0:
			q_counter -= 1
			if q_counter == 0:
				n_toggle = 0
			else:
				pass
		else:	
			pass	
		if curr > (len(queued)-1):	
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
	global queued
	global update
	global q_counter
	global n_toggle
	song_list = []
	dup_list = []

	if q_counter == 0:
		n_toggle = 1
		await ctx.invoke(nxt, song_name)
	else:				
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
					nxt_s = dup_list[num]+".mp3"
					update = queued
					og = update[nxt_s]
					if curr != og:
						if curr < og:
							update[nxt_s] = curr + q_counter	
							for kur in update:
								if (curr+q_counter) <= update[kur] < og and kur != nxt_s:
									update[kur] = update[kur]+1
								else:
									pass
						elif curr > og: 
							update[nxt_s] = (curr-1) + q_counter
							for kur in update:
								if og < update[kur] < (curr+q_counter) and kur != nxt_s:
									update[kur] = update[kur]-1
								else:
									pass
							curr -= 1
						q_counter += 1									
						await asyncio.sleep(.1)	
						queue = sorted(update.items(), key=lambda x:x[1])
						queued = dict(queue)
					else:
						q_counter += 1	
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
			nxt_s = dup_list[0]+".mp3"
			update = queued
			og = update[nxt_s]
			if curr != og:
				if curr < og:
					update[nxt_s] = curr + q_counter
					for kur in update:
						if (curr+q_counter) <= update[kur] < og and kur != nxt_s:
							update[kur] = update[kur]+1
						else:
							pass
				elif curr > og:
					update[nxt_s] = (curr-1) + q_counter
					for kur in update:
						if og < update[kur] < (curr+q_counter) and kur != nxt_s:
							update[kur] = update[kur]-1
						else:
							pass
					curr -= 1
				q_counter += 1									
				await asyncio.sleep(.1)	
				queue = sorted(update.items(), key=lambda x:x[1])
				queued = dict(queue)		
			else:
				q_counter += 1					
		else:
			await ctx.send("Sorry I couldn't find that song")

@client.command(aliases = ['n'])
async def nxt(ctx, song_name):
	global music
	global curr
	global queued
	global update
	global q_counter
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
				nxt_s = dup_list[num]+".mp3"
				update = queued
				og = update[nxt_s]
				if curr != og:
					if curr < og:
						update[nxt_s] = curr	
						for kur in update:
							if curr <= update[kur] < og and kur != nxt_s:
								update[kur] = update[kur]+1
							else:
								pass
					elif curr > og: 
						update[nxt_s] = curr -1
						for kur in update:
							if og < update[kur] < curr and kur != nxt_s:
								update[kur] = update[kur]-1
							else:
								pass
						curr -= 1
					if q_counter != 1:
						q_counter += 1
					else:
						pass										
					await asyncio.sleep(.1)	
					queue = sorted(update.items(), key=lambda x:x[1])
					queued = dict(queue)
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
		nxt_s = dup_list[0]+".mp3"
		update = queued
		og = update[nxt_s]
		if curr != og:	
			if curr < og:
				update[nxt_s] = curr	
				for kur in update:
					if curr <= update[kur] < og and kur != nxt_s:
						update[kur] = update[kur]+1
					else:
						pass
			elif curr > og:
				update[nxt_s] = curr - 1
				for kur in update:
					if og < update[kur] < curr and kur != nxt_s:
						update[kur] = update[kur]-1
					else:
						pass
				curr -= 1
			if n_toggle == 1:
				q_counter += 1
			else:
				pass											
			await asyncio.sleep(.1)	
			queue = sorted(update.items(), key=lambda x:x[1])
			queued = dict(queue)		
		else:
			pass					
	else:
		await ctx.send("Sorry I couldn't find that song")

@client.command(aliases = ['q'])
async def queue(ctx):
	if ctx.message.author.voice != None:
		if ctx.voice_client.is_playing() is True or ctx.voice_client.is_paused() == True:
			queue = list(queued)
			await ctx.send("Up Next Are: ")
			for x in range(8):
				q = curr + x
				if q >= len(queue):
					q -= len(queue)
				await ctx.send(f"{str(q+1)}. {queue[q].replace('.mp3', '')}")
		else:
			await ctx.send("There is nothing playing")		
	else:
		await ctx.send("You are not in the channel")	

@client.command(aliases = ['se'])
async def search(ctx, query):
	inquiry = query
	songs = []
	for y in range(dirlen):
		song = str(hub[y])
		if song.endswith(".mp3"):
			audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{song}")
			z = song.replace("mp3", "")
			artist = audio.artist if audio.artist is not None else " "
			album = audio.album if audio.album is not None else " "
			songs.append([z, artist, album])
		else:
			continue	
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.append(["Songs", "Artists", "Albums"])
	if inquiry.lower() == "songs" or inquiry.lower() == "song":
		for x in songs:
			ws.append([x[0], x[1], x[2]])
	elif inquiry.lower() == "artists" or inquiry.lower() == "artist":
		songs.sort(key= lambda x: x[1])
		for x in songs:
			ws.append([x[0], x[1], x[2]])
	elif inquiry.lower() == "albums" or inquiry.lower() == "album":
		songs.sort(key= lambda x: x[2])
		for x in songs:
			ws.append([x[0], x[1], x[2]])
	wb.save(f"{inquiry}.xlsx")
	await ctx.send("Ayo! Here's the list of songs:\n",file=discord.File(f"{inquiry}.xlsx"))
	os.remove(f"{inquiry}.xlsx")

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
	client.remove_command(nxt)

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

@client.command(alias = ['t'])
async def toggle(ctx, mode):
	global tog
	global queued
	global curr
	global counter
	queue = []

	if ctx.voice_client.is_playing() is True or ctx.voice_client.is_paused() is True:
		for b in hub:
			if b.endswith(".mp3"):
				queue.append(b)
			else:
				pass
		counter = 1
		try:	
			client.add_command(back)
			client.add_command(skip)
			client.add_command(add)
			client.add_command(nxt)
		except:
			pass	

		if mode.lower() == "neutral" or mode.lower() == "n":
			try:
				shuffling.cancel()
				ordering.cancel()
			except:
				pass
			try: 	
				client.remove_command(back)
				client.remove_command(skip)
				client.remove_command(add)
				client.remove_command(nxt)	
			except:
				pass
			try:
				queued.clear()
			except:
				pass	
		elif mode.lower() == "order" or mode.lower() == "o":
			shuffling.cancel()
			try:
				queued.clear()
			except:
				pass
			for x in queue:
				queued[x] = queue.index(x)
			curr = queued[music]+1
			ordering.start(ctx)
		elif mode.lower() == "shuffle" or mode.lower() == "s":
			ordering.cancel()
			try:
				queued.clear()
			except:
				pass
			curr = 1
			random.shuffle(queue)
			queue.insert(0, queue.pop(queue.index(music)))
			for x in queue:
				queued[x] = queue.index(x)
			shuffling.start(ctx)
		else:
			await ctx.send("That is not a correct mode input")
	else:
		await ctx.send("There's nothing playing")

@client.command()
async def test(ctx):
	embedVar = discord.Embed()
	for x in range(50):
		song = str(hub[x])
		if song.endswith(".mp3"):
			embedVar.add_field(name="Song", value=song, inline=True)
			embedVar.add_field(name="Artist", value="Test Artist", inline=True)
			embedVar.add_field(name="Album", value="Test Album", inline=True)
			# embedVar.add_field(name=".", value=song, inline=True)
			# embedVar.add_field(name="\u200b", value="Test Artist", inline=True)
			# embedVar.add_field(name="\u200b", value="Test Album", inline=True)	
		else:
			continue

	await ctx.send(embed=embedVar)


client.run(numbers())


