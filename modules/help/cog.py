from nextcord.ext import commands
from .help_commands import MyHelpCommand

class HelpCog(commands.Cog, name="Help"):
    """"Shows help info about commands"""
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))