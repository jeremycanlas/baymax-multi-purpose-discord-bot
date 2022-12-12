from nextcord.ext import commands
from nextcord import Embed, Colour
from nextcord import Interaction, SlashOption, ChannelType, User
from nextcord.abc import GuildChannel
from azapi import AZlyrics
import os
import nextcord
from revChatGPT.revChatGPT import Chatbot

config = {
    "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..eQ8KTItT-R5IeiRz.xDzlCo3RkMcRp5grMN_NKQSkTOOxmFYtb0FZs3IY3EaxA_IkTfhIPyNiWvpSrBGLosuSo5VlH9ve-zRTSbIZ1eet0x2R4yUbiGixEDONK4Z01Z_VFoL9D5qfK7V7fA-M78Jt59cz-3AoFrA1J1m7NklQB9jGoxkguemC5qHSWTEya0xLR4UxSoD0WE8AkMWgiCrk81YZ1DPEQ4Vv5WxiSDJytZcB1ZebP75t9YspLhO0_LtokweI5PDHh42wJ2uCcB1rbm_vTMPjcu5LUgvn8KzuSf7BJXunGpxTP_wzrWjwyHutT1RR_Ew0MTKErYKI79Xrqxig_Cv9EDCQfv00vbYdFh4ZOKvRfByQUtbHRAPcoWeoixRMI68mn-0vhlVNLEX-2ssfr9iBurhHFShazZUQ9_7gfq7Po5-UPiTYEKkOdjr17oYiM3QYqJBPXkZyE5xD0So5MehCsUf3iWaq1RWOGIr3WO2Id45At9OLwdD54nLrYfQWXSlfppo538glSZzmpygUg6_nnPxB-pnrh5SvO7Jiit0TzTTg_e9wEfE7vrWfg2ZyGltjaXiVzuJfEq5doVgoZH1PO6gmk2asH2PGBfIuEV7l4GjtzCssF4L8A4E_Kdd3xi03PdV98ngJaeXEewgwQ2w2hou_tpyEsWoHN8y3YJKjAbPFx9JbMY7mFSqNOkRIZNlb0DAYf2u8yBxbKpxqDUs_WWdAKI-HqMsRgMSbRBl7JlRFPdEjLYaCCFRmwT6F3b7nEt9RS48YVvxNaZFfzAUdya344SPBJ5w-cFd9BHcbo4Tdtwp4IEljwTBpGtBXfCV7K62_rBPJGzpnc-5KOvKaZKdKmH5MuEac7k4BpV20tmgsUImc5B--i5ndSuMcS3tSTTvNNbKoIkIRo-DCfBJ0OKVri9E1_-1OU0SA4OczB47sNatzYTMe206MGWn3odOgjc4BsDm1I3vCSzXO_0MosLWNVI9zTaHF9P6SyrQF6kL4tDqjQ296-IcbhQTdHQyI0oSdpOENgkqKhAXA54fnySwm02XrVG5mG_wpGS72p9S6i3CqZPxS3GOIQgFpDbRs-NwnGtccKw8B-5AgfaIZqGaNbnx-CGEy4UZv8zGSRpSyv1KtzxDmQGXM-m3RwU6xXNhvd3qeEpkV13v7hTwpr2QsOPNy9vpEOz8w4xrOHIl2EIaRj27kEcJRVe2FcqwL8l5JmAHwpI9w1YCOdXXgudVxrZe97zEygGVC53isW8AW4v4h8CUzsgk5iIcEua1gQot_5rYImNE13iBMTdWOTTeVEC0OPV9NnlDDym4pzCw_a3bKf6m0qmc8XAzj6G8m6xv6hpqj8EDbQZv3JfQzgWlyG8fS7UH9xanCHfso5ApgFce3zOLd22cM7cgNqbxrEJpR6QXCkmqRWZsjElyrnLWA_pFz3-oBmZ67ayfdsdNp33o1HbwySgofW6VwX0n7gSuCMpORzVH5S90OnYywXZcI5Hsqq8pXG6xCi0s1pubki1fk1s5KgiJIUM-Y7AM9TWPKBZ-p5DucQMSZYkHBSQmLTBZDsRp_X5-0KddRPAOEi3yHUwSaOP-Ve_u51zFCvVuzP-KuG9ojf9mzGNYkbgnWOLofmRuhqSbEwhPXtmsunSzEmWLg82gTIaI1MK_Y23ljWRCuMXVdWat3kvDJV_KJS1yDHmzaOreuRZHL83QdSPTdWCJPChZpeCZRZg7dprhmZcrd4Ug8XKXF140ifH8fiKU6qkAKQ4RHrzcTvm1dK61eDUtYpCj83QouUKOLRoTEa91mVgGms0fdMa3GK7bar3Neh_Z6qI-_adCBSMrg_2bJBSNhHEvBULoDbTIxKcpMwked1VSplcHMxKEMViYrYKQTs8ffCfZMjkv_kms5hklp6uqOqYLKFPpyZxmmFtF-4Ku7g_RDiZpOTR8Cr70TqN_jzjGxX6J2l2OR2Rq0Qjs4OYta0fQ5eUHt8Ho063S--_DRSaUgNdNCFOvSkRd-LzpKWdj6G3gv_-V7eCsLxf69ESBxNE6TK3_8qkH0AlecqXNWjeHHyKD3-NSXBQDX-ImdeiEXBCwSjoMumLQe-czKfC1nLIlny_T1BhOrPxBLc7_XdG3BrstDRsTcAZNBbQORxEs3v3Ucy_y2jFDWGbOLnUsdX6Po5r4rf2VAJdfPJv6NEfNGZ3rOCakevMIob83IjIdyDLndD3WbOGJa7CBTYJx4BPumAQo8yAxtuGbU5Hym2hQkBcwwvXEMDSzQ9Z71A8DNht40.X0oUkq0S7v5yL9Bu6b-YmQ" # Deprecated. Use only if you encounter captcha with email/password
}

class ChatGPT(commands.Cog, name="ChatGPT cog"):
    """Receives ChatGPT related commands"""

    def __int__(self, bot: commands.Bot):
        self.bot = bot
    
    @nextcord.slash_command(name='chatgpt')
    async def chatgpt(self, interaction: nextcord.Interaction, prompt:str):
        """Ask anything to OpenAI's chatgpt language model
        
            Parameters
            ----------
            interaction: Interaction
                The interaction object
            prompt: str
                Ask the AI anything
        """
        await interaction.response.defer()
        chatbot = Chatbot(config, conversation_id=None)
        chatbot.refresh_session()
        message = chatbot.get_chat_response(prompt)["message"]
        await interaction.send(f"{interaction.user.name}: '{prompt}'\n\n{message}")

def setup(bot: commands.Bot):
    bot.add_cog(ChatGPT(bot))