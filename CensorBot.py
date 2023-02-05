import discord
import json
import re

print(f"Discord.py Version: {discord.__version__}")

print("Loading Discord Client...")

print("Loading Bot Info...")
TOKEN = "";#Put your bot's token here
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
guilds = []
print("Loaded Bot Info!")

print("Loading JSON's...")
#storedvars
storedvarsjson = open("storedvars.json", "r", encoding="utf-8")
storedvars = json.load(storedvarsjson)
storedvarsjson.close()
#blocked
blockedjson = open("blocked.json", "r", encoding="utf-8")
blocked = json.load(blockedjson)
blockedjson.close()
#admins
adminsjson = open("admins.json", "r", encoding="utf-8")
admins = json.load(adminsjson)
adminsjson.close()
print("Loaded JSON's!")

print("Sucessfully Loaded Discord Client!\nStarting Discord Client...")

@client.event
async def on_ready():
    print("We have logged in as {0.user}!".format(client))
    
async def messages(message, user_message, userid):
    #Admin commands
    if str(userid) in admins["admins"]:
        if user_message[0] == '!':
            if user_message[1:5] == "help":
                await message.channel.send("Commands:\n---------\n-urlblock: toggles URLblock to block links\n-block: blocks a specific string\n-unblock: unblocks a specific string\n-addadmin: adds an admin\n-removeadmin: removes an admin")
            elif user_message[1:9] == "urlblock":
                storedvars["URLblock"] = not storedvars["URLblock"]
                urlblockjson = open("storedvars.json", "w", encoding="utf-8")
                json.dump(storedvars, urlblockjson)
                urlblockjson.close()
                if storedvars["URLblock"]:
                    await message.channel.send("URLblock was enabled!")
                else:
                    await message.channel.send("URLblock was disabled!")
            elif user_message[1:6] == "block":
                if not user_message[7:len(user_message)] in blocked["blocked"]:
                    blocked["blocked"].append(user_message[7:len(user_message)])
                    addblockedjson = open("blocked.json", "w", encoding="utf-8")
                    json.dump(blocked, addblockedjson)
                    addblockedjson.close()
                    await message.channel.send(f"The string {user_message[7:len(user_message)]} has been blocked!")
                else:
                    await message.channel.send("That block already exists!")
            elif user_message[1:8] == "unblock":
                if user_message[9:len(user_message)] in blocked["blocked"]:
                    blocked["blocked"].remove(user_message[9:len(user_message)])
                    unblockjson = open("blocked.json", "w", encoding="utf-8")
                    json.dump(blocked, unblockjson)
                    unblockjson.close()
                    await message.channel.send(f"The string {user_message[9:len(user_message)]} has been unblocked!")
                else:
                    await message.channel.send("That block doesn't exist!")
            elif user_message[1:15] == "stringsblocked":
                await message.channel.send(blocked["blocked"])
            elif user_message[1:9] == "addadmin":
                if not user_message[10:len(user_message)] in admins["admins"]:
                    admins["admins"].append(user_message[10:len(user_message)])
                    addadminjson = open("admins.json", "w", encoding="utf-8")
                    json.dump(admins, addadminjson)
                    addadminjson.close()
                    await message.channel.send(f"Admin {user_message[13:len(user_message)]} has been added!")
                else:
                    await message.channel.send("That admin already exists!")
            elif user_message[1:12] == "removeadmin":
                if user_message[13:len(user_message)] in admins["admins"]:
                    admins["admins"].remove(user_message[13:len(user_message)])
                    removeadminjson = open("admins.json", "w", encoding="utf-8")
                    json.dump(admins, removeadminjson)
                    removeadminjson.close()
                    await message.channel.send(f"Admin {user_message[13:len(user_message)]} has been removed!")
                else:
                    await message.channel.send("That admin doesn't exist!")
            else:
                await message.channel.send("That was an invalid command!")
    else:
        #Blocking
        if storedvars["URLblock"]:
            if re.search("(?P<url>https?://[^\s]+)", user_message) != None:
                await message.delete()
                await message.channel.send(f"You can't send URLs when URLblock is on <@{userid}>!")
        if any(ext in user_message for ext in blocked["blocked"]):
            await message.delete()
            await message.channel.send(f"You can't send that word <@{userid}>!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    userid = int(message.author.id)
    user_message = str(message.content)

    if isinstance(message.channel, discord.channel.DMChannel):
        await messages(message, user_message, userid)
    elif isinstance(message.channel, discord.channel.TextChannel):
         await messages(message, user_message, userid)
    else:
        print("There was a request send from a channel that we could not access")
            
client.run(TOKEN)
