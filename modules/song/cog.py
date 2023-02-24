from nextcord.ext import commands
from nextcord import Embed, Colour
from nextcord import Interaction, SlashOption, ChannelType, User
from nextcord.abc import GuildChannel
from azapi import AZlyrics
import os
import nextcord

class Song(commands.Cog, name="Song Cog"):
    """Receives song related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name='lyrics', description='find lyrics')
    async def lyrics(self, interaction: nextcord.Interaction, song_query:str):
        """Displays lyrics

        Parameters
        ----------
        interaction: Interaction
            The interaction object
        song_query: str
            song title with or without the song artist
        """
        await interaction.response.defer()
        api = AZlyrics("google")
        api.title = song_query
        Lyrics = api.getLyrics()
        em = Embed(title=f"{api.title} by {api.artist}", description=Lyrics, color = Colour.random())
        em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
        await interaction.edit_original_message(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Song(bot))