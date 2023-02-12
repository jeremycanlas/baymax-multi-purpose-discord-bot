import nextcord
from nextcord.ext import commands
from nextcord import Embed
import aiohttp

def formatNumber(num):
  if num % 1 == 0:
    return int(round(num,2))
  else:
    return round(num,2)

emoji_list = [
                '<:Jett:981179240219283486>', '<:Fade:981189331391762472>', '<:Astra:981196459452039208>', 
                '<:Chamber:981197401610145822>','<:Skye:981197665335402496>', '<:Cypher:981201393484451840>', 
                '<:Raze:981201651396403280>', '<:Sage:981197932315430922>', '<:Omen:981212904495906846>', 
                '<:Reyna:981213151905341480>', '<:Viper:981213592437284935>', '<:Sova:981213989080035339>', 
                '<:Killjoy:981214514953469982>', '<:Brimstone:981396624435736586>', '<:Kayo:981398370356699186>', 
                '<:Yoru:981398892186857494>', '<:Breach:981399392558940241>', '<:Phoenix:981400329990070302>',
                '<:Neon:982248325094989846>', "<:Harbor:1050390110471999489>"
            ]
rank_list = [
                "<:Iron_1:1050391647722164284>", "<:Iron_2:1050391678659330069>", "<:Iron_3:1050391695839199242>",
                "<:Bronze_1:1050392486809456650>", "<:Bronze_2:1050392498662543400>", "<:Bronze_3:1050392508775006228>", 
                "<:Silver_1:1050392525564825701>", "<:Silver_2:1050392536113483847>", "<:Silver_3:1050392547765268570>",
                "<:Gold_1:1050392559609991198>", "<:Gold_2:1050392569428840488>", "<:Gold_3:1050392583706263552>",
                "<:Platinum_1:1050392608456855573>", "<:Platinum_2:1050392618124713994>", "<:Platinum_3:1050392628107157586>", 
                "<:Diamond_1:1050392645291225109>", "<:Diamond_2:1050392657526009926>", "<:Diamond_3:1050392668460560414>", 
                "<:Ascendant_1:1050392688421249064>", "<:Ascendant_2:1050392697434820678>", "<:Ascendant_3:1050392706775527505>",
                "<:Immortal_1:1050392717605224508>", "<:Immortal_2:1050392727742849064>", "<:Immortal_3:1050392747653206016>",
                "<:Radiant:1050392767882342410>"
            ]

