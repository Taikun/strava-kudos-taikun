from discord import app_commands, Intents, Client, Interaction
from jproperties import Properties

class Bot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=None)


bot = Bot(intents=Intents.default())

@bot.event
async def on_ready():
    print(f"Conectado como: {bot.user}")


@bot.tree.command()
async def youtube(interaction: Interaction):
    await interaction.response.send_message("Taikun Channel: https://www.youtube.com/c/TaikunCornerChannel")


@bot.tree.command()
async def givemebadge(interaction: Interaction):
    await interaction.response.send_message("Listo!, espera 24 horas para reclamar la insignia\nPuedes reclamarla aquí: https://discord.com/developers/active-developer")

configs = Properties()
with open("kudos.properties", "rb") as config_file:
        configs.load(config_file)

TOKEN_DISCORD_BOT = configs.get("TOKEN_DISCORD_BOT").data

bot.run(TOKEN_DISCORD_BOT)

