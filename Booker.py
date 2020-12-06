import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import datetime

# TODO
# 1. seperate datetime object and begin using it for conditionals
# 2. send progress reminders to users to keep them on track -- simple extension of loops once i have datetime object broken
# 3. at end of month maybe i send a message and disscusion questions in order to stimulate conversation
# 4. eventually get books to autochange and rotate through selections as new month hits
# 4b) example: on 1st at 9am sends message >>> this month you are reading XYZ it is XYZ pages long, good luck have fun
# 4c) maybe api implementation here? book api to pull book title and length maybe a brief sysnopsis even -- this could be fun

#possible features?
#add commands for check ins
#add commands for finishing the book

current_Date = datetime.datetime.now()

#general channel id -- must have
CHANNEL_ID = 784457938551046167

#command prefix 
bot = Bot(command_prefix='!')
#my token
TOKEN = 'Nzg0NDU2MDA2NTQ0MzkyMjc1.X8pjlg.FJeoVY8nwmG4o6OZ1SEbRpJyd1U'

# this event makes sure bot is ready and will output when it is
#want to change bot so it displays the current months book // not sure how 
#maybe i need to use a datetime object and conditionals
#if month == x then output y as name of activity
#doable
@bot.event
async def on_ready():
    print('bot running')
    await bot.change_presence(activity= discord.Activity(type = discord.ActivityType.listening, name = "Death on the Nile"))

#when someone types test bot returns testing 123
@bot.event
async def on_message(message):
    if message.content == 'test':
        await message.channel.send('Testing 1 2 3')
    
    await bot.process_commands(message)

#simpel test command to learn discordloops
#runs every 10sec
#must have the before loop check to ready or it doesnt work
@tasks.loop(seconds=10)
async def testingLoop():
    message_channel= bot.get_channel(CHANNEL_ID)
    await message_channel.send("10 Second Bot Initiated")

@testingLoop.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

#whiteboard this
#want this loop to run once a week, provide motivation and remind for reading 
#ask users -- are you x amount of length through your book?
#this will have to use dateobject aswell -- if day < 15 || day == 30
#are you halfway through book
#are you done the book
#need to breakup datetime object and then refresh it once a day maybe?
@tasks.loop(hours=168)
async def weekly_announcment():
    message_channel= bot.get_channel(CHANNEL_ID)
    await message_channel.send("Are you reading your book? How are you enjoying it?")

@weekly_announcment.before_loop
async def before():
    await bot.wait_until_ready()
    print("Weekly Bot Initiated")

#prints date object
print(current_Date)

#need the start functions on loops or they dont run
testingLoop.start()
weekly_announcment.start()

#must end with bot.run
bot.run(TOKEN)