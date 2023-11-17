import discord
from discord.ext import commands
import os
import subprocess

BOT_TOKEN = '<your token>'
intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

WHITELIST = {
    724668769619804240,
    724668769619804240, # User ID
}

# The name of the channel for the bot to operate in
CHANNEL_NAME = 'dish'

def is_whitelisted():
    def predicate(ctx):
        return ctx.message.author.id in WHITELIST
    return commands.check(predicate)

@bot.event
async def on_guild_join(guild):
    permissions = discord.Permissions(send_messages=True, embed_links=True, read_messages=True)
    await guild.create_text_channel(CHANNEL_NAME, overwrites={
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    })
    

@bot.command()
@is_whitelisted()
async def shell(ctx, *, cmd):
    if isinstance(ctx.channel, discord.DMChannel) or ctx.channel.name == CHANNEL_NAME: 
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        if stdout:
            await ctx.send(f'```{stdout.decode()}```')
        if stderr:
            await ctx.send(f'```{stderr.decode()}```')

@bot.command()
@is_whitelisted()
async def test(ctx):
    if isinstance(ctx.channel, discord.DMChannel) or ctx.channel.name == 'dish':
        await ctx.send('Test message in #dish.')

bot.run(BOT_TOKEN)
