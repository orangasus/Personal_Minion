import discord
from discord.ext import commands


class Errors(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      await ctx.send('Sorry, master. I do not understand...')

async def setup(client):
  await client.add_cog(Errors(client))