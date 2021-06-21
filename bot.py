import discord
import os
import sys
import io
from discord.ext import commands, tasks
from itertools import cycle 
from keep_alive import keep_alive
from discord.ext.commands import CommandNotFound
import discord.ext.commands
import nacl
import asyncio
import time
import tracemalloc
import json

tracemalloc.start()
client = commands.Bot(command_prefix = ".")
member = discord.Client()
hub = os.listdir("C:/Users/LucaN/Downloads/music")
dirlen = len(hub)
msg = None
music = None		

def numbers():
	f = open("C:/Users/LucaN/OneDrive/Desktop/Discord Music Bot/config.json", "r")
	data = json.load(f)
	mason = data["token"]
	f.close()
	return mason
	

@client.event
async def on_ready():
	print("bot is ready")

@client.command()
async def shutdown(ctx):
	try:
		client.remove_command(repeat)
		repeater.cancel()
		await ctx.voice_client.disconnect()	
	except:
		pass

		
	sys.exit()	

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
		return msg
	else:
		pass    

# @client.listen("on_message")
# async def on_message(message):
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
		

@commands.command()
async def forward(ctx):
	repeater.stop()
	client.remove_command(forward)	
	

@commands.command()
async def repeat(ctx):
	repeater.start(ctx)
	client.add_command(forward)

@tasks.loop(count=None)
async def repeater(ctx):
	if ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused() is False:
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{music}"))


@commands.command()
async def skip(ctx):
	print(True)


@commands.command()
async def back(ctx):
	print(True)


@client.command()
async def cmds(ctx):
	await ctx.send("Here's the list of commands")
	for cmd in client.commands:
		await ctx.send(str(cmd)+"\n")

@client.command()
async def order(ctx):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	value = 0
	x = 1
	song_list_ordered = []

	try:
		value = ctx.voice_client.is_playing()
		if value == True:
			ctx.voice_client.stop()
	except:
		pass

	for b in hub:
		if b.endswith(".mp3"):
			song_list_ordered.append(b)
		else:
			pass		

	if ctx.message.author.voice != None:
		if ctx.voice_client is None:
			await voiceChannel.connect()

		try:
			client.add_command(repeat)
		except:
			pass

	while x < (len(song_list_ordered)-1): 
		if ctx.voice_client.is_playing() == False and ctx.voice_client.is_paused() == False:
			print(True)
			try:
				ctx.voice_client.stop()
			except:
				pass	
			global music
			music = song_list_ordered[x]	
			ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{song_list_ordered[x]}"))
			await ctx.send("Now playing "+ str(song_list_ordered[x]))
			x += 1
			y = x - 1
			z = x + 1

		else:
			print(False)	

		if x > 0:
			try:
				client.add_command(back)
			except:
				pass
		else:
			try:
				client.remove_command(back)
			except:
				pass

		if x < (len(song_list_ordered) - 1):
			try:
				client.add_command(skip)
			except:
				pass
		else:
			try:
				client.remove_command(skip)
			except:
				pass		
	else:
		await ctx.send("You are not in the channel")

	# while x < (len(song_list_ordered)-1):
	# 	if x > 0:
	# 		try:
	# 			client.add_command(back)
	# 		except:
	# 			pass
	# 	else:
	# 		try:
	# 			client.remove_command(back)
	# 		except:
	# 			pass
	# 	if x < (len(song_list_ordered) - 1):
	# 		try:
	# 			client.add_command(skip)
	# 		except:
	# 			pass
	# 	else:
	# 		try:
	# 			client.remove_command(skip)
	# 		except:
	# 			pass
	# 	if ctx.voice_client.is_playing() is False and ctx.voice_client.is_paused is False:				
	# 		global music
	# 		music = song_list_ordered[x]
	# 		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"C:/Users/LucaN/Downloads/music/{song_list_ordered[x]}"))
	# 		await ctx.send("Now playing "+ str(song_list_ordered[x]))
	# 		x+=1
	# 	else:
	# 		continue				


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

@client.command()
async def play(ctx, song_name):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	value = None
	global music
	music = song_name
	song_list = []
	dup_list = []

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

	count = 0
	songs = []
	if song_name.endswith(".mp3"):
		song_name = song_name.replace(".mp3", "")
	word1 = "".join(val for val in song_name if val.isalnum() or val == "." or val == "!" or val == "'" or val == " ")	
	song = word1.lower().split()
	for i in song:
		whitesong = "".join((" ",i," "))
		songs.append(whitesong)
	for b in hub:
		if b.endswith(".mp3"):
			b = b.replace(".mp3","")
			song_list.append(b)			

	for x in song_list:
		songs_list = set()						
		word = "".join(val for val in x if val.isalnum() or val == "." or val == "!" or val == "'" or val == " ")
		v = word.lower().split()
		for j in v:
			songsong = "".join((" ",j," "))
			songs_list.add(songsong)	
		for y in songs:
			for c in songs_list:
				if y in c:
					count+=1
					continue
				else:
					count+=0
					continue

		if count == len(song):
			dup_list.append(x)
			count = 0
		else:
			count = 0
	if len(dup_list) > 1 and len(dup_list) < 76:
		num = 0
		while num in range(len(dup_list)):
			if len(dup_list[num].split()) == len(song):
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

		if num > (len(dup_list)-1):
			await ctx.send("Here are a couple of songs that share a similar name. Can you specify which one?")
			for z in dup_list:
				await ctx.send(str(z))

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
async def stop(ctx):
	if ctx.message.author.voice != None:
		try:
			client.remove_command(repeat)
			repeater.cancel()
		except:
			pass
		try:	
			await ctx.voice_client.stop()
		except:
			pass		
	else:
		await ctx.send("There is nothing playing")

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

@client.command()
async def pause(ctx):
	if ctx.message.author.voice != None:
		try:
			if ctx.voice_client.is_paused() == False:
				ctx.voice_client.pause()
			else:
				await ctx.send("The song is already paused")	
		except:
			await ctx.send("There is nothing playing")
	else:
		await ctx.send("You are not in the channel")			

@client.command()
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


@client.command()
async def test(ctx):
	# print(ctx.voice_client)
	ctx.voice_client.stop()
	# print(None)
	# voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	# vc = ctx.voice_client
	# if vc.is_paused() == True:
	# 	print(True)
	# 	time.sleep(5)
	# else:
	# 	print(False)
	# 	time.sleep(5)

# @client.command()
# async def test3(ctx):
			 			
	# if ctx.voice_client.is_paused() == True:
	# 	print(True)  
	# else:
	# 	print(False)

@client.command()
async def test2(ctx):
	for x in hub:
		if "flyers" and "bradio" in "BRADIO-FlyersTVアニメデスパレードOP曲(OFFICIAL VIDEO).mp3".lower():
			print(True)

@client.command()
async def play2(ctx, song_name):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	value = None
	global music
	music = song_name
	song_list = []
	dup_list = []

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
	# print(len(song))
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

	# print(dup_list, len(dup_list))
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

client.run(numbers())
keep_alive()


