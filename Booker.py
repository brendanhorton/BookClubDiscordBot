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

#want to eventually create hash to keep track of books for each month -- hardcoding for now
bookOfTheMonth = 'Death on the Nile'

# this event makes sure bot is ready and will output when it is
#want to change bot so it displays the current months book // not sure how 
#maybe i need to use a datetime object and conditionals
#if month == x then output y as name of activity
#can have large hash with book for each month
#expansion would include allowing user to set books for each month per instance of bot
#doable
@bot.event
async def on_ready():
    print('Booker started reading!')
    await bot.change_presence(activity= discord.Activity(type = discord.ActivityType.listening, name = bookOfTheMonth))

#when someone types test bot returns testing 123
#need to translate datetime into written month -- shouldnt be hard -- might be included in module quick google
@bot.event
async def on_message(message):
    if message.content == '!currentbook':
        await message.channel.send(f'The book for the month of December is {bookOfTheMonth}')
    
    await bot.process_commands(message)


#goal is to create multiple different reminders based on date
#halfway point
#end of month
#once i add !finished then i can @ only the people who arent done their books -- less channel spam
@tasks.loop(hours=24)
async def weekly_announcment():
    messageChannel = bot.get_channel(CHANNEL_ID)
    #on 15th sends reminder to read
    if currentDate.day == 15:
        await messageChannel.send(f"@everyone We are halfway through the month! Are you halfway through {bookOfTheMonth}?")
    #
    if currentDate.day == 30:
        await messageChannel.send(f"@everyone The month is over hope you're done {bookOfTheMonth}!")
    else:
        await messageChannel.send(f"@everyone This is just a testing conditional I don't care what the date is makes sure loop is working.")


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