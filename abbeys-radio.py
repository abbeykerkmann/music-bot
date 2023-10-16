import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command('help')

YDL_OPTIONS = {
    'format': 'bestaudio/best',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

videoQueue = []
currentVideo = ""
isPlaying = False
isPaused = False

ydl = youtube_dl.YoutubeDL(YDL_OPTIONS)

@bot.command()
async def boop(ctx):
    await ctx.send('boop!')

@bot.command()
async def help(ctx):
    help_message = """
    Here are the commands you can use:
    /join - Connects the bot to your voice channel.
    /play <url> - Plays the video from the provided YouTube URL.
    /add <url> - Adds the video from the provided YouTube URL to the queue.
    /queue - Shows the current video and the queue.
    /clear - Clears the queue.
    /skip - Skips the current video and plays the next one in the queue.
    /pause - Pauses the current video.
    /resume - Resumes the paused video.
    /stop - Stops the current video and clears the queue.
    /disconnect - Disconnects the bot from the voice channel.
    """
    await ctx.send(help_message)

@bot.command()
async def join(ctx):
    userChannel = ctx.message.author.voice.channel
    await userChannel.connect()
    await ctx.send("Connected to voice channel.")

@bot.command()
async def play(ctx, url):
    song = search(url)
    if type(song) == type(True):
        await ctx.send("Could not download the video. Please check the URL and try again.")
    else:
        videoQueue.append(song)
        await ctx.send("Video added to the queue.")
        if isPlaying == False:
            playNext(ctx)

@bot.command()
async def add(ctx, url):
    song = search(url)
    if type(song) == type(True):
        await ctx.send("Could not download the video. Please check the URL and try again.")
    else:
        videoQueue.append(song)
        await ctx.send("Video added to the queue.")

@bot.command()
async def queue(ctx):
    message = ""
    if currentVideo != "":
        message += "Current Video: {} \n".format(currentVideo)
    if len(videoQueue) > 0:
        index = 1
        message += "Up Next: \n"
        for video in videoQueue:
            message += "{}. {} \n".format(index, video['title'])
            index += 1
    else:
        message += "Nothing in the queue!"
    await ctx.send(message)

@bot.command()
async def disconnect(ctx):
    voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voiceClient:
        await voiceClient.disconnect()
        await ctx.send('Disconnected from the voice channel.')

@bot.command()
async def skip(ctx):
    voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voiceClient:
        await ctx.send("Skipping the current video.")
        voiceClient.stop()
        playNext(ctx)
    else:
        await ctx.send("Not currently playing anything!")

@bot.command()
async def pause(ctx):
    global isPlaying, isPaused
    voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if isPlaying:
        isPlaying = False
        isPaused = True
        voiceClient.pause()
    else:
        await ctx.send("Not currently playing anything!")

@bot.command()
async def resume(ctx):
    global isPlaying, isPaused
    voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if isPaused:
        isPlaying = True
        isPaused = False
        voiceClient.resume()
    else:
        await ctx.send("Video is not paused!")

@bot.command()
async def stop(ctx):
    global isPlaying, isPaused
    voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.send("Stopping all video playback.")
    voiceClient.stop()

@bot.command()
async def clear(ctx):
    global videoQueue
    await ctx.send("Clearing the video queue.")
    videoQueue.clear()

def search(url):
    info = ydl.extract_info(url, download=False)
    for index in range(len(info['formats'])):
        if 'format_note' in info['formats'][index] and info['formats'][index].get('format_note') == 'Default':
            return {'audio': info['formats'][index], 'title': info['title']}

def playNext(ctx):
    global isPlaying, currentVideo
    voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if len(videoQueue) > 0:
        isPlaying = True
        songInfo = videoQueue.pop(0)
        source = songInfo['audio']['url']
        currentVideo = songInfo['title']
        voiceClient.play(discord.FFmpegPCMAudio(source=source, executable='C:\\FFmpeg\\bin\\ffmpeg.exe', options=FFMPEG_OPTIONS), after=lambda e: playNext(ctx))
    else:
        currentVideo = ""
        isPlaying = False

bot.run('TOKEN')