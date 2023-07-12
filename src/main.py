import discord
from discord.ext import tasks, commands
import subprocess


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
currentIp = None

@client.event
async def on_ready():
    owner = client.application.owner

class MyCog(commands.Cog):
    def __init__(self):
        self.ip_checker.start()

    def cog_unload(self):
        self.ip_checker.cancel()

    @tasks.loop(hours=1.0)
    async def ip_checker(self):
        completedProcess = subprocess.run("dig +short myip.opendns.com @resolver1.opendns.com", check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) #If this errors out, it stops the program, routes normal output back here
        newIp = str(completedProcess.stdout)
        if newIp == currentIp:
            return
        currentIp = newIp
        owner = client.application.owner
        if owner.dm_channel == None:
            await owner.create_dm()
        await owner.dm_channel.send(f'Current public IP: {currentIp}')

token = ""
with open("iposter_token.txt") as f:
    token = f.readlines()
client.run(token)