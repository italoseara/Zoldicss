import { SlashCommand, command, message } from "@/util";
import { ChatInputCommandInteraction } from "discord.js";
import * as messages from "messages.json";

@command({
  name: "ping",
  description: "🏓 Ping!",
})
class Ping extends SlashCommand {
  async execute(interaction: ChatInputCommandInteraction) {
    const latency = Date.now() - interaction.createdAt.getTime();

    await interaction.reply({
      content: message(messages.commands.ping, { latency }),
      ephemeral: true,
    });
  }
}

export default Ping;
