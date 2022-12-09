from nextcord.ext import commands
from nextcord import Embed
import nextcord
import aiohttp

class Dog(commands.Cog, name="Dog"):
    """Receives dog related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name='dog')
    async def dog(self, interaction: nextcord.Interaction):
        """Displays random dog photo
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://dog.ceo/api/breeds/image/random") as api:
                data = await api.json()
                photo = data['message']
                em = Embed()
                em.set_image(url=photo)
                em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
                await interaction.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Dog(bot))