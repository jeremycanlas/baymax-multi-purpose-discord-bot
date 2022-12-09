from nextcord.ext import commands
from nextcord import Embed
import nextcord
import aiohttp

class Quote(commands.Cog, name="Quote"):
    """Receives quote related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name='quote')
    async def quote(self, interaction: nextcord.Interaction):
        """Displays a random quote
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.themotivate365.com/stoic-quote") as api:
                data = await api.json()
                author = data["author"]
                quote = data["quote"]
                await interaction.send(f"{quote} - {author}")
    @nextcord.slash_command(name='fact')
    async def fact(self, interaction: nextcord.Interaction):
        """Displays a random fact
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://uselessfacts.jsph.pl/random.json") as api:
                data = await api.json()
                author = data["source"]
                quote = data["text"]
                await interaction.send(f"{quote} - {author}")
def setup(bot: commands.Bot):
    bot.add_cog(Quote(bot))