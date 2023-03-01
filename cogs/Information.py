import discord
from discord.ext import commands

my_orange = 0xfc6203


class Information(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(
    description=
    'Displays information about the server: name, creation date, number of memebers, owner and description'
  )
  async def server_info(self, ctx):
    guild = ctx.guild
    num_members = guild.member_count
    created_date = f'{guild.created_at.day:02}.{guild.created_at.month:02}.{guild.created_at.year}'
    desc = guild.description if guild.description != None else '???'

    msg = f'ID: {guild.id}\nCreated: {created_date}\nMembers: {num_members}\nOwner: {guild.owner.name}\nDescription: {desc}'

    embed = discord.Embed(title=guild.name, description=msg, color=my_orange)
    icon = guild.icon if guild.icon != None else 'https://static.wixstatic.com/media/1f9c5d_b553ba0ec050464dbbd9bea215f10e94~mv2.png'
    embed.set_thumbnail(url=f'{icon}')
    await ctx.send(embed=embed)

  @commands.command(
    name="help",
    description=
    "Returns all commands available with their full description by default. User can pass command names to receive info only about specific commands"
  )
  async def help(self, ctx, *args):
    helptext = ""
    if len(args) == 0:
      for command in self.client.commands:
        helptext += '```' + f"${command.name} - {command.description}\n" + '```'
    else:
      query = list(set(args))
      for command in self.client.commands:
        if str(command) in args:
          helptext += '```' + f"${command.name} - {command.description}\n" + '```'
          query.remove(str(command))
      if len(query) > 0:
        helptext = f"_Ignored: {', '.join(query)} - not commands\n_" + helptext
    await ctx.send(helptext)


  def format_member_info(self, d):
    msg = '```'+'ID: {}\nCreated: {}\nJoined: {}\nStatus: {}\nActivities: {}'.format(d['id'],d['creation_date'],d['joined_date'],d['status'],d['activity'])+'```'
    embed = discord.Embed(title=d['name'], description=msg, color=my_orange)
    embed.set_thumbnail(url=d['avatar'])
    embed.set_footer(text=d['bot'])
    return embed

  def get_member_info(self, member):
    creation_date = f'{member.created_at.day:02}.{member.created_at.month:02}.{member.created_at.year}'
    name = member.display_name
    avatar = member.display_avatar
    joined_date = f'{member.joined_at.day:02}.{member.joined_at.month:02}.{member.joined_at.year}'
    is_bot = 'Human' if not member.bot else 'Bot'
    status=f'{member.status}'
    activites = member.activities
    print(activites)
    if activites == None or len(activites) == 0:
      activites = '???'
      print('No activities')
    else:
      activites = activites[0].name
    d = {
      'creation_date': creation_date,
      'name': name,
      'avatar': avatar,
      'joined_date': joined_date,
      'status': status,
      'bot': is_bot,
      'id': member.id,
      'activity' : activites
    }
    return d

  @commands.command(
    description='Displays information about a server member\\members. If the username contains spaces, it should be enclosed in quotation marks')
  async def user_info(self, ctx, *args):
    guild = ctx.guild
    args = list(set(args))
    for member in guild.members:
      if member.display_name in args:
        d = self.get_member_info(member)
        embed=self.format_member_info(d)
        await ctx.send(embed=embed)


async def setup(client):
  await client.add_cog(Information(client))
