import discord
from discord.ext import tasks, commands
import subprocess
import re

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix=commands.when_mentioned_or("&"))
        self.synced = False

    async def setup_hook(self) -> None:
        await self.add_cog(IPChecker(self))
        return await super().setup_hook()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        if not self.synced:
            await self.tree.sync()
            self.synced = True

class IPChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currentIp = ""
        print("Cog init")
        self.ip_checker.start()

    def cog_unload(self):
        print("Cog unload")
        self.ip_checker.cancel()

    @tasks.loop(seconds=5.0)
    async def ip_checker(self):
        completedProcess = subprocess.run("dig +short myip.opendns.com @resolver1.opendns.com", check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) #If this errors out, it stops the program, routes normal output back here
        newIpDirty = str(completedProcess.stdout)
        newIp = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', newIpDirty)[0] #Sanitizes it from b'xxx.xxx.xxx.xxx\n' to xxx.xxx.xxx.xxx
        if newIp == self.currentIp:
            return
        self.currentIp = newIp
        owner = bot.application.owner
        if owner.dm_channel == None:
            await owner.create_dm()
        await owner.dm_channel.send(f'Current public IP: {self.currentIp}')

token = ""
with open("/run/secrets/iposter_token") as f:
    token = f.read()

bot = Bot()
bot.run(token)