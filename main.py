# main.py
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import datetime
import asyncio
import database

# --- Configuración Inicial ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = False

# Zona horaria para la tarea diaria (16:00 UTC = 17:00 en Canarias)
UTC_TIME = datetime.time(hour=16, minute=0, tzinfo=datetime.timezone.utc)

class PocoyoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.initial_extensions = [
            "cogs.user_commands",
            "cogs.admin_commands"
        ]

    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        
        await self.tree.sync()
        self.daily_fcm_task.start()

    async def on_ready(self):
        print(f'¡Hola! Soy {self.user} y estoy listo para jugar.')
        print(f'ID: {self.user.id}')
        
    @tasks.loop(time=UTC_TIME)
    async def daily_fcm_task(self):
        print(f"Ejecutando la tarea diaria de FCM a las {UTC_TIME} UTC...")
        
        channel_id = database.get_config("fcm_channel_id")
        if not channel_id:
            print("Error: No hay canal de juego configurado. La tarea no se ejecutará.")
            return

        channel = self.get_channel(channel_id)
        if not channel:
            print(f"Error: No se pudo encontrar el canal con ID {channel_id}.")
            return

        characters = database.get_random_characters(3)
        if len(characters) < 3:
            print("Error: No hay suficientes personajes en la base de datos (se necesitan 3).")
            await channel.send("Uy, no hay suficientes amigos para jugar hoy. Elly está buscando más.")
            return

        for name, image_url in characters:
            embed = discord.Embed(title=name, color=discord.Color.random())
            embed.set_image(url=image_url)
            await channel.send(embed=embed)
            await asyncio.sleep(1)

        final_message = await channel.send("### **¿Qué eliges? ¡A votar!**")

        await final_message.add_reaction("🔥")
        await final_message.add_reaction("💍")
        await final_message.add_reaction("💀")
        print("Tarea diaria completada con éxito.")

    @daily_fcm_task.before_loop
    async def before_daily_task(self):
        await self.wait_until_ready()
        print("El bot está listo, la tarea diaria está esperando su hora.")

# --- Ejecución del Bot ---
if __name__ == "__main__":
    database.setup_database()
    bot = PocoyoBot()
    bot.run(TOKEN)
