from nextcord.ext import commands
from nextcord import Embed
import nextcord
import aiohttp
import random

class Animal(commands.Cog, name="Animal"):
    """Receives dog related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name='animal')
    async def animal(self, interaction: nextcord.Interaction):
        """Displays random animal photo
        """
        animal_api = [
            "https://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true",
            "https://shibe.online/api/cats?count=1&urls=true&httpsUrls=true",
            "https://shibe.online/api/birds?count=1&urls=true&httpsUrls=true", 
            "https://aws.random.cat/meow", 
            "https://random-d.uk/api/v2/random", 
            "https://randomfox.ca/floof/"
            ]
        async with aiohttp.ClientSession() as session:
            select_random_api = random.choice(animal_api)
            async with session.get(select_random_api) as api:
                if select_random_api == animal_api[0] or select_random_api == animal_api[1] or select_random_api == animal_api[2]:
                    data = await api.json()
                    print(select_random_api)
                    print(data)
                    photo = data[0]
                elif select_random_api == animal_api[3]:
                    data = await api.json()
                    photo = data['file']
                elif select_random_api == animal_api[4]:
                    data = await api.json()
                    photo = data['url']
                elif select_random_api == animal_api[5]:
                    data = await api.json()
                    photo = data['image']
                em = Embed()
                em.set_image(url=photo)
                em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
                await interaction.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Animal(bot))