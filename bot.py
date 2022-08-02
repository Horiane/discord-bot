#bot.py
#?--- Imports ---
from os import getenv # Allows to program accsess .env files (enviromental variables)
from discord import Client, Intents, Embed, Color # Imports the discord client and intents which are used to get higher level accsess to the API
from discord.utils import get # Imports the get functions from discord.py utilitys
from dotenv import load_dotenv # Loads environment variables from a .env file into your shell’s environment variables so that you can use them in your code
from asyncio import TimeoutError, sleep # Used when waiting x time for a response
from random import randint, choice #Used to make random choices
from giphy_client import DefaultApi # Imports the giphy client
from giphy_client.rest import ApiException # Used when handling API errors
#? Opening banned words
with open('BadWords.txt', 'r') as f:
    words = f.read()
    badwords = words.split()
#?--- Intents ---
intents = Intents.default() # Sets up intents with default settings, these  are used to get higher level accsess to the API
intents.members = True # Enables the members intent, which allows us to mention/ping users

#?--- Imports the data from .env's ---
# Loads the env's from a seperate file into this one, this is done for security reasons.
load_dotenv()
DISCORD_TOKEN = getenv('DISCORD_TOKEN') # The TOKEN is a unique identifier for our bot, its how our program knows what bot on discord to connect to
GIPHY_TOKEN = getenv('GIPHY_TOKEN')

#?--- Variables ---
welcomeChannelID = 997500329262333982
reactionMessageID = 999697327180759244
commandPrefix = "!"#Command prefix
#?--- Init' Client ---
# A Client is an object that represents a connection to Discord. 
# The Client handles events, tracks states, and generally interacts with Discord APIs.
client = Client(intents=intents)

#?--- Events ---
#? Performs actions based on keywords in user messages
@client.event # Starts an event
async def on_message(message): # Runs the on_message API call
    #* Stops the bot responding to it's self
    if message.author == client.user:
        return
    #* Output commands availible
    elif message.content.lower().startswith(commandPrefix + "commands"): #Checks to see if  message starting with !commands is sent
        emb = Embed(color = Color.blue(), title="Bot Functions", description=f"All of the commands and functions(command prefix is '!'):\n-Auto delete swear words\n-'!ping' to check client latency\n-'!dice' rolls dice\n-'!rps [your choice], ex. !rps rock") #Creates an embedded message
        await message.channel.send(embed=emb)
    #* Ping pong game with latency check
    elif message.content.lower().startswith(commandPrefix + "ping"):
        await message.channel.send(f'Pong! In {round(client.latency * 1000)}ms')
    #* Dice
    elif message.content.lower().startswith(commandPrefix + "dice"):
        await message.channel.send(f'The dice rolls '+str(randint(1,6))+'!')
    #* Rock Paper Scissor
    elif message.content.lower().startswith(commandPrefix + "rps"):
        humchoice=message.content.lower()[5]
        rnd="rps"
        comchoice=rnd[randint(0,2)]
        #Does the computer win?
        if comchoice=="r" and humchoice=="s":
            await message.channel.send("Computer wins!\nYou choosed scissors, the computer choosed rock.")
        elif comchoice=="p" and humchoice=="r":
            await message.channel.send("Computer wins!\nYou choosed rock, the computer choosed paper.")
        elif comchoice=="s" and humchoice=="p":
            await message.channel.send("Computer wins!\nYou choosed paper, the computer choosed scissors.")
        #Does the human win?
        elif humchoice=="r" and comchoice=="s":
            await message.channel.send("You win!\nYou choosed rock, the computer choosed scissors.")
        elif humchoice=="p" and comchoice=="r":
            await message.channel.send("You win!\nYou choosed paper, the computer choosed rock.")
        elif humchoice=="s" and comchoice=="p":
            await message.channel.send("You win!\nYou choosed scissor, the computer choosed paper.")
        #Does they draw?
        elif humchoice=="s" and comchoice=="s":
            await message.channel.send("Draw!\nYou choosed scissors, the computer choosed scissor too!")
        elif humchoice=="p" and comchoice=="p":
            await message.channel.send("Draw!\nYou choosed paper, the computer choosed paper too!")
        elif humchoice=="r" and comchoice=="r":
            await message.channel.send("Draw!\nYou choosed rock, the computer choosed rock too!")
    #*Stores user message
    msgCheck = message.content.lower()
    #*Swear word filter (could add more words) enough for now
    for word in badwords:
        if word in msgCheck:
            await message.delete()
            msg=await message.channel.send(f'Stop swearing {message.author.mention}!')
            await sleep(2)
            await msg.delete()
            return


#? Shows the the program has made a connection between its self and the discord bot
@client.event # Starts an event
async def on_ready(): # Runs the on_ready API call
# Uses the get API call to the servers the the bot is connected to
    print(f"{client.user.name} has connected to the following servers:\n") #Prints the name of the bot and lists connected servers and their IDs
    for guild in client.guilds:
        print(f"Name: {guild.name}, ID: {guild.id}")

#* Connects the client to our bot via its TOKEN & runs the above functions
client.run(DISCORD_TOKEN)
