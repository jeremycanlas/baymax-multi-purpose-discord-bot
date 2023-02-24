import random
import requests
import json
import asyncio
import aiohttp

# In order to get bot token from .env file so that bot token isn't exposed
import os
from dotenv import load_dotenv

# Library that allows for lyrics query from AZlyrics
from azapi import AZlyrics

# Library for python discord
from nextcord.ext import commands
import nextcord

load_dotenv()
nextcord.opus.load_opus("libopus.so")
#Changing Activity Status of Baymax
# activity = nextcord.Activity(type= nextcord.ActivityType.listening, name='you')
# bot = commands.Bot(command_prefix='!', activity=activity)

intents = nextcord.Intents.all()
intents.members = True
# activity = nextcord.Game(name="testing slash commands")
activity = nextcord.Activity(type= nextcord.ActivityType.listening, name='you')
# bot = commands.Bot(command_prefix='$', activity=activity, status=nextcord.Status.idle, intents = intents)
#bot = commands.Bot(command_prefix='$', activity=activity, intents = intents)
bot = commands.Bot(command_prefix='$', activity=activity, intents = intents)
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        bot.load_extension(f"modules.{folder}.cog")

#GREETINGS
greetings = ['hello baymax', 'hi baymax', 'baymax hello', 'baymax hi', 'salutations baymax', 'greetings baymax']
greetings_response = ['Hello I am Baymax, your personal healthcare companion... what seems to be the problem?', 'Hi I am Baymax, your personal healthcare companion... what seems to be the problem?', 'yo wassap homi']
special_greetings = ['yo baymax', 'baymax yo', 'sup baymax', 'baymax sup']
morning_greeting = ['goodmorning', 'good morning']
afternoon_greeting = ['good afternoon', 'goodafternoon']
evening_greeting = ['goodevening', 'good evening']

#NEGATIVE
pain_words = ['aray', 'ARAY', 'aray!', 'Aray!', 'sakit', 'SAKIT', 'Sakit', "ouch", 'OUCH', 'awit', 'Awit', 'AWIT']

words1 = ['bano', 'noob', 'BANO', 'NOOB', 'Bano', 'Noob']
rate_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '10']

violence = ['fight him for me baymax', 'fight her for me baymax', 'fight him baymax', 'fight her baymax', 'baymax fight her', 'baymax fight him', 'fight baymax', 'baymax fight', 'baymax i choose you', 'baymax i choose u']

violence_response = ['Low battery...', 'My programming prevents me from injuring a human being.', "I am not fast.", "My hands are equipped with defibrillators...Clear."]

sad_words = ['sad', 'lonely', 'depressed', 'alone']

go_away = ['go away baymax', 'no baymax', 'stfu baymax', 'baymax stfu', 'shut up baymax', 'baymax shut up']

go_away_frozen = ['go away anna']

#CARING
inspire_keyword = ['inspirational', 'cheer', 'comfort', 'inspire', 'wise']

encouragement = ['There there.', "You will be alright. There. There.", 'It is okay to cry. Crying is a natural response to pain.', 'You have been a good boy / girl you may have a lollipop', "Would you like a hug?"]

thanks_keyword = ['thanks baymax', 'baymax thanks', 'baymax thank you', 'salamat baymax', 'thank you baymax', 'baymax salamat']

bored_keyword = ['bored']

bored_response = ['Might I have to remind you of your readings?', 'Perhaps you might be forgetting something... academic', 'Have you tried talking to a real person?', 'An apple a day keeps the doctor away', 'Try eating some snacks']

happy = ["hurray", "yay", "YES", 'celebrate']
happy_response = ["My sensors indicate a rise in serotonin, initaiting dancing maneuvers..."]
#UNIQUE GIMMICK
fistbump = ['fistbump', 'fist bump']

shout_out = ['pashout out baymax','pashoutout baymax', 'shout out baymax', 'baymax pashout out', 'baymax mention me', 'mention me baymax', 'mention me']

shout_out_response = ['gotchu', 'gotchu homi', 'here you go', 'sending one your way', 'okay okay', 'sige sige', 'gegege']

kiss_keyword = ['pakiss', 'kiss me']

