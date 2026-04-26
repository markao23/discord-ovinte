import discord
import os
import asyncio
from keep_alive import keep_alive

TOKEN = os.environ.get("DISCORD_TOKEN")
CANAL_ID = 1494127600350658621
MEMBROS_ID = 1498006459940868207  

# === ADICIONE O ID DO SEU BOT PRINCIPAL AQUI ===
BOT_PRINCIPAL_ID = 1475934513313091615
TEMPO_ESPERA = 30

class VigiaClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offline_task = None
        # NOVA VARIÁVEL: Guarda o último status para evitar duplicatas
        self.ultimo_status_conhecido = None 

    async def on_ready(self):
        print(f"👁️ Bot Vigia logado como {self.user} e pronto para monitorar!")

    async def on_presence_update(self, before, after):
        if after.id != BOT_PRINCIPAL_ID:
            return

        # NOVO FILTRO: Se o status que chegou for igual ao que já processamos, ignora
        if self.ultimo_status_conhecido == after.status:
            return
            
        # Atualiza a memória com o novo status
        self.ultimo_status_conhecido = after.status

        canal = self.get_channel(CANAL_ID)
        if not canal:
            return

        # LOGICA 1: O BOT FICOU ONLINE
        if before.status == discord.Status.offline and after.status != discord.Status.offline:

            if self.offline_task and not self.offline_task.done():
                self.offline_task.cancel()
                print("Bot voltou rápido! Aviso de queda cancelado.")

            embed = discord.Embed(
                title="🟢 Bot Principal Online!",
                description="O bot principal acabou de ligar e está operante!",
                color=discord.Color.green(),
            )
            await canal.send(content=f"<@&{MEMBROS_ID}>", embed=embed)
            print("Aviso de ONLINE enviado.")

        # LOGICA 2: O BOT FICOU OFFLINE
        elif before.status != discord.Status.offline and after.status == discord.Status.offline:
            print("Bot principal parece ter caído. Iniciando contagem de verificação...")
            self.offline_task = asyncio.create_task(self.verificar_offline_real(canal))

    async def verificar_offline_real(self, canal):
        try:
            await asyncio.sleep(TEMPO_ESPERA)
            
            embed = discord.Embed(
                title="🔴 Bot Principal Offline",
                description=f"O bot principal foi desligado ou caiu.\n*(Confirmado após {TEMPO_ESPERA} segundos de inatividade)*",
                color=discord.Color.red(),
            )
            await canal.send(content=f"<@&{MEMBROS_ID}>", embed=embed)
            print("Aviso de OFFLINE enviado.")

        except asyncio.CancelledError:
            pass


intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = VigiaClient(intents=intents)

keep_alive()

try:
    client.run(TOKEN)
except Exception as e:
    print(f"Erro fatal no Vigia: {e}")
