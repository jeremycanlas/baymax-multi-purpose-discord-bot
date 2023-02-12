from nextcord.ext import commands
from nextcord import Embed
import nextcord
from azapi import AZlyrics
from youtube_dl import YoutubeDL
import baymax

class music_cog(commands.Cog, name="Music Cog"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = {}
        self.currently_playing = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

     #searching the item on youtube
    def search_yt(self, item, voice_channel):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title'], 'channel': voice_channel}

    def play_next(self, ctx):
        if len(self.music_queue[ctx.guild.id]) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[ctx.guild.id][0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue[ctx.guild.id].pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue[ctx.guild.id]) > 0:
            self.currently_playing = self.music_queue[ctx.guild.id][0][0]['title']
            self.is_playing = True

            m_url = self.music_queue[ctx.guild.id][0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            # voice = nextcord.utils.get(baymax.bot.voice_clients, guild=ctx.guild)
            # channel = ctx.author.voice.channel
            user = ctx.message.author
            vc = user.voice.channel
            if not vc.guild.voice_client in baymax.bot.voice_clients:
                # await vc.connect()
            # if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[ctx.guild.id][0][0]['channel'].connect()
                await ctx.voice_client.move_to(ctx.author.voice.channel)

                #in case we fail to connect
                # if self.vc == None:
                #     await ctx.send("Could not connect to the voice channel")
                #     return
            else:
                await self.vc.move_to(self.music_queue[ctx.guild.id][0][1])
            
            #remove the first element as you are currently playing it
            self.music_queue[ctx.guild.id].pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query, voice_channel)
            print("THIS IS SONG", song)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                em = Embed(title=None, description=f":musical_note: **{song['title']}** added to the queue")
                em.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar)
                await ctx.send(embed=em)
                #await ctx.send(f"{song['title']} added to the queue")
                try:
                    self.music_queue[ctx.guild.id].append([song])
                except:
                    self.music_queue[ctx.guild.id] = []
                    self.music_queue[ctx.guild.id].append([song])
                #self.music_queue[ctx.guild.id].append([song, voice_channel])
                print("THIS IS MUSIC_QUEUE",self.music_queue)

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)


    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue[ctx.guild.id])):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[ctx.guild.id][i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")
    @commands.command(name='test')
    async def test(self, ctx):
        
        print("ALL OF THE MUSIC QUEUE", self.music_queue)
        await ctx.send("test sent")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue[ctx.guild.id] = []
        await ctx.send("Music queue cleared")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
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
        # await interaction.send(self.music_queue)
        api = AZlyrics("google")
        if self.currently_playing == []:
            await interaction.send("No music is playing right now")
        else:
            api.title = self.currently_playing
            Lyrics = api.getLyrics()
            em = Embed(title=f"{api.title} by {api.artist}", description=Lyrics)
            em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
            await interaction.edit_original_message(embed=em)
def setup(bot: commands.Bot):
    bot.add_cog(music_cog(bot))