import discord
from discord.ext import commands

class JoinOrLeave(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = self.client.get_channel(1072215763529777274)
    await channel.send(f"Welcome, master {member.name}")

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    member.channle
    channel = self.client.get_channel(1072215763529777274)
    await channel.send(f"Farewell, master {member.name}")

async def setup(client):
  await client.add_cog(JoinOrLeave(client))