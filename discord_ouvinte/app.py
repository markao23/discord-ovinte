import discord
import os
from keep_alive import keep_alive  # Importa o mini-site

# Pega o token de forma segura
TOKEN = os.environ.get("DISCORD_TOKEN")


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logado como {self.user}")


client = MyClient(intents=discord.Intents.default())

# Inicia o mini-site ANTES de ligar o bot
keep_alive()

# Liga o bot com o Token protegido
client.run(TOKEN)
