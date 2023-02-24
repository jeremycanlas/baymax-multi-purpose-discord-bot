import nextcord
from nextcord.ext import commands
from nextcord import Embed
from azapi import AZlyrics
import yt_dlp

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = {}
        self.is_paused = {}
        self.currently_playing = {}
        self.is_bot_connected = {}

        self.music_queue = {}
        self.YDL_OPTIONS = {'format': 'm4a/bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a',}]}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
    def search_yt(self, item):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][3]['url'], 'title': info['title']}
    
    def play_next(self, ctx):
        if len(self.music_queue[ctx.guild.id]) > 0:
            self.is_playing[ctx.guild.id] = True

            m_url = self.music_queue[ctx.guild.id][0][0]['source']

            self.music_queue[ctx.guild.id].pop(0)
            self.currently_playing[ctx.guild.id].pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
        else:
            self.is_playing[ctx.guild.id] = False
    async def play_music(self, ctx):
        if len(self.music_queue[ctx.guild.id]) > 0:
            self.is_playing[ctx.guild.id] = True
            m_url = self.music_queue[ctx.guild.id][0][0]['source']
            voice_client = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            if self.vc == None or not voice_client:
                self.vc = await self.music_queue[ctx.guild.id][0][1].connect()
                print("passing through here")

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[ctx.guild.id][0][1])

            self.music_queue[ctx.guild.id].pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
        else:
            self.is_playing[ctx.guild.id] = False
    
    @commands.command(name="play", aliases=['p','playing'], help="Play the selected song from youtube")
    async def play(self, ctx, *args):
        if ctx.guild.id in self.music_queue:
            pass
        else:
            self.music_queue[ctx.guild.id] = []
            self.is_playing[ctx.guild.id] = False
            self.is_paused[ctx.guild.id] = False
            self.currently_playing[ctx.guild.id] = []
        query = " ".join(args)

        voice_channel = ctx.message.author.voice.channel if ctx.message.author.voice else None
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused[ctx.guild.id]:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format, try a different keyword")
            else:
                # await ctx.send("Song added to the queue")
                em = Embed(title=None, description=f":musical_note: **{song['title']}** added to the queue")
                em.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar)
                await ctx.send(embed=em)
                self.currently_playing[ctx.guild.id].append([query, song['title']])
                self.music_queue[ctx.guild.id].append([song, voice_channel])

                if self.is_playing[ctx.guild.id] == False:
                    await self.play_music(ctx)
                    
    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing[ctx.guild.id]:
            self.is_playing[ctx.guild.id] = False
            self.is_paused[ctx.guild.id] = True
            self.vc.pause()
        elif self.is_paused[ctx.guild.id]:
            self.vc.resume()
            
    @commands.command(name="resume", aliases=["r"], help="Resumes playing the current song")
    async def resume(self, ctx, *args):
        if self.is_paused[ctx.guild.id]:
            self.is_playing[ctx.guild.id] = True
            self.is_paused[ctx.guild.id] = False
            self.vc.resume()
            
    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            # await self.play_music(ctx)
            
    @commands.command(name="queue", aliases=["q"], help="Displays all the songs currently in the queue")
    async def queue(self, ctx):
        retval = ""
        
        for i in range(0, len(self.music_queue[ctx.guild.id])):
            retval += f"**{i+1}. **" + self.music_queue[ctx.guild.id][i][0]['title'] + '\n'
            
        if retval != "" or self.currently_playing[ctx.guild.id][0][1]:
            em = Embed(title=f"**Music Queue | {ctx.guild.name}**", description=f"**Now Playing:** {self.currently_playing[ctx.guild.id][0][1]}" +'\n' + retval)
            em.set_thumbnail(url=ctx.guild.icon.url)
            em.set_footer(text = ctx.author.name, icon_url = ctx.author.display_avatar)
            await ctx.send(embed=em)
            # await ctx.send(retval)
        else:
            await ctx.send("No music in the queue.")
            
    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the current song and clears the queue")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing[ctx.guild.id]:
            self.vc.stop()
        self.music_queue[ctx.guild.id] = []
        await ctx.send("Music queue cleared")
    
    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from the voice channel")
    async def leave(self, ctx):
        self.is_playing[ctx.guild.id] = False
        self.is_paused[ctx.guild.id] = False
        await self.vc.disconnect()
    
    @commands.command(name="lyrics", help="Displays the lyrics of the currently playing song")
    async def lyrics(self, ctx):
        api = AZlyrics("google")
        if self.currently_playing[ctx.guild.id] == []:
            await ctx.send("No music is playing right now")
        else:
            for elem in self.currently_playing[ctx.guild.id][0]:
                print("this is elem: ",elem)
                print("this is currently playing: ", self.currently_playing[ctx.guild.id])
                api.title = elem
                print("this is api.title: ", api.title)
                Lyrics = api.getLyrics()
                print(Lyrics)
                print(type(Lyrics))
                if type(Lyrics) == str:
                    em = Embed(title=f"{api.title} by {api.artist}", description=Lyrics)
                    em.set_footer(text = ctx.author.name, icon_url = ctx.author.display_avatar)
                    em.set_thumbnail(url=ctx.guild.icon)
                    await ctx.send(embed=em)
                    break
            if type(Lyrics) == int:
                await ctx.send("Could not find lyrics, try /lyrics song")
    
    @nextcord.slash_command(name='lyric', description='display current song\'s lyrics')
    async def lyric(self, interaction: nextcord.Interaction):
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
        if self.currently_playing[interaction.guild.id] == []:
            await interaction.send("No music is playing right now")
        else:
            for elem in self.currently_playing[interaction.guild.id][0]:
                print("this is elem: ",elem)
                print("this is currently playing: ", self.currently_playing[interaction.guild.id])
                api.title = elem
                print("this is api.title: ", api.title)
                Lyrics = api.getLyrics()
                print(Lyrics)
                print(type(Lyrics))
                if type(Lyrics) == str:
                    em = Embed(title=f"{api.title} by {api.artist}", description=Lyrics)
                    em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
                    em.set_thumbnail(url=interaction.guild.icon)
                    await interaction.edit_original_message(embed=em)
                    break
            if type(Lyrics) == int:
                await interaction.send("Could not find lyrics, try /lyrics song")
def setup(bot: commands.Bot):
    bot.add_cog(music_cog(bot))