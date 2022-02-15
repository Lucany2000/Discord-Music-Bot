# from ast import alias
# from asyncore import read
# from glob import glob
# from pydoc import describe
# from turtle import title
# from xml.etree.ElementInclude import include
import discord
import os
import sys
import io
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
import discord.ext.commands
import nacl
import asyncio
import json
import random
import openpyxl
from tinytag import TinyTag

hub = []
client = commands.Bot(command_prefix = ".", help_command=None)
member = discord.Client()
base = os.listdir("C:/Users/LucaN/Downloads/music")
for og in base:
	if og.endswith(".mp3"):
		hub.append(og)
full = hub
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
pos = None
pos2 = None
song_name = None
playback = None
now = 0

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
		tracker.start(ctx)

@client.command(aliases = ['h'])
async def help(ctx):
	await ctx.send("Here's the list of commands")
	embed = discord.Embed(title="Manual", description="A list of commands, their aliases, uses, inputs, and conditions")
	embed.add_field(name="Help", value="Alias = 'h'\nUse: Menu containing descriptions about other Commands")
	embed.add_field(name="Play", value="Alias = 'p'\nUse: play music given input of song name, cancels audio based commands")
	embed.add_field(name="Order", value="Alias = 'o'\nUse: plays music in alphabetical order, loops around once it hits the end")
	embed.add_field(name="Shuffle", value="Alias = 's'\nUse: plays music in shuffled order, loops around once it hits the end")
	embed.add_field(name="Pause", value="Alias = '||'\nUse: pauses music")
	embed.add_field(name="Stop", value="Alias = 'st'\nUse: stops music")
	embed.add_field(name="Resume", value="Alias = 'r'\nUse: resumes music")
	embed.add_field(name="Leave", value="Alias = 'l'\nUse: forces bot to leave voice chat")
	embed.add_field(name="Skip", value="Alias = '>'\nUse: skips current song, can only be used while in: playlist, order, shuffle, toggle, will loop back to first if on last song")
	embed.add_field(name="Back", value="Alias = '<'\nUse: goes back from current song, can only be used while in: playlist, order, shuffle, toggle, will loop back to last if on first song")
	embed.add_field(name="Add", value="Alias = 'a'\nUse: adds song to a queue, can only be used while in: playlist, order, shuffle, toggle")
	embed.add_field(name="Nxt", value="Alias = 'n'\nUse: adds song to be played next, can only be used while in: playlist, order, shuffle, toggle")
	embed.add_field(name="Queue", value="Alias = 'q'\nUse: shows the next 8 songs that will play next, can only be used while in: playlist, order, shuffle, toggle")
	embed.add_field(name="Search", value="Alias = 'se'\nUse: gives full list of songs with corresponding artists and albums in a table format")
	embed.add_field(name="Repeat", value="Alias = 're'\nUse: repeats current song, mainly canceled out by the 'forward' command")
	embed.add_field(name="Forward", value="Alias = 'f'\nUse: cancels out 'repeat' command")
	embed.add_field(name="Toggle", value="Alias = 't'\nInput = 'neutral'/alias = 'n': nothing changes, cancels out other options\nInput = 'order'/alias = 'o': invokes 'order' command from current song's postion\nInput = 'shuffle'/alias = 's': invokes 'shuffle' using current song as first song")
	embed.add_field(name="Playlist", value="Alias = 'pl'\nUse: creates a playlist based off artist or album inputted, all audio commands besides 'play' will act as if the songs in the playlist are the only songs available, can be turned off if 'all' is inputed")
	await ctx.send(embed=embed)

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
		tracker.start(ctx)
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
		tracker.start(ctx)
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
	global now
	if ctx.voice_client.is_playing() is True or ctx.voice_client.is_paused() is True:
		tracker.cancel()
		now = 0
		ctx.voice_client.stop()
	else:
		await ctx.send("Nothing is playing right now")	

@commands.command(aliases = ['<'])
async def back(ctx):
	global curr
	global now
	if ctx.voice_client.is_playing() is True or ctx.voice_client.is_paused() is True:
		tracker.cancel()
		ctx.voice_client.stop()
		if playback is True:	
			curr -= 1
			now = 0
		else:
			curr -= 2
			now = 0		
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

	global pos
	global pos2

	pos = None
	pos2 = None

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
			audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{x}.mp3")
			z = x
			x = x.lower()
			for y in song:
				if y in x:
					pos = x.find(y)
					if pos2 == None:
						pos2 = pos
					else:
						if pos2 <= pos:
							pos2 = pos
							pass
						else:
							continue
					count+=1
					x = x.replace(y, "", 1)
					continue	
				else:
					count+=0
				if y in (audio.artist.lower() if audio.artist is not None else " "):
					pos = x.find(y)
					if pos2 == None:
						pos2 = pos
					else:
						if pos2 <= pos:
							pos2 = pos
							pass
						else:
							continue
					count+=1
					x = x.replace(y, "", 1)
					continue	
				else:
					count+=0
				if y in (audio.album.lower() if audio.album is not None else " "):
					pos = x.find(y)
					if pos2 == None:
						pos2 = pos
					else:
						if pos2 <= pos:
							pos2 = pos
							pass
						else:
							continue
					count+=1
					x = x.replace(y, "", 1)
					continue	
				else:
					count+=0
		pos = None
		pos2 = None

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
	global pos
	global pos2

	pos = None
	pos2 = None
				
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
		audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{x}.mp3")
		z = x
		x = x.lower()
		for y in song:
			if y in x:
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
			if y in (audio.artist.lower() if audio.artist is not None else " "):
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
			if y in (audio.album.lower() if audio.album is not None else " "):
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
		pos = None
		pos2 = None

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
			if ordering.is_running() is True or shuffling.is_running() is True:
				queue = list(queued)
				await ctx.send("Up Next Are: ")
				for x in range(8):
					q = curr + x
					if q >= len(queue):
						q -= len(queue)
					await ctx.send(f"{str(q+1)}. {queue[q].replace('.mp3', '')}")
			else:
				await ctx.send("No queue list detected")		
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

