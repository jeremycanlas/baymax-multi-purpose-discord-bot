from nextcord.ext import commands
from nextcord import Embed, Colour
from azapi import AZlyrics

class Song(commands.Cog, name="Song Cog"):
    """Receives song related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='lyrics',aliases=['l'])
    async def lyrics(self, ctx: commands.Context, *args:str):
        """Displays lyrics
        ```
        $lyrics nasty
        $l reel it in
        $lyrics nasty ariana
        ```
        """
        song_query = " ".join(args[:])
        api = AZlyrics("google")
        api.title = song_query
        Lyrics = api.getLyrics()
        em = Embed(title=f"{api.title} by {api.artist}", description=Lyrics, color = Colour.random())
        em.set_footer(text = ctx.author.name, icon_url = ctx.author.display_avatar)
        await ctx.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Song(bot))