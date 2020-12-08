import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from discord.message import Attachment
import requests
import json
import datetime
from TOKEN import *

#collection of months and corresponding book // 
# should start blank and be added to as books are chosen through commands
bookCollection = {
    "January": "15 Dogs",
    "February": "feb",
    "March": "mar",
    "April": "apr",
    "May": "may",
    "June": "june",
    "July": "july",
    "August": "aug",
    "September": "sept",
    "October": "oct",
    "November": "nov",
    "December": "death on the nile"
}

#command prefix and bot object
bot = Bot(command_prefix='!')

#intializes currentDate variable and update it when performing date based loops to ensure right time
#need to break date setting into own method soon -- very WET
currentDate = datetime.datetime.now()
#sets current month to string using currentDate and dateobject.strftime
currentMonth = currentDate.strftime("%B")
#sets a book of the month for ease of use
bookOfTheMonth = bookCollection[currentMonth]


#need to put api call in method so i can call when book is changed for the month
#should probably make this a try / e so i cant break bot with bad GET
response = requests.get(f"https://v1.nocodeapi.com/colourised/gr/ylbRWcheecMozbsx/search?q={bookOfTheMonth}").json()
if response != False:
    print("BOOK GET SUCCESFUL!")


#general channel id -- must have -- book club only has one channel so dont need to edit this rn
#if expanded to work for others would need to have a different solution to finding channel id
CHANNEL_ID = 784457938551046167

# this event makes sure bot is ready and will output when it is
@bot.event
async def on_ready():
    print('Booker started reading!')
    await bot.change_presence(activity= discord.Activity(type = discord.ActivityType.listening, name = bookCollection[currentMonth]))

#provides title and author of current months book
@bot.command()
async def bookinfo(ctx):
    await ctx.send(f"{response['results'][0]['title']} by {response['results'][0]['author']['name']}")
    await ctx.send(response['results'][0]['image_url'])

#command to addbook to a selected month
@bot.command()
async def addbook(ctx, month, book):
    month = month.capitalize()
    bookCollection[month] = book
    await ctx.send(f"{book} has been chosen for the month of {month}")

#for the boys
@bot.command()
async def xanman(ctx):
    await ctx.send("I FUCK BITCHES AND IM MLG PRO YEET!!!!")

#once i add !finished then i can @ only the people who arent done their books -- less channel spam
@tasks.loop(hours=24)
async def weekly_announcment():
    messageChannel = bot.get_channel(CHANNEL_ID)
    #need to update bookOfTheMonth before sending this message!
    if currentDate.day == 1:
        await messageChannel.send(f"@everyone It is {currentMonth}! Time for a new book! This month you're reading {bookCollection[currentMonth]}")
    #reminder halfway through month
    if currentDate.day == 15:
        await messageChannel.send(f"@everyone We are halfway through the month! Are you halfway through {bookCollection[currentMonth]}?")
    #send discussion questions? actual check of last day // currently assuming all months 30 days
    if currentDate.day == 30:
        await messageChannel.send(f"@everyone The month is over hope you're done {bookCollection[currentMonth]}!")

@weekly_announcment.before_loop
async def before():
    await bot.wait_until_ready()
    currentDate = datetime.datetime.now()
    print(f"updated datetime to {currentDate}")

#need the start method on loops or they dont run
weekly_announcment.start()

#must end with bot.run
bot.run(TOKEN)