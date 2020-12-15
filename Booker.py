import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from discord.message import Attachment
import requests
import json
from TOKEN import *
from Date import *
#intializes date object
date = Date()

#bookGetter // GET based on title - no async though oof
def getBook(bookTitle):
        try:
            response = requests.get(f"https://v1.nocodeapi.com/colourised/gr/ylbRWcheecMozbsx/search?q={bookTitle}").json()
            print("BookFinder Succesful!")
            return response
        except:
            print("Unable to Find Book Info!")

#collection of months and corresponding book // 
# should start blank and be added to as books are chosen through commands
#expansion will include bookShelf object to move this outta main
#TODO
#if book collection is empty can prompt choices for the month possibly?
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

#could put this into a bookshelf object aswell
#only using
#no longer using but have a bookOfMonth bookshelf method could save code
# bookOfTheMonth = bookCollection[date.getMonth()]

#general channel id -- must have -- book club only has one channel so dont need to edit this rn
#if expanded to work for others would need to have a different solution to finding channel id
CHANNEL_ID = 784457938551046167

# this event makes sure bot is ready and will output when it is
# want to update status aswell
#TODO
#ez fix just update String currentlyReading when running the 24hour bot will change if book changes
@bot.event
async def on_ready():
    print('Booker started reading!')
    await bot.change_presence(activity= discord.Activity(type = discord.ActivityType.listening, name = bookCollection[date.getMonth()]))

#provides title and author of current months book
#should put this into variables for readability probably just parsing json rn
@bot.command()
async def currentbook(ctx):
    bookResponse = getBook(bookCollection[date.getMonth()])
    await ctx.send(f"{bookResponse['results'][0]['title']} by {bookResponse['results'][0]['author']['name']}")
    await ctx.send(bookResponse['results'][0]['image_url'])

#gets book COVER / NAME / AUTHOR with API call for given month
@bot.command()
async def bookinfo(ctx, month):
    bookResponse = getBook(bookCollection[month])
    await ctx.send(f"{bookResponse['results'][0]['title']} by {bookResponse['results'][0]['author']['name']}")
    await ctx.send(bookResponse['results'][0]['image_url'])


#command to addbook to a selected month
@bot.command()
async def addbook(ctx, month, book):
    month = month.capitalize()
    bookCollection[month] = book
    await ctx.send(f"{book} has been chosen for the month of {month}")

#gets all members in current channel and fills collection with names and book status(default unfinished -- may need to change)
#should put all users in clubMembers object which can pull info
#cleaner
#should probably launch this when bot starts just to establish working !finished command
@bot.command()
async def getmembers(ctx):
    async for member in ctx.guild.fetch_members(limit=None):
        if member.name == 'BookClubBot':
            continue
        memberCollection[member.name] = 'unfinished'
    print(memberCollection)
        
@bot.command()
async def finished(ctx):
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

#ideally want to @ anyone who hasnt finished their book
#this is only command which uses channelID
@tasks.loop(hours=24)
async def weekly_announcment():
    messageChannel = bot.get_channel(CHANNEL_ID)
    if date.getDay() == 1:
        await messageChannel.send(f"@everyone It is {date.getMonth()}! Time for a new book! This month you're reading {bookCollection[date.getMonth()]}")
    #reminder halfway through month
    if date.getDay() == 15:
        await messageChannel.send(f"@everyone We are halfway through the month! Are you halfway through {bookCollection[date.getMonth()].capitalize()}?")
    #send discussion questions? actual check of last day // currently assuming all months 30 
    #TODO - actual check for last day before sending month is over thing date.CheckLast() == true then send message
    if date.getDay() == 30:
        await messageChannel.send(f"@everyone The month is over hope you're done {bookCollection[date.getMonth()]}!")
#needed for loops to work
@weekly_announcment.before_loop
async def before():
    await bot.wait_until_ready()
    date.updateDate()
    print(f"Updated Date to {date.getDate()}")

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