from nextcord.ext import commands
from nextcord import Embed
import aiohttp

def formatNumber(num):
  if num % 1 == 0:
    return int(round(num,2))
  else:
    return round(num,2)


class Valorant(commands.Cog, name="Valorant Cog"):
    """Receives valorant related commands"""
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='valorant', aliases=['v'])
    async def valorant(self, ctx:commands.Context, a, *kwarg):
        """Displays valorant account level, rank, mmr
        ```
        $v jacc#lol
        $valorant jacc#lol
        ```
        """
        word = a
        tag_name = ''
        if len(kwarg) == 0:
            split_word = a.split('#')
            if ' ' in split_word[0]:
                user_name = split_word[0].replace(' ', '%20')
            else:
                user_name = split_word[0]
                tag_name = split_word[1]
        else:
            for element in kwarg:
                if '#' not in element:
                    word += ' ' + element
                    print(word)
                elif '#' in element:
                    if element[0] == "#":
                        split_word = element.replace('#', '')
                        tag_name = split_word
                    elif element[0] == " ":
                        split_word = element.split('#')
                        word += ' ' + split_word[0]
                        tag_name = split_word[1]
                    else:
                        split_word = element.split('#')
                        word += ' ' + split_word[0]
                        tag_name = split_word[1]
            user_name = word.replace(' ', '%20')

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v1/account/{user_name}/{tag_name}") as api:
                async with session.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{user_name}/{tag_name}") as api2:
                    data = await api.json()
                    data2 = await api2.json()
                    player_name = data["data"]["name"]
                    player_tag = data['data']['tag']
                    player_img = data['data']['card']['large']
                    valorant_level = data['data']['account_level']
                    rank = data2['data']['currenttierpatched']
                    elo = data2['data']['elo']

                    em = Embed(title=f"{player_name}#{player_tag}", description=f'*Account Level:* {valorant_level} \n *Rank:* {rank} \n *MMR:* {elo}')
                    em.set_image(url=player_img)
                    em.set_footer(text = ctx.author.name, icon_url = ctx.author.display_avatar)
                    await ctx.send(embed=em)
    
    @commands.command(name='match', describe="Gets all player's ranks of most recent finished match", aliases=['m'])
    async def match(self, ctx:commands.Context, a, *kwarg):
        """Displays most recent valorant game
        ```
        $m jacc#lol
        $match jacc#lol
        ```
        """
        word = a
        tag_name = ''
        if len(kwarg) == 0:
            split_word = a.split('#')
            if ' ' in split_word[0]:
                user_name = split_word[0].replace(' ', '%20')
            else:
                user_name = split_word[0]
                tag_name = split_word[1]
        else:
            for element in kwarg:
                if '#' not in element:
                    word += ' ' + element
                    print(word)
                elif '#' in element:
                    if element[0] == "#":
                        split_word = element.replace('#', '')
                        tag_name = split_word
                    elif element[0] == " ":
                        split_word = element.split('#')
                        word += ' ' + split_word[0]
                        tag_name = split_word[1]
                    else:
                        split_word = element.split('#')
                        word += ' ' + split_word[0]
                        tag_name = split_word[1]
            user_name = word.replace(' ', '%20')
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v3/matches/ap/{user_name}/{tag_name}") as api:
                data = await api.json()
                mapName = data['data'][0]['metadata']['map']
                redPlayerOneEmoji = ""
                redPlayerTwoEmoji = ""
                redPlayerThreeEmoji = ""
                redPlayerFourEmoji = ""
                redPlayerFiveEmoji = ""
                bluePlayerOneEmoji = ""
                bluePlayerTwoEmoji = ""
                bluePlayerThreeEmoji = ""
                bluePlayerFourEmoji = ""
                bluePlayerFiveEmoji = ""
                # 19
                emoji_list = [
                    '<:Jett:981179240219283486>', '<:Fade:981189331391762472>', '<:Astra:981196459452039208>', 
                    '<:Chamber:981197401610145822>','<:Skye:981197665335402496>', '<:Cypher:981201393484451840>', 
                    '<:Raze:981201651396403280>', '<:Sage:981197932315430922>', '<:Omen:981212904495906846>', 
                    '<:Reyna:981213151905341480>', '<:Viper:981213592437284935>', '<:Sova:981213989080035339>', 
                    '<:Killjoy:981214514953469982>', '<:Brimstone:981396624435736586>', '<:Kayo:981398370356699186>', 
                    '<:Yoru:981398892186857494>', '<:Breach:981399392558940241>', '<:Phoenix:981400329990070302>',
                    '<:Neon:982248325094989846>'
                            ]
                ########################### Red Team ###########################
                # Red Player One
                redPlayerOneName = data['data'][0]['players']['red'][0]['name']
                redPlayerOneTag = data['data'][0]['players']['red'][0]['tag']
                redPlayerOneLevel = data['data'][0]['players']['red'][0]['level']
                redPlayerOneCharacter = data['data'][0]['players']['red'][0]['character']

                redPlayerOneKills = data['data'][0]['players']['red'][0]['stats']['kills']
                redPlayerOneDeaths = data['data'][0]['players']['red'][0]['stats']['deaths']
                redPlayerOneAssists = data['data'][0]['players']['red'][0]['stats']['assists']
                redPlayerOneKDA = f'{redPlayerOneKills}/{redPlayerOneDeaths}/{redPlayerOneAssists}'

                redPlayerOneBodyshots = data['data'][0]['players']['red'][0]['stats']['bodyshots']
                redPlayerOneHeadshots = data['data'][0]['players']['red'][0]['stats']['headshots']
                redPlayerOneLegshots = data['data'][0]['players']['red'][0]['stats']['legshots']
                redPlayerOneHeadshotPercentage = round(int(redPlayerOneHeadshots)/(int(redPlayerOneHeadshots) + int(redPlayerOneBodyshots) + int(redPlayerOneLegshots)), 4)
                
                for i in range(len(emoji_list)):
                    if redPlayerOneCharacter in emoji_list[i]:
                        redPlayerOneEmoji = emoji_list[i]
                redPlayerOne = ""

                # Red Player Two
                redPlayerTwoName = data['data'][0]['players']['red'][1]['name']
                redPlayerTwoTag = data['data'][0]['players']['red'][1]['tag']
                redPlayerTwoLevel = data['data'][0]['players']['red'][1]['level']
                redPlayerTwoCharacter = data['data'][0]['players']['red'][1]['character']

                redPlayerTwoKills = data['data'][0]['players']['red'][1]['stats']['kills']
                redPlayerTwoDeaths = data['data'][0]['players']['red'][1]['stats']['deaths']
                redPlayerTwoAssists = data['data'][0]['players']['red'][1]['stats']['assists']
                redPlayerTwoKDA = f'{redPlayerTwoKills}/{redPlayerTwoDeaths}/{redPlayerTwoAssists}'

                redPlayerTwoBodyshots = data['data'][0]['players']['red'][1]['stats']['bodyshots']
                redPlayerTwoHeadshots = data['data'][0]['players']['red'][1]['stats']['headshots']
                redPlayerTwoLegshots = data['data'][0]['players']['red'][1]['stats']['legshots']
                redPlayerTwoHeadshotPercentage = round(int(redPlayerTwoHeadshots)/(int(redPlayerTwoHeadshots) + int(redPlayerTwoBodyshots) + int(redPlayerTwoLegshots)), 4)
                for i in range(len(emoji_list)):
                    if redPlayerTwoCharacter in emoji_list[i]:
                        redPlayerTwoEmoji = emoji_list[i]
                redPlayerTwo = ""

                # Red Player Three
                redPlayerThreeName = data['data'][0]['players']['red'][2]['name']
                redPlayerThreeTag = data['data'][0]['players']['red'][2]['tag']
                redPlayerThreeLevel = data['data'][0]['players']['red'][2]['level']
                redPlayerThreeCharacter = data['data'][0]['players']['red'][2]['character']

                redPlayerThreeKills = data['data'][0]['players']['red'][2]['stats']['kills']
                redPlayerThreeDeaths = data['data'][0]['players']['red'][2]['stats']['deaths']
                redPlayerThreeAssists = data['data'][0]['players']['red'][2]['stats']['assists']
                redPlayerThreeKDA = f'{redPlayerThreeKills}/{redPlayerThreeDeaths}/{redPlayerThreeAssists}'

                redPlayerThreeBodyshots = data['data'][0]['players']['red'][2]['stats']['bodyshots']
                redPlayerThreeHeadshots = data['data'][0]['players']['red'][2]['stats']['headshots']
                redPlayerThreeLegshots = data['data'][0]['players']['red'][2]['stats']['legshots']
                redPlayerThreeHeadshotPercentage = round(int(redPlayerThreeHeadshots)/(int(redPlayerThreeHeadshots) + int(redPlayerThreeBodyshots) + int(redPlayerThreeLegshots)), 4)
                for i in range(len(emoji_list)):
                    if redPlayerThreeCharacter in emoji_list[i]:
                        redPlayerThreeEmoji = emoji_list[i]
                redPlayerThree = ""

                # Red Player Four
                redPlayerFourName = data['data'][0]['players']['red'][3]['name']
                redPlayerFourTag = data['data'][0]['players']['red'][3]['tag']
                redPlayerFourLevel = data['data'][0]['players']['red'][3]['level']
                redPlayerFourCharacter = data['data'][0]['players']['red'][3]['character']

                redPlayerFourKills = data['data'][0]['players']['red'][3]['stats']['kills']
                redPlayerFourDeaths = data['data'][0]['players']['red'][3]['stats']['deaths']
                redPlayerFourAssists = data['data'][0]['players']['red'][3]['stats']['assists']
                redPlayerFourKDA = f'{redPlayerFourKills}/{redPlayerFourDeaths}/{redPlayerFourAssists}'

                redPlayerFourBodyshots = data['data'][0]['players']['red'][3]['stats']['bodyshots']
                redPlayerFourHeadshots = data['data'][0]['players']['red'][3]['stats']['headshots']
                redPlayerFourLegshots = data['data'][0]['players']['red'][3]['stats']['legshots']
                redPlayerFourHeadshotPercentage = round(int(redPlayerFourHeadshots)/(int(redPlayerFourHeadshots) + int(redPlayerFourBodyshots) + int(redPlayerFourLegshots)), 4)
                for i in range(len(emoji_list)):
                    if redPlayerFourCharacter in emoji_list[i]:
                        redPlayerFourEmoji = emoji_list[i]
                redPlayerFour = ""
                

                # Red Player Five
                redPlayerFiveName = data['data'][0]['players']['red'][4]['name']
                redPlayerFiveTag = data['data'][0]['players']['red'][4]['tag']
                redPlayerFiveLevel = data['data'][0]['players']['red'][4]['level']
                redPlayerFiveCharacter = data['data'][0]['players']['red'][4]['character']

                redPlayerFiveKills = data['data'][0]['players']['red'][4]['stats']['kills']
                redPlayerFiveDeaths = data['data'][0]['players']['red'][4]['stats']['deaths']
                redPlayerFiveAssists = data['data'][0]['players']['red'][4]['stats']['assists']
                redPlayerFiveKDA = f'{redPlayerFiveKills}/{redPlayerFiveDeaths}/{redPlayerFiveAssists}'

                redPlayerFiveBodyshots = data['data'][0]['players']['red'][4]['stats']['bodyshots']
                redPlayerFiveHeadshots = data['data'][0]['players']['red'][4]['stats']['headshots']
                redPlayerFiveLegshots = data['data'][0]['players']['red'][4]['stats']['legshots']
                redPlayerFiveHeadshotPercentage = round(int(redPlayerFiveHeadshots)/(int(redPlayerFiveHeadshots) + int(redPlayerFiveBodyshots) + int(redPlayerFiveLegshots)), 4)
                for i in range(len(emoji_list)):
                    if redPlayerFiveCharacter in emoji_list[i]:
                        redPlayerFiveEmoji = emoji_list[i]
                redPlayerFive = ""
                
                ########################### Blue Team ###########################
                # Blue Player One
                bluePlayerOneName = data['data'][0]['players']['blue'][0]['name']
                bluePlayerOneTag = data['data'][0]['players']['blue'][0]['tag']
                bluePlayerOneLevel = data['data'][0]['players']['blue'][0]['level']
                bluePlayerOneCharacter = data['data'][0]['players']['blue'][0]['character']

                bluePlayerOneKills = data['data'][0]['players']['blue'][0]['stats']['kills']
                bluePlayerOneDeaths = data['data'][0]['players']['blue'][0]['stats']['deaths']
                bluePlayerOneAssists = data['data'][0]['players']['blue'][0]['stats']['assists']
                bluePlayerOneKDA = f'{bluePlayerOneKills}/{bluePlayerOneDeaths}/{bluePlayerOneAssists}'

                bluePlayerOneBodyshots = data['data'][0]['players']['blue'][0]['stats']['bodyshots']
                bluePlayerOneHeadshots = data['data'][0]['players']['blue'][0]['stats']['headshots']
                bluePlayerOneLegshots = data['data'][0]['players']['blue'][0]['stats']['legshots']
                bluePlayerOneHeadshotPercentage = round(int(bluePlayerOneHeadshots)/(int(bluePlayerOneHeadshots) + int(bluePlayerOneBodyshots) + int(bluePlayerOneLegshots)), 4)
                for i in range(len(emoji_list)):
                    if bluePlayerOneCharacter in emoji_list[i]:
                        bluePlayerOneEmoji = emoji_list[i]
                
                bluePlayerOne = ""

                # Blue Player Two
                bluePlayerTwoName = data['data'][0]['players']['blue'][1]['name']
                bluePlayerTwoTag = data['data'][0]['players']['blue'][1]['tag']
                bluePlayerTwoLevel = data['data'][0]['players']['blue'][1]['level']
                bluePlayerTwoCharacter = data['data'][0]['players']['blue'][1]['character']

                bluePlayerTwoKills = data['data'][0]['players']['blue'][1]['stats']['kills']
                bluePlayerTwoDeaths = data['data'][0]['players']['blue'][1]['stats']['deaths']
                bluePlayerTwoAssists = data['data'][0]['players']['blue'][1]['stats']['assists']
                bluePlayerTwoKDA = f'{bluePlayerTwoKills}/{bluePlayerTwoDeaths}/{bluePlayerTwoAssists}'

                bluePlayerTwoBodyshots = data['data'][0]['players']['blue'][1]['stats']['bodyshots']
                bluePlayerTwoHeadshots = data['data'][0]['players']['blue'][1]['stats']['headshots']
                bluePlayerTwoLegshots = data['data'][0]['players']['blue'][1]['stats']['legshots']
                bluePlayerTwoHeadshotPercentage = round(int(bluePlayerTwoHeadshots)/(int(bluePlayerTwoHeadshots) + int(bluePlayerTwoBodyshots) + int(bluePlayerTwoLegshots)), 4)
                for i in range(len(emoji_list)):
                    if bluePlayerTwoCharacter in emoji_list[i]:
                        bluePlayerTwoEmoji = emoji_list[i]
                bluePlayerTwo = ""

                # Blue Player Three
                bluePlayerThreeName = data['data'][0]['players']['blue'][2]['name']
                bluePlayerThreeTag = data['data'][0]['players']['blue'][2]['tag']
                bluePlayerThreeLevel = data['data'][0]['players']['blue'][2]['level']
                bluePlayerThreeCharacter = data['data'][0]['players']['blue'][2]['character']

                bluePlayerThreeKills = data['data'][0]['players']['blue'][2]['stats']['kills']
                bluePlayerThreeDeaths = data['data'][0]['players']['blue'][2]['stats']['deaths']
                bluePlayerThreeAssists = data['data'][0]['players']['blue'][2]['stats']['assists']
                bluePlayerThreeKDA = f'{bluePlayerThreeKills}/{bluePlayerThreeDeaths}/{bluePlayerThreeAssists}'

                bluePlayerThreeBodyshots = data['data'][0]['players']['blue'][2]['stats']['bodyshots']
                bluePlayerThreeHeadshots = data['data'][0]['players']['blue'][2]['stats']['headshots']
                bluePlayerThreeLegshots = data['data'][0]['players']['blue'][2]['stats']['legshots']
                bluePlayerThreeHeadshotPercentage = round(int(bluePlayerThreeHeadshots)/(int(bluePlayerThreeHeadshots) + int(bluePlayerThreeBodyshots) + int(bluePlayerThreeLegshots)), 4)
                for i in range(len(emoji_list)):
                    if bluePlayerThreeCharacter in emoji_list[i]:
                        bluePlayerThreeEmoji = emoji_list[i]
                
                bluePlayerThree = ""

                # Blue Player Four
                bluePlayerFourName = data['data'][0]['players']['blue'][3]['name']
                bluePlayerFourTag = data['data'][0]['players']['blue'][3]['tag']
                bluePlayerFourLevel = data['data'][0]['players']['blue'][3]['level']
                bluePlayerFourCharacter = data['data'][0]['players']['blue'][3]['character']

                bluePlayerFourKills = data['data'][0]['players']['blue'][3]['stats']['kills']
                bluePlayerFourDeaths = data['data'][0]['players']['blue'][3]['stats']['deaths']
                bluePlayerFourAssists = data['data'][0]['players']['blue'][3]['stats']['assists']
                bluePlayerFourKDA = f'{bluePlayerFourKills}/{bluePlayerFourDeaths}/{bluePlayerFourAssists}'

                bluePlayerFourBodyshots = data['data'][0]['players']['blue'][3]['stats']['bodyshots']
                bluePlayerFourHeadshots = data['data'][0]['players']['blue'][3]['stats']['headshots']
                bluePlayerFourLegshots = data['data'][0]['players']['blue'][3]['stats']['legshots']
                bluePlayerFourHeadshotPercentage = round(int(bluePlayerFourHeadshots)/(int(bluePlayerFourHeadshots) + int(bluePlayerFourBodyshots) + int(bluePlayerFourLegshots)), 4)
                for i in range(len(emoji_list)):
                    if bluePlayerFourCharacter in emoji_list[i]:
                        bluePlayerFourEmoji = emoji_list[i]
                bluePlayerFour = ""

                # Blue Player One
                bluePlayerFiveName = data['data'][0]['players']['blue'][4]['name']
                bluePlayerFiveTag = data['data'][0]['players']['blue'][4]['tag']
                bluePlayerFiveLevel = data['data'][0]['players']['blue'][4]['level']
                bluePlayerFiveCharacter = data['data'][0]['players']['blue'][4]['character']

                bluePlayerFiveKills = data['data'][0]['players']['blue'][4]['stats']['kills']
                bluePlayerFiveDeaths = data['data'][0]['players']['blue'][4]['stats']['deaths']
                bluePlayerFiveAssists = data['data'][0]['players']['blue'][4]['stats']['assists']
                bluePlayerFiveKDA = f'{bluePlayerFiveKills}/{bluePlayerFiveDeaths}/{bluePlayerFiveAssists}'

                bluePlayerFiveBodyshots = data['data'][0]['players']['blue'][4]['stats']['bodyshots']
                bluePlayerFiveHeadshots = data['data'][0]['players']['blue'][4]['stats']['headshots']
                bluePlayerFiveLegshots = data['data'][0]['players']['blue'][4]['stats']['legshots']
                bluePlayerFiveHeadshotPercentage = round(int(bluePlayerFiveHeadshots)/(int(bluePlayerFiveHeadshots) + int(bluePlayerFiveBodyshots) + int(bluePlayerFiveLegshots)), 4)
                for i in range(len(emoji_list)):
                    i = int(i)
                    if bluePlayerFiveCharacter in emoji_list[i]:
                        bluePlayerFiveEmoji = emoji_list[i]
                bluePlayerFive = ""
                
                playerRanks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
                playerLevel = [redPlayerOneLevel, redPlayerTwoLevel, redPlayerThreeLevel, redPlayerFourLevel, redPlayerFiveLevel, bluePlayerOneLevel, bluePlayerTwoLevel, bluePlayerThreeLevel, bluePlayerFourLevel, bluePlayerFiveLevel]
                playerNames = [redPlayerOneName,redPlayerTwoName, redPlayerThreeName, redPlayerFourName, redPlayerFiveName, bluePlayerOneName, bluePlayerTwoName, bluePlayerThreeName, bluePlayerFourName, bluePlayerFiveName]
                playerCharacters = [redPlayerOneCharacter, redPlayerTwoCharacter, redPlayerThreeCharacter, redPlayerFourCharacter, redPlayerFiveCharacter, bluePlayerOneCharacter, bluePlayerTwoCharacter, bluePlayerThreeCharacter, bluePlayerFourCharacter, bluePlayerFiveCharacter]
                playerTags = [redPlayerOneTag, redPlayerTwoTag, redPlayerThreeTag, redPlayerFourTag, redPlayerFiveTag, bluePlayerOneTag, bluePlayerTwoTag, bluePlayerThreeTag, bluePlayerFourTag, bluePlayerFiveTag]
                playerData = [redPlayerOne, redPlayerTwo, redPlayerThree, redPlayerFour, redPlayerFive, bluePlayerOne, bluePlayerTwo, bluePlayerThree, bluePlayerFour, bluePlayerFive]
                playerKDA = [redPlayerOneKDA, redPlayerTwoKDA, redPlayerThreeKDA, redPlayerFourKDA, redPlayerFiveKDA, bluePlayerOneKDA, bluePlayerTwoKDA, bluePlayerThreeKDA, bluePlayerFourKDA, bluePlayerFiveKDA]
                playerHeadshotPercentage = [redPlayerOneHeadshotPercentage, redPlayerTwoHeadshotPercentage, redPlayerThreeHeadshotPercentage, redPlayerFourHeadshotPercentage, redPlayerFiveHeadshotPercentage, bluePlayerOneHeadshotPercentage, bluePlayerTwoHeadshotPercentage, bluePlayerThreeHeadshotPercentage, bluePlayerFourHeadshotPercentage, bluePlayerFiveHeadshotPercentage]
                playerEmojis = [redPlayerOneEmoji, redPlayerTwoEmoji, redPlayerThreeEmoji, redPlayerFourEmoji, redPlayerFiveEmoji, bluePlayerOneEmoji, bluePlayerTwoEmoji, bluePlayerThreeEmoji, bluePlayerFourEmoji, bluePlayerFiveEmoji]
                for one in range(len(playerNames)):
                    async with session.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{playerNames[one]}/{playerTags[one]}") as api2:
                        data2 = await api2.json()
                        rank = data2['data']['currenttierpatched']
                        elo = data2['data']['elo']
                        playerRanks[one] = rank
                        playerData[one] = f"{playerEmojis[one]}`{playerNames[one]}#{playerTags[one]}`\n *Level:* {playerLevel[one]}\n *Character:* {playerCharacters[one]}\n *Rank:* {playerRanks[one]}\n *MMR:* {elo}\n *KDA:* {playerKDA[one]}\n *Headshot Percentage:* {formatNumber(playerHeadshotPercentage[one] * 100)}%\n\n"


                em = Embed(title=f"{user_name}#{tag_name}'s {mapName}")
                em.add_field(name='Red Team', value=f'{playerData[0]}{playerData[1]}{playerData[2]}{playerData[3]}{playerData[4]}', inline=True)
                em.add_field(name='Blue Team', value=f'{playerData[5]}{playerData[6]}{playerData[7]}{playerData[8]}{playerData[9]}', inline=True)
                em.set_footer(text = ctx.author.name, icon_url = ctx.author.display_avatar)
                await ctx.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Valorant(bot))