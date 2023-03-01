import discord
from discord.ext import commands
import requests
import os
import json


my_orange = 0xfc6203

api_key_twelve = os.environ['TWELVE_TOKEN']
api_key_cmc = os.environ['CMC_TOKEN']
url_cmc = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
request_dict = {'symbol': "BTC,ETH", 'convert': 'USD'}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '{0}'.format(api_key_cmc)
}
session = requests.Session()
session.headers.update(headers)

class Finance(commands.Cog):

  def __init__(self, client):
    self.client = client

  def crypto_info(self, ticker_list):
    arguments = ','.join(ticker_list)
    request_dict = {'symbol': f"{arguments}", 'convert': 'USD'}
    response = session.get(url=url_cmc, params=request_dict)
    response = json.loads(response.text)
    d = {}
    try:
      for el in ticker_list:
        d[str(el)] = response['data'][str(el)][0]['quote']['USD']['price']
    except KeyError:
      pass
    return d
  
  def format_crypto(self, d):
    res = ""
    for key in d.keys():
      res += f'{key} {d[key]:10.2f} USD\n'
    res = "```" + res + "```"
    return res
  
  @commands.command(
    name='crypto',
    description=
    'Displays info about given crypto symbols. By default displays data about BTC and ETH. Type symbols separated by a space'
  )
  async def crypto(self, ctx, *args):
    if len(args) == 0:
      args = ['BTC', 'ETH']
    d = self.crypto_info(args)
    if len(d) == 0:
      msg = 'Unable to retrive data. Please check the command syntax by typing \"$help crypto\" or check the spelling of crypto symbols'
    else:
      msg = self.format_crypto(d)
    embed = discord.Embed(title='Crypto', description=msg, color=my_orange)
    embed.set_thumbnail(url='https://www.pngall.com/wp-content/uploads/10/Dai-Crypto-Logo-PNG-HD-Image.png')
    embed.set_footer(text='Source: CoinMarketCap')
    await ctx.send(embed=embed)

  def get_stock_info(self, symbol):
    link = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=5min&apikey={api_key_twelve}&outputsize=1'
    response = json.loads(requests.get(link).text)
    try:
      return (float(response['values'][0]['high']) +
              float(response['values'][0]['low'])) / 2, float(
                response['values'][0]['open']), float(
                  response['values'][0]['close'])
    except KeyError:
      return None
  
  
  def format_stock_data(self, d):
    res = 'Values are in this order: avg, open, close\n\n'
    for key in d.keys():
      res += f'{key} {d[key][0]:^15.2f}{d[key][1]:^15.2f}{d[key][2]:^15.2f}\n'
    res = '```' + res + '```'
    return res
  
  
  @commands.command(
    description=
    'Displays info about given stock symbols. By default displays data about DJI, SPX and IXIC. Type tickers separated by a space'
  )
  async def stock(self, ctx, *args):
    d = {}
    if len(args) == 0:
      args = ["DJI", 'SPX', 'IXIC']
    for el in args:
      response = self.get_stock_info(str(el))
      if response == None:
        await ctx.send(
          f'Unable to retrieve data for \"{el}\" symbol. Please check the spelling or type \"$help stock\" for information about this command'
        )
        return
      else:
        d[el] = self.get_stock_info(str(el))
    msg = self.format_stock_data(d)
    embed = discord.Embed(title='Stocks', description=msg, color=my_orange)
    embed.set_footer(text='Source: TwelveData')
    embed.set_thumbnail(url='https://upstox.com/app/themes/upstox/dist/img/home/new/grow-stock.png')
    await ctx.send(embed=embed)

async def setup(client):
  await client.add_cog(Finance(client))