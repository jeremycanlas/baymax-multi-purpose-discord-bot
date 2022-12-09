from nextcord.ext import commands
from nextcord import Embed
import nextcord
import aiohttp

class Crypto(commands.Cog, name="Crypto Cog"):
    """Receives cryptocurrency related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name='crypto')
    async def crypto(self, interaction: nextcord.Interaction, symbol:str):
        """Displays real time of specified cryptocurrency prices
        ```
        $c slp
        $crypto ETH
        ```
        
        Parameters
        ----------
        interaction: Interaction
            The interaction object
        symbol: str
            the crypto currency symbol
            ex:
            eth, ETH, btc, BTC
        """
        symbol = symbol.upper()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT") as api:
                data = await api.json()
                crypto_symbol = data['symbol']
                price = data['price']
                em = Embed(title=f"{symbol}", description=f"{crypto_symbol} price is {price}")
                em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
                await interaction.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Crypto(bot))