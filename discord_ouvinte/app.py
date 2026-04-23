import discord
import os
from keep_alive import keep_alive  # Importa o mini-site

# Pega o token de forma segura
TOKEN = os.environ.get("DISCORD_TOKEN")
canal_id = 1494127600350658621
membros = 1494355178114257047

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logado como {self.user}")

        canal = self.get_channel(canal_id)
        if canal:
            embed = discord.Embed(
                title="🟢 Bot Online!",
                description="Acabei de ser ligado e estou pronto para ajudar o servidor!",
                color=discord.Color.green(),  # Cor da barra lateral
            )
            await canal.send(content=f"<@{membros}>", embed=embed)
        else:
            print("Não consegui achar o canal. Verifique se o CANAL_ID está correto!")


client = MyClient(intents=discord.Intents.default())

# Inicia o mini-site ANTES de ligar o bot
keep_alive()

# Liga o bot com o Token protegido
client.run(TOKEN)