@client.command(aliases = ['p'])
async def play(ctx, song_name):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	global music
	music = song_name
	song_list = []
	dup_list = []
	global pos
	global pos2
	global hub

	pos = None
	pos2 = None

	hub = full

	try:
		shuffling.cancel()
		ordering.cancel()
		client.remove_command(skip)
		client.remove_command(back)
		client.remove_command(add)
		client.remove_command(nxt)
	except:
		pass		

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
		audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{x}.mp3")
		z = x
		x = x.lower()
		for y in song:
			if y in x:
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
			if y in (audio.artist.lower() if audio.artist is not None else " "):
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
			if y in (audio.album.lower() if audio.album is not None else " "):
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
		pos = None
		pos2 = None		

		if count == len(song):
			dup_list.append(z)
			count = 0
		else:
			count = 0

	if len(dup_list) == 1:
		try:
			if ctx.voice_client.is_playing() == True:
				ctx.voice_client.stop()
		except:
			pass		
		music = dup_list[0]+".mp3"
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
		tracker.start(ctx)
		await ctx.send("Now playing "+ str((dup_list[0])))
		try:
			client.add_command(repeat)
		except:
			pass

	elif len(dup_list) > 1:
		num = 0
		while num < (len(dup_list)):
			if len(dup_list[num]) == len(song_name):
				try:
					if ctx.voice_client.is_playing() == True:
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
			await ctx.send("Here are a couple of songs that share a similar name/similar artist/similar album. Can you specify which one?")
			# await ctx.send(f"**```\n{song_name}\n```**\n{str(list(l for l in dup_list))}\n")
			# embedVar = discord.Embed()
			for l in dup_list:
				await ctx.send(str(l))
			# embedVar.add_field(name=f"{song_name}", value=list(l for l in dup_list))
			# await ctx.send("```**")	

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

@client.command(aliases = ['||'])
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

@client.command(alias = ['pl'])
async def playlist(ctx, tgle, metadata):
	meta = metadata
	t = tgle
	song_list = []
	dup_list = []
	global pos
	global pos2
	global hub

	pos = None
	pos2 = None

	if t.lower() != "all" or t.lower() != 'a':
		try:
			shuffling.stop()
			ordering.stop()
			client.remove_command(skip)
			client.remove_command(back)
			client.remove_command(add)
			client.remove_command(nxt)
		except:
			pass
					
		word2 = [char for char in meta]
		try:
			if len(word2) <= 0 or str(word2[0]) == " ":
				await ctx.send("Sorry I couldn't find that Artist/Album")
			else:
				pass
		except IndexError:
			pass				

		if meta.endswith(".mp3"):
			await ctx.send("This is not an Artist/Album")	
		meta = meta.lower().split()
		for b in hub:
			if b.endswith(".mp3"):
				b = b.replace(".mp3", "")
				song_list.append(b)			

		count = 0
		for x in song_list:
			audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{x}.mp3")
			for y in meta:
				if y in (audio.artist.lower() if audio.artist is not None else " "):
					pos = x.find(y)
					if pos2 == None:
						pos2 = pos
					else:
						if pos2 <= pos:
							pos2 = pos
							pass
						else:
							continue
					count+=1
					x = x.replace(y, "", 1)
					continue	
				else:
					count+=0
				if y in (audio.album.lower() if audio.album is not None else " "):
					pos = x.find(y)
					if pos2 == None:
						pos2 = pos
					else:
						if pos2 <= pos:
							pos2 = pos
							pass
						else:
							continue
					count+=1
					x = x.replace(y, "", 1)
					continue	
				else:
					count+=0
			pos = None
			pos2 = None			

			if count == len(meta):
				if t.lower() == "artist":
					dup_list.append(audio.artist)
					count = 0
				elif t.lower() == "album":
					dup_list.append(audio.album)
					count = 0
			else:
				count = 0

		if len(dup_list) == 1:
			if dup_list[0] != " " or dup_list[0] != None:
				hub.clear()
				for z in full:
					audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{z}")
					if t.lower() == "artist":
						if audio.artist == dup_list[0]:
							hub.append(z)
					elif t.lower() == "album":
						if audio.album == dup_list[0]:
							hub.append(z)
					await ctx.send(f"You're now in playlist {dup_list[0]}")		
			else:
				await ctx.send("Sorry I couldn't find that Artist/Album")						

		elif len(dup_list) > 1:
			num = 0
			while num < (len(dup_list)):
				if len(dup_list[num]) == len(meta):
					if dup_list[num] != " " or dup_list[num] != None:
						hub.clear()
						for z in full:
							audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{z}")
							if t.lower() == "artist":
								if audio.artist == dup_list[num]:
									hub.append(z)
							elif t.lower() == "album":
								if audio.album == dup_list[num]:
									hub.append(z)
							await ctx.send(f"You're now in playlist {dup_list[num]}")		
						else:
							await  ctx.send("Sorry I couldn't find that Artist/Album")				
				else:
					num+=1

			if num == (len(dup_list)):
				await ctx.send("Here are a couple of artists/albums that share a similar name. Can you specify which one?")
				# await ctx.send(f"**```\n{song_name}\n```**\n{str(list(l for l in dup_list))}\n")
				# embedVar = discord.Embed()
				for l in dup_list:
					await ctx.send(str(l))
				# embedVar.add_field(name=f"{song_name}", value=list(l for l in dup_list))
				# await ctx.send("```**")	

		else:
			await ctx.send("Sorry I couldn't find that Artist/Album")
	else:
		hub = full
		await ctx.send("You've exited the playlist")


