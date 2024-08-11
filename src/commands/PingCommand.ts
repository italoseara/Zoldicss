import { SlashCommand, command } from "@/util";
import { ChatInputCommandInteraction } from "discord.js";

@command({
  name: "ping",
  description: "🏓 Ping!",
})
class PingCommand extends SlashCommand {
  async execute(interaction: ChatInputCommandInteraction) {
    const latency = Date.now() - interaction.createdAt.getTime();

    await interaction.reply({
      content: `🏓 Pong! \`${latency}ms\``,
      ephemeral: true,
    });
  }
}

export default PingCommand;
