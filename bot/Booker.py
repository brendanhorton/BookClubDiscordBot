from MemberList import MemberList
from BookShelf import BookShelf
import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from discord.message import Attachment
import requests
import json
from Date import Date
import os

TOKEN = os.environ.get('TOKEN')

#intializes Objects // have Date, BookShelf, and MemberList each controls respective group
date = Date()
bookShelf = BookShelf()
memberList = MemberList()

#bookGetter // GET based on title - no async though oof
def getBook(bookTitle):
        try:
            response = requests.get(f"https://v1.nocodeapi.com/colourised/gr/ylbRWcheecMozbsx/search?q={bookTitle}").json()
            print("BookFinder Succesful!")
            return response
        except:
            print("Unable to Find Book Info!")

#command prefix and bot object
#also removes default help command
bot = Bot(command_prefix='!')

#general channel id -- must have -- book club only has one channel so dont need to edit this rn
#if expanded to work for others would need to have a different solution to finding channel id
CHANNEL_ID = 792860110308638743


# this event makes sure bot is ready and will output when it is
# want to update status aswell
#TODO
#ez fix just update String currentlyReading when running the 24hour bot will change if book changes
@bot.event
async def on_ready():
    print('Booker started reading!')
    await bot.change_presence(activity= discord.Activity(type= discord.ActivityType.listening, name= bookShelf.getBook(date.getMonth())))

#provides title and author of current months book and image
#DONE
@bot.command()
async def currentbook(ctx):
    bookResponse = getBook(bookShelf.getBook(date.getMonth()))
    bookTitle = bookResponse['results'][0]['title']
    bookAuthor = bookResponse['results'][0]['author']['name']
    await ctx.send(f"{bookTitle} by {bookAuthor}")
    await ctx.send(bookResponse['results'][0]['image_url'])

#gets book COVER / NAME / AUTHOR with API call for given month
#DONE
@bot.command()
async def bookinfo(ctx, month):
    bookResponse = getBook(bookShelf.getBook(month))
    bookTitle = bookResponse['results'][0]['title']
    bookAuthor = bookResponse['results'][0]['author']['name']
    await ctx.send(f"{bookTitle} by {bookAuthor}")
    await ctx.send(bookResponse['results'][0]['image_url'])


#command to addbook to a selected month
#DONE
@bot.command()
async def addbook(ctx, month, book):
    bookShelf.updateMonth(month, book)
    await ctx.send(f"{book} has been chosen for the month of {month}")

#gets all members in current channel and fills collection with names and book status
@bot.command()
async def getmembers(ctx):
    memberCollection = {}
    async for member in ctx.guild.fetch_members(limit=None):
        if member.name == 'BookClubBot':
            continue
        memberCollection[member.name] = 'unfinished'
    memberList.populateList(memberCollection)
    memberList.getMembers()

@bot.command()
async def finished(ctx):
    #get user who sent message
    user = ctx.author.name

    memberList.getMembers()
    memberList.markFinished(user)

    memberList.getMembers()
    if memberList.checkAll():
        await ctx.send('@everyone is finished their book! Time to discuss!')
    else:
        await ctx.send('Not everyone is finished their book yet. Kick back and relax.')
    #want to else here and send message which displays how many people haven't finished their book (if only 1 person then at them)

#ideally want to @ anyone who hasnt finished their book 
#this is only command which uses channelID (can i fix that?)
@tasks.loop(hours=24)
async def weekly_announcment():
    messageChannel = bot.get_channel(CHANNEL_ID)
    if date.getDay() == 1:
        memberList.reset()
        await messageChannel.send(f"@everyone It is {date.getMonth()}! Time for a new book! This month you're reading {bookShelf.getBook(date.getMonth())}")
    #reminder halfway through month
    if date.getDay() == 15:
        await messageChannel.send(f"@everyone We are halfway through the month! Are you halfway through {bookShelf.getBook(date.getMonth())}?")
    #TODO - actual check for last day before sending month is over thing date.CheckLast() == true then send message
    if date.getDay() == 30:
        await messageChannel.send(f"@everyone The month is over hope you're done {bookShelf.getBook(date.getMonth())}!")
        

#needed for loops to work
@weekly_announcment.before_loop
async def before():
    await bot.wait_until_ready()
    date.updateDate()
    print(f"Updated Date to {date.getDate()}")

#need the start method on loops or they dont run
weekly_announcment.start()

#must end with bot.run
bot.run(TOKEN)