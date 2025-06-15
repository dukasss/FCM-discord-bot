# cogs/user_commands.py
import discord
from discord.ext import commands
from discord import app_commands
import database

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sugerir", description="Sugiere un personaje para que sea añadido al juego.")
    async def sugerir(self, interaction: discord.Interaction, nombre: str):
        """Publica una sugerencia de personaje en el canal dedicado."""
        suggestions_channel_id = database.get_config("suggestions_channel_id")
        
        if not suggestions_channel_id:
            await interaction.response.send_message("Uy, Elly no sabe dónde van las ideas. Un admin tiene que configurar el canal de sugerencias.", ephemeral=True)
            return

        suggestions_channel = self.bot.get_channel(suggestions_channel_id)
        if not suggestions_channel:
            await interaction.response.send_message("Pato no encuentra el canal de sugerencias, aunque estaba configurado. ¡Qué raro!", ephemeral=True)
            return

        texto_aclaratorio = "Recuerda, solo se permiten personajes ficticios y políticos porque hay que respetar a las personas (los políticos no merecen ningún tipo de respeto por q no son personas)."

        embed = discord.Embed(
            title="Nueva Sugerencia",
            description=f"**Personaje Sugerido:**\n`{nombre}`",
            color=discord.Color.yellow()
        )
        embed.set_author(name=f"Sugerido por: {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty)
        embed.set_footer(text=texto_aclaratorio)
        
        try:
            await suggestions_channel.send(embed=embed)
            await interaction.response.send_message("¡Listo! Tu idea ya está en el tablón. Pato la mirará luego.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Uy, parece que no tengo permisos para escribir en el canal de sugerencias.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(UserCommands(bot))
