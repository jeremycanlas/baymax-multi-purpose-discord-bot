from nextcord.ext import commands
from nextcord import Embed, Colour
from nextcord import Interaction, SlashOption, ChannelType, User
from nextcord.abc import GuildChannel
from azapi import AZlyrics
import os
import nextcord
from revChatGPT.revChatGPT import Chatbot

config = {
    "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..BZtYok9HBzIJlGJB.3UAcBzkhO96bNNLqbZNLxsIp1GivIxhuhO3t1zgjyXOOtSZnLbz14-9lAJvemOFRGm79RfS8YtzzBou7Ch0_ihIIbEqsRV4NZjiQ_pGswwoUm0hE9d_-s_BIc6eztSFSeVeiq_Zf1K7NLfS_mQ7D6bsavr211tuFV2kODYE2pt6jrxHAEBvwMSqhKjZz6AO31nRxZx3XAEFGxKGQQERlseqF9PMNpAFMhYBrU6Ecmaf6M8E6npSMiWPp0i5T04vGC9gbtqQ-VgIbB7wAL4HsxRPW9lmTfAEIHJT6jN0qFB-EiY9B9xJqxzH5yBuwzO-xRyS18Ap10841yaYWTu8Ut7efPhNo1F-NAVMJpDwOmiikl8aRAEelhc51Wgf66kHGzqFevG7pv9F7MVmMmom8mpM_aTxACXIEb6Oy2oWYuXXxw6TY4lXYB2N6SEQJQizaEZQv5Q2gbOmupzXtOOhtXPZvxe0cHx0p85fcPxQZ9UUSUNn4DGeW8AYmvsG927vAVBwN9BB-z3PycavzvadSz3YB0bCVoRTSR_Ikm51FKT6eWU4LqDgWp7_awpbUTY7Oy85QAoGnrKgHcNNr-LpdF0GvGWjqNaEfvmaqsV3Wz8JQHQSrMlle7t1APa1ATNUvSlbsR8HyFEoiZtKuUtk1q0J_8-puDUgJzTY13pqf80BX2Qui-NpBj7uZAlAC1zcYlnYKohc5nqlsIfWs5NTTG1Wf5U_t5uAKVWTymphA5aQm5Q_v-v_gr_ZOpcaBtLylbEJUptKF22fsEcih1De64ZnxEQtOOlx1ffGRWc78fVf_7If5yl33MmvMuCtov9l27rYGr4VlfjAEERHWxngzKj9na0nijYPeasBb8R-LIAmgANvPcbicYmP0awA5TM1K2fogK-VVhguwwH3RLF7ixFEgW3oj_-XXC5swfWiAVAnkj-KWQawhS7AAw_mw-KKm-zPWVqcTsiVFr7Txo2aPf6gc0f05Ab5DE6UUwj6fTAcZfA1fEBBJBtEs2k4A1TLOSK_G0p_jrTycoX7o2snMP3-viJJqm_RGW9FRVUXmqUwl-FpcBGXxeqjodt1OR8zgoi4NKeK_5ljWBQr-bOh5AaX5oH4fs4RiFrQUXRYZuWq0USxUmAOliFzXEU4TMr2_v1oyjkikURiU7SNAtO7pCZgpdsXUdj3iplyD5uW7bhMjtgIDXCSWlxbRv0SXaOt2MEGCN6wmN39FWrUIMbgOBgTcQTG60eHPTv2jyfgmgNzHO89yqiwQoTSWvT7AmmyQPTkxeQUIOZlohVhVuBln3RhQIfczXR1raWXOIEuNpqUW_QklOilrZhirZIWAL-TynjAsUx62keEXD4MZAm2t6WJ5t3vy6H4S8esqt9wJ7yGD__7XDQpZXmiCaYEQoszHIs9mh1JfYox9TyWsJucM75ghjyF4IBvrHL0yOSIfQSwW4diMRRhpWn-H_0TUW4RECNSG0u4_1c_-hAe-4rTlh-xIjkb1tLlC6YQWIg7ZCiIxolE8W5qAczwMNKzQ_gdFsVLnEe8lPSlfIDcQn0uR0BhntaPCybZFf1H39Gw2_0RYfOTiAlMxku_x5u8vQNprRGGwFs-E9P2yu_Mpbfyw7x7kLmXgPkgBZf89cudHvN9knDRyCn-wROj1Eh-VED55DyO67vVqz26PrtD3Aqrq5vSKNBO0O_EjOgklRRQjoYpaFxckerwocdGnOA3BzAeC4BdYNtFjzKp9LeoRnMtsuq-q3f63vJztFnpXTvXO5VJIb1F3EH-Wx8_grQ4V7EMRn2EGy5yDbqAf7jXkRTC9N6zr1SwfLNlu5sJ4SUjwhHuHbYAPqkEzjzKVmOLIf_z8-ifr-VNbQjC3kifwQ_hVLsz1ATOkeKalGcrZC6Q49GT1KiCovQKMzbhYR2DK35yNa7OScKN_7yR48PlSTiqZfzFKlmaYYU0K0GZYEFfCLgk1Zr7lHiLZLhfXoIBiqaRloEN4pZIGg_46fsXfU6rJtAvWgAiFc_dxOhKBVZNPh8a_PC2n0HYV20zvujO1JmVOSh-IGCqH3rHrAeITdIgo07GQYYg-5BsmWN2AbxVkQKkhJc3jecfXgfRGD-fjevtPPNkWC75PyebZ2f76Eee_7xPFNGR9g7K6HQUcB_4QgLOsdj6CJWRldsfw2XbHGOZdyF4QzXwMhav9wzvvDK-AcE-aSIAelT7nfldDRMMvIpApXzNAYqijePFMdaw7WID27KuzT-laXzGbttdWDyPPcp8Mu-s1.O-G_-vhp9Bc7AfJNIRhURw" # Deprecated. Use only if you encounter captcha with email/password
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