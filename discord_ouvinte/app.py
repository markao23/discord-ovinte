import discord
import os
import asyncio
from keep_alive import keep_alive

TOKEN = os.environ.get("DISCORD_TOKEN")
CANAL_ID = 1494127600350658621
MEMBROS_ID = 1494355178114257047  # Assumindo que seja um cargo (Role)

# === ADICIONE O ID DO SEU BOT PRINCIPAL AQUI ===
BOT_PRINCIPAL_ID = 1475934513313091615

# Tempo em segundos que o Vigia vai esperar antes de avisar que o bot caiu
TEMPO_ESPERA = 30


class VigiaClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Variável para guardar a tarefa de contagem regressiva do offline
        self.offline_task = None

    async def on_ready(self):
        print(f"👁️ Bot Vigia logado como {self.user} e pronto para monitorar!")

    async def on_presence_update(self, before, after):
        # Ignora as atualizações se não for o nosso Bot Principal
        if after.id != BOT_PRINCIPAL_ID:
            return

        canal = self.get_channel(CANAL_ID)
        if not canal:
            return

        # LOGICA 1: O BOT FICOU ONLINE (Era offline e mudou para online/idle/dnd)
        if (
            before.status == discord.Status.offline
            and after.status != discord.Status.offline
        ):

            # Se o bot caiu, mas voltou rápido antes do TEMPO_ESPERA acabar, cancelamos o aviso de queda!
            if self.offline_task and not self.offline_task.done():
                self.offline_task.cancel()
                print("Bot voltou rápido! Aviso de queda cancelado.")

            embed = discord.Embed(
                title="🟢 Bot Principal Online!",
                description="O bot principal acabou de ligar e está operante!",
                color=discord.Color.green(),
            )
            # Nota: <@&ID> é para mencionar cargos. Se for um usuário específico use <@ID>
            await canal.send(content=f"<@&{MEMBROS_ID}>", embed=embed)
            print("Aviso de ONLINE enviado.")

        # LOGICA 2: O BOT FICOU OFFLINE
        elif (
            before.status != discord.Status.offline
            and after.status == discord.Status.offline
        ):
            print(
                "Bot principal parece ter caído. Iniciando contagem de verificação..."
            )

            # Cria uma "tarefa em segundo plano" para esperar e avisar
            self.offline_task = asyncio.create_task(self.verificar_offline_real(canal))

    async def verificar_offline_real(self, canal):
        try:
            # Espera o tempo definido para ver se foi apenas um restart rápido
            await asyncio.sleep(TEMPO_ESPERA)

            # Se o código chegou até aqui sem ser cancelado, o bot principal realmente caiu
            embed = discord.Embed(
                title="🔴 Bot Principal Offline",
                description=f"O bot principal foi desligado ou caiu.\n*(Confirmado após {TEMPO_ESPERA} segundos de inatividade)*",
                color=discord.Color.red(),
            )
            await canal.send(content=f"<@&{MEMBROS_ID}>", embed=embed)
            print("Aviso de OFFLINE enviado.")

        except asyncio.CancelledError:
            # Esse erro é gerado de propósito lá no bloco 'ONLINE' se o bot voltar a tempo.
            # Apenas ignoramos em silêncio.
            pass


# Configuração de Intents (MUITO IMPORTANTE ativar presences e members)
intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = VigiaClient(intents=intents)

# Inicia o servidor do keep_alive (se você usa Flask no Replit, por exemplo)
keep_alive()

try:
    client.run(TOKEN)
except Exception as e:
    print(f"Erro fatal no Vigia: {e}")
