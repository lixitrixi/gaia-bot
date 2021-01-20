# Imports
import discord
from discord.ext import commands
import os
import json
from random import randint


# Functions
def get_prefix(bot, message):
  with open('databases/prefixes.json', 'r') as f:
    prefixes = json.load(f)

  try:
    return prefixes[str(message.guild.id)]
  except KeyError:
    return '?' # default prefix


# Setup
bot = commands.Bot(command_prefix=get_prefix)

TOKEN = ""

bot.remove_command('help')
bot.add_check(commands.guild_only())

admin_ids = []


# Events
@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name} | {bot.user.id}")

@bot.event
async def on_guild_join(guild):
  with open('databases/prefixes.json', 'r') as f:
    prefixes = json.load(f)
  
  prefixes[str(guild.id)] = '?'

  with open('databases/prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)

@bot.event
async def on_guild_remove(guild):
  with open('databases/prefixes.json', 'r') as f:
    prefixes = json.load(f)
  
  prefixes.pop(str(guild.id))

  with open('data/prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)

@bot.event
async def on_message_edit(before, after):
  await bot.process_commands(after)

@bot.event
async def on_command_error(ctx, error):
  await ctx.send(error)


# Commands
@bot.command()
async def reload(ctx): # reloads all cogs
  if not ctx.author.id in admin_ids:
    return await ctx.send("You do not own this bot.")

  for file in os.listdir('cogs'):
    if file.endswith('.py'):
      bot.unload_extension(f'cogs.{file[:-3]}')
      bot.load_extension(f'cogs.{file[:-3]}')
    
  await ctx.message.add_reaction('✅')

@bot.command()
@commands.is_owner()
async def load(ctx, ext):
  if not ctx.author.id in admin_ids:
    return await ctx.send("You do not own this bot.")

  for file in os.listdir('cogs'):
    if file.endswith(f'{ext}.py'):
      bot.load_extension(f'cogs.{file[:-3]}')

  await ctx.message.add_reaction('✅')


# Runtime
for file in os.listdir('cogs'): # load .py files in cogs folder as extensions
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)
