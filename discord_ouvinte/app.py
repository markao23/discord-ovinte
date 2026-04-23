import discord
import os
import asyncio
import signal
from keep_alive import keep_alive

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
                description="Acabei de ser ligado e estou pronto para ajudar!",
                color=discord.Color.green(),
            )
            await canal.send(content=f"<@{membros}>", embed=embed)

    async def setup_hook(self):
        # Esta função pode ser usada para configurações iniciais se necessário
        pass

    async def desligar_com_aviso(self):
        """Função para enviar a mensagem de offline antes de fechar"""
        canal = self.get_channel(canal_id)
        if canal:
            embed = discord.Embed(
                title="🔴 Bot Offline",
                description="Estou sendo desligado para manutenção ou reinicialização.",
                color=discord.Color.red(),
            )
            try:
                await canal.send(content=f"<@{membros}>", embed=embed)
                print("Mensagem de offline enviada!")
            except Exception as e:
                print(f"Erro ao enviar mensagem de offline: {e}")

        # Fecha a conexão do bot de forma limpa
        await self.close()


# Configuração de Intents
intents = discord.Intents.default()
client = MyClient(intents=intents)

# Inicia o servidor do keep_alive
keep_alive()

try:
    # Rodar o bot
    client.run(TOKEN)
except KeyboardInterrupt:
    # Captura quando você aperta Ctrl+C no terminal
    print("Desligando via terminal...")
finally:
    # Nota: Em ambientes como Replit, o 'finally' pode não rodar se o processo
    # for morto brutalmente (SIGKILL). Mas para desligamentos normais, funciona.
    print("Bot encerrado.")