dance_keyword = ['dance']

dance_response = ['I think I can dance.',
'I have all the right moves.']

#ARBITRARY
initialize_number = list(range(10,100,1))

#Functions
#Using zenquotes for random inspirational quotes + author name
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

  
#WIP, random binary number generator that doesn't work as intended
def rand_key():
  key1 = ""
  for i in range(random.choice(initialize_number)):
    temp = str(random.randint(0, 1))
    key1 += temp
  return(key1)

#Discord Events
#Function that prints a phrase when baymax goes online
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=nextcord.Game(name="on " + str(len(bot.guilds)) + " Servers", type=0))

#Message based events
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    print(f"{username} said: '{user_message}' ({channel})")
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    if message.author.bot:
        return

#Initial Starter Quips
    if message.content.startswith('initialize baymax') or message.content.startswith('baymax initialize') or message.content.startswith('initialize'):
        await message.channel.send(rand_key())
    
    if message.content.startswith('baymax what can you do') or message.content.startswith('baymax what can u do'):
        await message.channel.send('you homi SHEEEEEESH')

    #Greeting Variance
    if any(greet in message.content for greet in greetings):
        await message.channel.send(random.choice(greetings_response))

    if any(word in message.content for word in special_greetings):
        await message.channel.send("Yo yo yo")
    if any(word in message.content for word in morning_greeting):
        await message.channel.send('Good morning, ready to start the day? ' + "{0.author.mention}".format(message))
    
    if any(word in message.content for word in afternoon_greeting):
        await message.channel.send('Good afternoon ' + "{0.author.mention}".format(message) + ', don\'t forget to hydrate yourself')

    if any(word in message.content for word in evening_greeting):
        await message.channel.send('Good evening ' + "{0.author.mention}".format(message))

    #Caring
    if any(word in message.content for word in sad_words):
        await message.channel.send('On a scale of 1 to 10, how would you rate your pain?')

    if any(vio in message.content for vio in violence):
        await message.channel.send(random.choice(violence_response))
    
    if message.content in pain_words:
        await message.channel.send('I heard a sound of distress. What seems to be the trouble?')

    if any(word in message.content for word in thanks_keyword):
        await message.channel.send('You are most certainly welcome{0.author.mention}'.format(message))

    if any(word in message.content for word in go_away):
        await message.channel.send('I cannot deactivate until you say you are satisfied with your care.')

    if any(word in message.content for word in go_away_frozen):
        await message.channel.send('Okay bye...')

    if message.content.startswith('i am satisfied with my care'):
        await message.channel.send('***SHUTTING DOWN***')
    if message.content.startswith('baymax deactivate'):
        await message.channel.send('***DEACTIVATING***')
    #inspire
    if any(word in message.content for word in inspire_keyword):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content in rate_number:
        await message.channel.send(random.choice(encouragement))

    #Unique Gimmick
    if any(word in message.content for word in fistbump):
        await message.channel.send('Bah-a-la-la-la.')

    if message.content.startswith('hiro is sick'):
        await message.channel.send('OMW')

    if message.content.startswith('baymax translate'):
        await message.channel.send('you are on your own homi')

    if any(word in message.content for word in words1):
        await message.channel.send('grabe naman lods')

    if any(word in message.content for word in shout_out):
        await message.channel.send(random.choice(shout_out_response) + "{0.author.mention}".format(message))

    if any(word in message.content for word in kiss_keyword):
        await message.channel.send(':* {0.author.mention}'.format(message))
    if any(word in message.content for word in dance_keyword):
        await message.channel.send(random.choice(dance_response))
    for word in happy:
        if word in message.content:
            await message.channel.send(random.choice(happy_response))
    if message.content.startswith('!hello'):
        await message.reply('Hello!', mention_author=True)
    if any(word in message.content for word in bored_keyword):
        await message.channel.send(random.choice(bored_response))

# @bot.command()
# async def join(ctx):
#     channel = ctx.author.voice.channel
#     await channel.connect()

# @bot.command()
# async def leavee(ctx):
#     await ctx.voice_client.disconnect()

bot.run(os.environ["BAYMAX_TOKEN"])