# Imports
import discord
from discord.ext import commands
import random
import sys
import json


# Functions
def set_prefix(guild_id, prefix): # Creates a new entry or edits an old prefix entry
  with open('databases/prefixes.json', 'r') as f:
    prefixes = json.load(f)
  
  prefixes[str(guild_id)] = prefix

  with open('databases/prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)


# Cog
class General(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Commands
  @commands.command()
  async def ping(self, ctx):
    await ctx.send(f"Pong! ({round(self.bot.latency*1000)}ms)")
  
  @commands.command()
  async def set_prefix(self, ctx, *, prefix='?'):
    set_prefix(ctx.guild.id, prefix)
    await ctx.send(f"This server's prefix has been set to `{prefix}`")

  @commands.command()
  async def roo(self, ctx, n=20):
    await ctx.send('ROO '*n)

  @commands.command(aliases=['r'])
  async def roll(self, ctx, args):
    dice = args.split("d") # ['5', '6'] 
    result = [random.randint(1,int(dice[1])) for n in range(int(dice[0]))]

    result.sort()

    result_embed = discord.Embed()
    result_embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    result_embed.add_field(name=f"Result: {sum(result)}", value=str(result))

    await ctx.send(embed=result_embed)
  
  @commands.command()
  async def coinflip(self, ctx):
    await ctx.send(random.choice(['Heads!', 'Tails!']))

  @commands.command() # Poll Command, adds a poll to the message
  async def poll(self, ctx, *, choices="😀 😐 😕"):
    [await ctx.message.add_reaction(choice) for choice in choices.split(' ')]

def setup(bot):
  bot.add_cog(General(bot))
