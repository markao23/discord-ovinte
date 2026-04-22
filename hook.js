const { Client, GatewayIntentBits } = require("discord.js");
const express = require("express");

// ==========================================
// 1. SERVIDOR WEB (Para Render e UptimeRobot)
// ==========================================
const app = express();
app.get("/", (req, res) => res.send("Bot Monitor está Vivo e Vigiando!"));

// O Render define a porta automaticamente na variável de ambiente PORT
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Servidor Web rodando na porta ${port}`));

// ==========================================
// 2. LÓGICA DO BOT DO DISCORD
// ==========================================
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildPresences, // ESSENCIAL para ler status de online/offline
  ],
});

// Substitua pelos IDs reais
const ID_DO_BOT_PRINCIPAL = "1475934513313091615";
const ID_DO_CANAL_DE_AVISO = "1456704732159676478";

client.once("ready", () => {
  console.log(`Bot Monitor logado como ${client.user.tag}!`);
});

// Evento que dispara sempre que alguém (ou algum bot) muda de status
client.on("presenceUpdate", (oldPresence, newPresence) => {
  // Verifica se a atualização de status veio do seu bot principal
  if (!newPresence || newPresence.userId !== ID_DO_BOT_PRINCIPAL) return;

  const canal = client.channels.cache.get(ID_DO_CANAL_DE_AVISO);
  if (!canal) return;

  // Define os status (se oldPresence for null, assume offline)
  const statusAntigo = oldPresence ? oldPresence.status : "offline";
  const statusNovo = newPresence.status;

  // Lógica para avisar se caiu ou voltou
  if (statusNovo === "offline" && statusAntigo !== "offline") {
    canal.send(
      `🚨 **ALERTA!** O bot principal acabou de ficar OFFLINE! <@SEU_ID_AQUI_SE_QUISER_SER_MARCADO>`,
    );
  } else if (statusNovo !== "offline" && statusAntigo === "offline") {
    canal.send(`✅ **UFA!** O bot principal voltou a ficar ONLINE!`);
  }
});

// Adicionando capturadores de erro para descobrirmos o problema
client.login(process.env.TOKEN); // Ou o nome da variável que você usou no Render

