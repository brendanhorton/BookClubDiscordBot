import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import datetime
from TOKEN import *

#command prefix 
bot = Bot(command_prefix='!')

#intializes currentDate variable and update it when performing date based loops to ensure right time
currentDate = datetime.datetime.now()

#general channel id -- must have -- book club only has one channel so dont need to edit this rn
#if expanded to work for others would need to have a different solution to finding channel id
CHANNEL_ID = 784457938551046167

# this event makes sure bot is ready and will output when it is
#want to change bot so it displays the current months book // not sure how 
#maybe i need to use a datetime object and conditionals
#if month == x then output y as name of activity
#can have large hash with book for each month
#expansion would include allowing user to set books for each month per instance of bot
# doable
@bot.event
async def on_ready():
    print('bot running')
    await bot.change_presence(activity= discord.Activity(type = discord.ActivityType.listening, name = "Death on the Nile"))

#when someone types test bot returns testing 123
@bot.event
async def on_message(message):
    if message.content == '!currentbook':
        await message.channel.send('The book for the month of December is Death on the Nile')
    
    await bot.process_commands(message)

#simpel test command to learn discordloops
#runs every 10sec
#must have the before loop check to ready or it doesnt work
# @tasks.loop(seconds=10)
# async def testingLoop():
#     message_channel= bot.get_channel(CHANNEL_ID)
#     await message_channel.send("10 Second Bot Initiated")

# @testingLoop.before_loop
# async def before():
#     await bot.wait_until_ready()
#     print("Finished waiting")

#whiteboard this
#want this loop to run once a week, provide motivation and remind for reading 
#ask users -- are you x amount of length through your book?
#this will have to use dateobject aswell -- if day < 15 || day == 30
#are you halfway through book
#are you done the book
#need to breakup datetime object and then refresh it once a day maybe?
@tasks.loop(hours=24)
async def weekly_announcment():
    message_channel= bot.get_channel(CHANNEL_ID)
    # await message_channel.send("Are you reading your book? How are you enjoying it?")
    if currentDate.day == 15:
        await message_channel.send("Today is the 6th of December")
    else: 
        await message_channel.send("Today is not the date you entered in the thingy")

@weekly_announcment.before_loop
async def before():
    await bot.wait_until_ready()
    currentDate = datetime.datetime.now()
    print(f"updated datetime to {currentDate}")

# #need the start functions on loops or they dont run
# testingLoop.start()
weekly_announcment.start()

#must end with bot.run
bot.run(TOKEN)