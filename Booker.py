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

memberCollection = {}
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
#should put this into variables for readability probably
@bot.command()
async def currentbook(ctx):
    await ctx.send(f"{response['results'][0]['title']} by {response['results'][0]['author']['name']}")
    await ctx.send(response['results'][0]['image_url'])


@bot.command()
async def bookinfo(ctx, month):
    await ctx.send(f"{bookCollection[month]} is the book for the month of {month.capitalize()}")


#command to addbook to a selected month
@bot.command()
async def addbook(ctx, month, book):
    month = month.capitalize()
    bookCollection[month] = book
    await ctx.send(f"{book} has been chosen for the month of {month}")

#gets all members in current channel and fills collection with names and book status(default unfinished -- may need to change)
@bot.command()
async def getmembers(ctx):
    async for member in ctx.guild.fetch_members(limit=None):
        if member.name == 'BookClubBot':
            continue
        memberCollection[member.name] = 'unfinished'
    print(memberCollection)
        
@bot.command()
async def bookfinished(ctx):
    #get user who sent message
    user = ctx.author.name
    memberCollection[user] = 'finished'
    #need function for checking if all finished
    print(memberCollection)
    if checkAllFinished(memberCollection):
        await ctx.send('@everyone is finished their book! Time to discuss!')
    #want to else here and send message which displays how many people haven't finished their book (if only 1 person then at them)
    

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

#function which gets checks if all members of guild have completed the book
#can add way more functionality to this if i want
#perhaps in seperate functions
def checkAllFinished(memberCollection):
    allFinished = True
    for member in memberCollection:
        if memberCollection[member] == 'unfinished':
            allFinished = False
    
    return allFinished

#need the start method on loops or they dont run
weekly_announcment.start()

#must end with bot.run
bot.run(TOKEN)

##TODO
#need to refresh bookOfTheMonth if current month is changed
#need api call for !bookinfo 