const express = require("express");
const app = express();

// ⚠️ CUIDADO: Cole sua URL aqui, mas não compartilhe com mais ninguém!
const webhookUrl =
  "https://discord.com/api/webhooks/1496487271363252314/uHcpWMNCC50aIAdSyrYN_iDpUSia8p2flfbIBSvEbs44wDdiVyw0E-LHsIR25KVuNAE6";

async function enviarStatusBot(status) {
  const isOnline = status === "ON";
  const corHex = isOnline ? 0x00ff00 : 0xff0000;
  const mensagem = isOnline
    ? "Preparar os canhões! O bot está online e rodando 24/7! 🚢💣"
    : "Recolher as velas! O bot foi desligado. ⚓💤";

  const data = {
    content: "@everyone",
    allowed_mentions: { parse: ["everyone"] },
    embeds: [
      {
        title: `Status do Bot: ${status}`,
        description: mensagem,
        color: corHex,
        timestamp: new Date().toISOString(),
        footer: { text: "Captain Hook System" },
      },
    ],
  };

  try {
    const response = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      console.log("✅ Mensagem com Embed enviada com sucesso!");
    } else {
      // Aqui está o truque: se o Discord recusar, ele vai mostrar o motivo!
      const erroDiscord = await response.text();
      console.error("❌ O Discord recusou a mensagem. Erro:", erroDiscord);
    }
  } catch (error) {
    // Se cair aqui, provavlemente seu Node.js é antigo e não suporta o 'fetch'
    console.error(
      "⚠️ Erro fatal ao tentar enviar (Verifique sua versão do Node.js):",
      error.message,
    );
  }
}

// ROTA DA WEB: Para o UptimeRobot
app.get("/", (req, res) => {
  res.send("O navio está navegando! 🏴‍☠️ (Servidor Online)");
});

// Ligar o Servidor Web e avisar o Discord
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`⚓ Servidor rodando na porta ${PORT}`);

  // Envia a mensagem pro Discord
  enviarStatusBot("ON");
});
