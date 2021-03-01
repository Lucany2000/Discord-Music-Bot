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
# import

tracemalloc.start()
client = commands.Bot(command_prefix = ".")
member = discord.Client()
hub = os.listdir("C:/Users/LucaN/Downloads/music")
dirlen = len(hub)
msg = None
music = None

@client.event
async def on_ready():
	print("bot is ready")

@client.command()
async def shutdown(ctx):
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
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"music/{music}"))


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
	try:
		value = ctx.voice_client.is_playing()
		if value == True:
			ctx.voice_client.stop()
	except:
		pass
	if ctx.voice_client is None:
		await voiceChannel.connect()	
	ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"music/{str(hub[0])}"))		


@client.command()
async def songs(ctx):
	f = open("songs.txt", "w", encoding='utf8')
	x = 0
	while x < (dirlen - 1):
		song = str(hub[x])
		if song.endswith(".jpg"):
			x+=1
		else:
			z = ''.join(('"',song,'"'))
			f.write(z+"\n")
			x+=1
	f.close()		
	with open("songs.txt", "rb") as file:
		await ctx.send("Ayo! Here's the list of songs:", file=discord.File(file, "songs.txt"))
	f.close()
		# os.remove("songs.txt")

@client.command()
async def play(ctx, song_name):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	value = None
	global music
	music = song_name
	try:
		value = ctx.voice_client.is_playing()
		if value == True:
			ctx.voice_client.stop()
	except:
		pass		
	x = 0
	while x < (dirlen - 1):
		song = str(hub[x])
		if song == song_name:
			if ctx.message.author.voice != None:
				if ctx.voice_client is None:
					vc = await voiceChannel.connect()			
				vc = ctx.voice_client		
				vc.play(discord.FFmpegPCMAudio(executable="C:/Users/LucaN/FFmpeg/ffmpeg/bin/ffmpeg.exe", source=f"music/{song_name}"))
				await ctx.send("Now playing "+ str(song_name))
				try:
					client.add_command(repeat)
				except:
					pass	
			else:
				await ctx.send("You are not in the channel")
				break
		else:
			x+=1
	if x == (dirlen - 1):
		await ctx.send("Sorry I couldn't find that song")				
			
@client.command()
async def stop(ctx):
	if ctx.message.author.voice != None:
		try:
			client.remove_command(repeat)
			repeater.cancel()
		except:
			pass
		await ctx.voice_client.disconnect()	
	else:
		await ctx.send("There is nothing playing")	

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
	repeater.cancel()
	# print(None)
	# voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	# vc = ctx.voice_client
	# if vc.is_paused() == True:
	# 	print(True)
	# 	time.sleep(5)
	# else:
	# 	print(False)
	# 	time.sleep(5)

def test4():
	print("Hello")

@client.command()
async def test3(ctx):
	print(None)
	test4()
	# if ctx.voice_client.is_paused() == True:
	# 	print(True)
	# else:
	# 	print(False)


@client.command()
async def test2(ctx):
	print("test")
	# await test2.invoke(ctx)

	# print(ctx.author.public_flags.all())
	# voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	# await ctx.invoke(client.get_command("test"))
	# print(cmd_msg(message))
	# client.add_command(test3)
	# await test3.invoke(ctx)
	# test3(ctx = discord.ext.commands.Context)



client.run("NzY3ODAwNjc0MjUxMDQ2OTU0.X43MGQ.y9BKD0kVnQZkaBl79Q9t61wxpd4")
keep_alive()