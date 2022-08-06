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
from deck import cardDeck
#? Opening banned words
with open('BadWords.txt', 'r') as f:
    words = f.read()
    badwords = words.split()
#?--- Imports the data from .env's ---
# Loads the env's from a seperate file into this one, this is done for security reasons.
load_dotenv()
DISCORD_TOKEN = getenv('DISCORD_TOKEN') # The TOKEN is a unique identifier for our bot, its how our program knows what bot on discord to connect to
GIPHY_TOKEN = getenv('GIPHY_TOKEN')
#?--- Variables ---
welcomeChannelID = 997500329262333982
reactionMessageID = 999697327180759244
commandPrefix = "!"#Command prefix

#?--- Intents ---
intents = Intents.default() # Sets up intents with default settings, these  are used to get higher level accsess to the API
intents.members = True # Enables the members intent, which allows us to mention/ping users
#?--- Init' Client ---
# A Client is an object that represents a connection to Discord. 
# The Client handles events, tracks states, and generally interacts with Discord APIs.
client = Client(intents=intents)
#fuctions
def card():
    global playerCards,playerValue,dealerCards,dealerValue
    playerCards,playerValue=choice(list(cardDeck.items()))
    del cardDeck[playerCards]
    dealerCards,dealerValue=choice(list(cardDeck.items()))
    del cardDeck[dealerCards]
    print(playerCards,playerValue,dealerCards,dealerValue)
    return playerCards,playerValue,dealerCards,dealerValue


def blackjack():
    global playerValue,dealerValue,emb1,dealerPoints,playerPoints
    playerPoints=0
    dealerPoints=0
    card()
    emb1=Embed(color = Color.blue(), title="Bot Functions", description=f"You pulled out a:\n" + playerCards + "\nDealer pulled out a:\n" + dealerCards)
    
        
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
        comchoice=choice(rnd)
            #Does the computer win?
        if comchoice=="r" and humchoice=="s":
            await message.channel.send("You choose scissors.\nI choosed rock.\n**I win!**")
        elif comchoice=="p" and humchoice=="r":
            await message.channel.send("You choose rock.\nI choosed paper.\n**I win!**")
        elif comchoice=="s" and humchoice=="p":
            await message.channel.send("You choose paper.\nI choose scissors.\n**I win!**")
        #Does the human win?
        elif humchoice=="r" and comchoice=="s":
            await message.channel.send( "You choose rock.\nI choose scissors.\n**You win!**")
        elif humchoice=="p" and comchoice=="r":
            await message.channel.send("You choose paper.\nI choosed rock.\n**You win!**")
        elif humchoice=="s" and comchoice=="p":
            await message.channel.send("You choose scissor.\nI choose paper.\n**You win!**")
        #Does they draw?
        elif humchoice=="s" and comchoice=="s":
            await message.channel.send("You choose scissors.\nI choose scissor.\n**Draw!**")
        elif humchoice=="p" and comchoice=="p":
            await message.channel.send("You choose paper.\nI choose paper.\n**Draw!**")
        elif humchoice=="r" and comchoice=="r":
            await message.channel.send("You choose rock.\nI choose rock.\n**Draw!**")
    elif message.content.lower().startswith(commandPrefix + "bj") or message.content.lower().startswith(commandPrefix + "blackjack"):
        await message.channel.send("The command is WIP, it may not work as intended")
        blackjack()
        message = await message.channel.send(embed=emb1)
        message_id = message.id
        await message.add_reaction("👊")
        await message.add_reaction("🛑")
        #wip
        #? Reaction roles, assigns role based on message reactions
        #@client.event
        #async def on_raw_reaction_add(payload):# Checks for reactions being removed from a message
        #    server = client.get_guild(payload.guild_id) # Gets the server ID
        #    
        #    if payload.message_id == reactionMessageID: # Checks if the ID of the message matches the reaction roles message ID
        #        role = None # Sets the role variable to None (empty)
        #        if payload.emoji.name == "👊": # Checks if the reaction emoji matches this emoji     
        #            playerPoints += playerValue
        #            dealerPoints += dealerValue
        #            await message.edit(embed=emb2)      
        #        elif payload.emoji.name == "🛑":
        #            pass
        ##? Reaction roles, removes role based on message reactions
        #@client.event
        #async def on_raw_reaction_remove(payload): # Checks for reactions being removed from a message and gets the payload wich contains all the infomation about the event
        #    pass
        #    server = client.get_guild(payload.guild_id) # Gets the server ID

        #    if payload.message_id == reactionMessageID: # Checks if the ID of the message matches the reaction roles message ID
        #        role = None

        #        if payload.emoji.name == "🎮": # Checks if the reaction emoji matches this emoji
        #            role = get(server.roles, name = "Roblox Player") #Gets the role from the server
        #        
        #        elif payload.emoji.name == "🎵":
        #            role = get(server.roles, name = "Music Lover")
        #        
        #        if role is not None: # Makes sure a role has been assigned to the role variable
        #            member = server.get_member(payload.user_id) # Gets the ID of the user who removed the emoji
        #            if member is not None: #Makes sure the member is still in the server
        #                await member.remove_roles(role) # Removes the role from the user

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

