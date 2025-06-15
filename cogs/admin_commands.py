# cogs/admin_commands.py
import discord
from discord.ext import commands
from discord import app_commands
import database

class AdminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="configurar", description="Establece los canales para el juego y las sugerencias.")
    @app_commands.checks.has_permissions(administrator=True)
    async def configurar(self, interaction: discord.Interaction, canal_juego: discord.TextChannel, canal_sugerencias: discord.TextChannel):
        """Configura los canales necesarios para el bot."""
        database.set_config("fcm_channel_id", str(canal_juego.id))
        database.set_config("suggestions_channel_id", str(canal_sugerencias.id))
        await interaction.response.send_message(
            f"¡Listo! El juego se publicará en {canal_juego.mention} y las sugerencias en {canal_sugerencias.mention}.",
            ephemeral=True
        )

    @app_commands.command(name="aprobar", description="Añade un personaje al juego. Coge el nombre del canal de sugerencias.")
    @app_commands.checks.has_permissions(administrator=True)
    async def aprobar(self, interaction: discord.Interaction, nombre: str, url_imagen: str):
        """Aprueba un personaje y lo añade al juego."""
        try:
            database.add_character(nombre, url_imagen)
            await interaction.response.send_message(f"¡Listo! '{nombre}' ya está en el juego. Elly está contenta.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Uy, se cayó. Seguramente '{nombre}' ya existe en el juego.", ephemeral=True)

    @configurar.error
    @aprobar.error
    async def admin_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("No puedes hacer eso. No eres mi jefe. Pato es mi jefe.", ephemeral=True)
        else:
            print(error)
            await interaction.response.send_message("Uy, se cayó. Elly tiene que arreglarlo.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))