@client.command(aliases=['*'])
async def test(ctx, song_name):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	global music
	music = song_name
	song_list = []
	dup_list = []
	global pos
	global pos2

	pos = None
	pos2 = None

	try:
		shuffling.cancel()
		ordering.cancel()
		client.remove_command(skip)
		client.remove_command(back)
		client.remove_command(add)
		client.remove_command(nxt)
	except:
		pass

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
		audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{x}.mp3")
		z = x
		x = x.lower()
		for y in song:
			if y in x:
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
			if y in (audio.artist.lower() if audio.artist is not None else " "):
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
			if y in (audio.album.lower() if audio.album is not None else " "):
				pos = x.find(y)
				if pos2 == None:
					pos2 = pos
				else:
					if pos2 <= pos:
						pos2 = pos
						pass
					else:
						continue
				count+=1
				x = x.replace(y, "", 1)
				continue	
			else:
				count+=0
		pos = None
		pos2 = None			

		if count == len(song):
			dup_list.append(z)
			count = 0
		else:
			count = 0

	if len(dup_list) == 1:
		try:
			if ctx.voice_client.is_playing() == True:
				ctx.voice_client.stop()
		except:
			pass		
		music = dup_list[0]+".mp3"
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
		tracker.start(ctx)
		await ctx.send("Now playing "+ str((dup_list[0])))
		try:
			client.add_command(repeat)
		except:
			pass

	elif len(dup_list) > 1:
		num = 0
		while num < (len(dup_list)):
			if len(dup_list[num]) == len(song_name):
				try:
					if ctx.voice_client.is_playing() == True:
						ctx.voice_client.stop()
				except:
					pass		
				music = dup_list[num]+".mp3"
				ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))
				tracker.start(ctx)
				await ctx.send("Now playing "+ str((dup_list[num])))
				try:
					client.add_command(repeat)
				except:
					pass
				break
			else:
				num+=1

		if num == (len(dup_list)):
			await ctx.send("Here are a couple of songs that share a similar name/similar artist/similar album. Can you specify which one?")
			# await ctx.send(f"**```\n{song_name}\n```**\n{str(list(l for l in dup_list))}\n")
			# embedVar = discord.Embed()
			for l in dup_list:
				await ctx.send(str(l))
			# embedVar.add_field(name=f"{song_name}", value=list(l for l in dup_list))
			# await ctx.send("```**")	

	else:
		await ctx.send("Sorry I couldn't find that song")

# @tasks.loop(count=None)
# async def tracker(ctx):
# 	global playback
# 	audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{music}")
# 	then = round(audio.duration)
# 	now = None

# 	if ctx.voice_client.is_playing() is True:
# 		now = timer()
# 		print((round(now)))
# 		if now is not None and (round(now)-5) >= then/2:
# 			playback = True
# 		else:
# 			playback = False
# 		print(playback)	
# 	elif ctx.voice_client.is_paused() is True:
# 		print("sleep")
# 		await asyncio.sleep(.1)	
# 	elif ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
# 		playback = False
# 		tracker.cancel()

@tasks.loop(count=None)
async def tracker(ctx):
	global playback
	global now
	audio = TinyTag.get(f"C:/Users/LucaN/Downloads/music/{music}")
	dur = round(audio.duration)
	
	if ctx.voice_client.is_playing() is True:
		now += 1
		await asyncio.sleep(1)	
	elif ctx.voice_client.is_paused() is True:
		await asyncio.sleep(.1)	
	elif ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
		now = 0
		playback = False
		tracker.cancel()

	if now >= dur/2:
		playback = True
	else:
		playback = False
	print(playback)			

client.run(numbers())