class Valorant(commands.Cog, name="Valorant Cog"):
    """Receives valorant related commands"""
    def __int__(self, bot: commands.Bot):
        self.bot = bot
    
    @nextcord.slash_command(name='valorant')
    async def valorant(self, interaction:nextcord.Interaction, username, tag):
        """Displays valorant player level and rank

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    username: str
        Valorant username
        ex:
        abc
    tag: str
        Valorant user tag
        ex:
        1234
    """
        await interaction.response.defer()
        if ' ' in username:
            username = username.replace(' ', '%20')
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}") as api:
                async with session.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{username}/{tag}") as api2:
                    data = await api.json()
                    data2 = await api2.json()
                    player_name = data["data"]["name"]
                    player_tag = data['data']['tag']
                    player_img = data['data']['card']['large']
                    valorant_level = data['data']['account_level']
                    rank = data2['data']['currenttierpatched']
                    elo = data2['data']['elo']
                    rank = rank.replace(" ", "_")
                    for elem in range(len(rank_list)):
                        if rank in rank_list[elem]:
                            rank = rank_list[elem]
                    em = Embed(title=f"{player_name}#{player_tag}", description=f'*Account Level:* {valorant_level} \n *Rank:* {rank} \n *MMR:* {elo}')
                    em.set_image(url=player_img)
                    em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
                    await interaction.edit_original_message(embed=em)

    @nextcord.slash_command(name='match', description="Gets all player's ranks of most recent finished match")
    async def match(self, interaction: nextcord.Interaction, username, tag):
        """Gets all player's ranks of most recent finished valorant match

        Parameters
        ----------
        interaction: Interaction
            The interaction object
        username: str
            Valorant username
            ex:
            abc
        tag: str
            Valorant user tag
            ex:
            1234
        """
        await interaction.response.defer()
        if ' ' in username:
            username = username.replace(' ', '%20')
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v3/matches/ap/{username}/{tag}") as api:
                data = await api.json()
                mapName = data['data'][0]['metadata']['map']
                gameMode = data['data'][0]['metadata']['mode']
                # Initialize Variable Lists
                redPlayerName = []
                redPlayerTag = []
                redPlayerLevel = []
                redPlayerCharacter = []
                redPlayerKDA = []
                redPlayerHSP = []                
                bluePlayerName = []
                bluePlayerTag = []
                bluePlayerLevel = []
                bluePlayerCharacter = []
                bluePlayerKDA = []
                bluePlayerHSP = []  
                #     print('True')
                for elem in range(10):
                    if data['data'][0]['players']['all_players'][elem]['team'] == 'Red':
                        redPlayerName.append(data['data'][0]['players']['all_players'][elem]['name'])
                        redPlayerTag.append(data['data'][0]['players']['all_players'][elem]['tag'])
                        redPlayerLevel.append(data['data'][0]['players']['all_players'][elem]['level'])
                        redPlayerCharacter.append(data['data'][0]['players']['all_players'][elem]['character'])
                        redPlayerKDA.append(f"{data['data'][0]['players']['all_players'][elem]['stats']['kills']}/{data['data'][0]['players']['all_players'][elem]['stats']['deaths']}/{data['data'][0]['players']['all_players'][elem]['stats']['assists']}")
                        redPlayerHeadshot =  data['data'][0]['players']['all_players'][elem]['stats']['headshots']
                        redPlayerBodyshot = data['data'][0]['players']['all_players'][elem]['stats']['bodyshots']
                        redPlayerLegshot = data['data'][0]['players']['all_players'][elem]['stats']['legshots']
                        redPlayerHeadshotPercentage = redPlayerHeadshot / (redPlayerBodyshot + redPlayerLegshot)
                        redPlayerHSP.append(f"{formatNumber(redPlayerHeadshotPercentage * 100)}%")
                    if data['data'][0]['players']['all_players'][elem]['team'] == 'Blue':
                        bluePlayerName.append(data['data'][0]['players']['all_players'][elem]['name'])
                        bluePlayerTag.append(data['data'][0]['players']['all_players'][elem]['tag'])
                        bluePlayerLevel.append(data['data'][0]['players']['all_players'][elem]['level'])
                        bluePlayerCharacter.append(data['data'][0]['players']['all_players'][elem]['character'])
                        bluePlayerKDA.append(f"{data['data'][0]['players']['all_players'][elem]['stats']['kills']}/{data['data'][0]['players']['all_players'][elem]['stats']['deaths']}/{data['data'][0]['players']['all_players'][elem]['stats']['assists']}")
                        bluePlayerHeadshot =  data['data'][0]['players']['all_players'][elem]['stats']['headshots']
                        bluePlayerBodyshot = data['data'][0]['players']['all_players'][elem]['stats']['bodyshots']
                        bluePlayerLegshot = data['data'][0]['players']['all_players'][elem]['stats']['legshots']
                        bluePlayerHeadshotPercentage = bluePlayerHeadshot / (bluePlayerBodyshot + bluePlayerLegshot)
                        bluePlayerHSP.append(f"{formatNumber(bluePlayerHeadshotPercentage * 100)}%")
                playerNames = redPlayerName + bluePlayerName
                playerTags = redPlayerTag + bluePlayerTag
                playerLevels = redPlayerLevel + bluePlayerLevel
                playerCharacters = redPlayerCharacter + bluePlayerCharacter
                playerKDAs = redPlayerKDA + bluePlayerKDA
                playerHSPs = redPlayerHSP + bluePlayerHSP
                playerEmojis = playerCharacters.copy()
                for i in range(len(playerCharacters)):
                    for elem in range(len(emoji_list)):
                        if playerCharacters[i] in emoji_list[elem]:
                            playerEmojis[i] = emoji_list[elem]
                # Initialize variable list to be used while looping through individual player data
                playerRanks = list(range(10))
                playerEmojiRanks = list(range(10))
                playerElos = list(range(10))
                playerData = list(range(10))
                rank = list(range(10))
                for one in range(len(playerNames)):
                    async with session.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{playerNames[one]}/{playerTags[one]}") as api2:
                        data2 = await api2.json()
                        rank = data2['data']['currenttierpatched']
                        elo = data2['data']['elo']
                        playerRanks[one] = rank
                        if rank != None:
                            playerEmojiRanks[one] = rank.replace(" ", "_")
                            for elem in range(len(rank_list)):
                                if playerEmojiRanks[one] in rank_list[elem]:
                                    playerEmojiRanks[one] = rank_list[elem]
                        else:
                            playerEmojiRanks[one] = "Unranked"
                        playerElos[one] = elo
                        playerData[one] = f"{playerEmojis[one]}`{playerNames[one]}#{playerTags[one]}`\n *Level:* {playerLevels[one]}\n *Character:* {playerCharacters[one]}\n *Rank:* {playerEmojiRanks[one]}\n *MMR:* {playerElos[one]}\n *KDA:* {playerKDAs[one]}\n *Headshot Percentage:* {playerHSPs[one]}\n\n"
                em = Embed(title=f"{username}#{tag}'s {mapName} {gameMode}")
                em.add_field(name='Red Team', value=f'{playerData[0]}{playerData[1]}{playerData[2]}{playerData[3]}{playerData[4]}', inline=True)
                em.add_field(name='Blue Team', value=f'{playerData[5]}{playerData[6]}{playerData[7]}{playerData[8]}{playerData[9]}', inline=True)
                em.set_footer(text = interaction.user.name, icon_url = interaction.user.display_avatar)
                await interaction.edit_original_message(embed=em)

    
def setup(bot: commands.Bot):
    bot.add_cog(Valorant(bot))