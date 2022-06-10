from nextcord.ext import commands
from nextcord import Embed
import aiohttp

class Crypto(commands.Cog, name="Crypto Cog"):
    """Receives cryptocurrency related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='crypto', aliases=['c'])
    async def crypto(self, ctx: commands.Context, a:str):
        """Displays real time of specified cryptocurrency prices
        ```
        $c slp
        $crypto ETH
        ```
        """
        a = a.upper()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={a}USDT") as api:
                data = await api.json()
                symbol = data['symbol']
                price = data['price']
                em = Embed(title=f"{a}", description=f"{symbol} price is {price}")
                em.set_footer(text = ctx.author.name, icon_url = ctx.author.display_avatar)
                await ctx.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Crypto(bot))