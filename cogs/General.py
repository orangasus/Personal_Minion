import discord
from discord.ext import commands
import json
import requests
import os
import random
import logging


class General(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.rapid_api_key = os.environ['RAPID_TOKEN']

  @commands.command(
  description='Greets in response using author\'s name to address her/him/them'
  )
  async def hi(self, ctx):  # ctx - context
    nickname = ctx.message.author.name
    msg = f'Hello, master {nickname}'
    await ctx.send(msg)

  def get_stoic_quote_random(self):
    response = requests.get("https://stoicquotesapi.com/v1/api/quotes/random")
    json_data = dict(json.loads(response.text))
    quote = json_data['body']
    author = json_data['author']
    return quote, author

  def get_format_stoic_quote(self):
    q, a = self.get_stoic_quote_random()
    q = q[:len(q) - 1]
    msg = f"_\"{q}\" - {a}_"
    return msg
  
  @commands.command(description='Displays a random stoic quote', name='stoic')
  async def stoic(self, ctx):
    await ctx.send(self.get_format_stoic_quote())

  def get_bad_joke(self):
    url = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"
    headers = {
      "X-RapidAPI-Key": self.rapid_api_key,
      "X-RapidAPI-Host": "jokes-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    return data[0]['joke']

  @commands.command(description='Displays a random joke')
  async def break_ice(self, ctx):
    msg = '_' + self.get_bad_joke() + '_'
    await ctx.send(msg)

  def roll_a_dice(self, number, value):
    l = []
    for i in range(number):
      l.append(str(random.randint(1, value + 1)))
    return l

  def format_dice_data(self, d):
    res = ''
    for k in d.keys():
      res += f"{k:5} -->   "
      rolls = ', '.join(d[k])
      res += rolls + '\n'
    res = '```' + res + '```'
    return res

  @commands.command(
    description=
    'Rolls specified number of specified dice. Rolls 1d20 by default. Syntax: $dice <number of dice>d<value of dice>. Example: $dice 2d20 1d10 1d10 5d5'
  )
  async def dice(self, ctx, *args):
    if len(args) == 0:
      args = ['1d20']
    res = {}
    for el in args:
      try:
        num, val = map(int, el.split('d'))
        if num <= 0 or val <= 0:
          raise ValueError
      except:
        await ctx.send(
          f'Unable to roll this dice: \"{el}\". Check for spelling errors or type \"$help dice\" for info about this command'
        )
        return
      else:
        if f'd{val}' in res.keys():
          res[f'd{val}'].extend(self.roll_a_dice(num, val))
        else:
          res[f'd{val}'] = self.roll_a_dice(num, val)
    await ctx.send(self.format_dice_data(res))

async def setup(client):
  await client.add_cog(General(client))