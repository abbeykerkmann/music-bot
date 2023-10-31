# Abbey's Radio (WIP)

## Overview
This project was created for me to experiment with creating my own music bot for Discord.
The bot was created using Python and leverages the Discord and YoutubeDL libraries

## How it works
Audio from youtube videos can be played using this bot by providing the URL of the video you want to play.
First, the bot must join the user's voice channel using the `/join` command, and then using the `/play <url>` command, you can play any youtube video you want! There are a variety of other commands that cover different functions as well.

### Currently Supported Commands
```
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
```
