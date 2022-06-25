# baymax-multi-purpose-discord-bot
Inspired by the movie character Baymax from Big Hero 6, Baymax is a task-oriented chat bot that responds to certain keywords in any text channel of the discord server.

He is built with Python using the nextcord library and is currently hosted in a virtual machine in Google Cloud.

Baymax can display Valorant data of users using a valorant API using the $valorant for player data and $match for player's recent match data.

The discord bot also utilizes the Binance API to get real time data of specified cryptocurrency using $crypto "SYMBOL" as well as getting song lyrics with $lyrics.

Try saying hi to baymax

Functions
$valorant username#tagname ($v) - gets user's level and rank
$match username#tagname ($m) -Gets all player's ranks of most recent finished match
$inspire - sends random inspirational quotes, also automatically replies if Baymax detects sad words in chat
$crypto "BTC" - gets real time price of specified cryptocurrency
$lyrics "song name and/or song artist" - gets the lyrics of specified song
$join - Baymax joins voice channel of message author
$leave - Baymax leaves voice channel
