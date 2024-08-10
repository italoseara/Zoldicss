import { SlashCommand, command, SlashCommandInteraction } from "@/util";

@command({
  name: "ping",
  description: "🏓 Ping!",
})
class PingCommand extends SlashCommand {
  async execute(interaction: SlashCommandInteraction) {
    const reply = await interaction.deferReply({
      ephemeral: true,
      fetchReply: true,
    });

    const latency = reply.createdTimestamp - interaction.createdTimestamp;
    interaction.editReply(`🏓 Pong! \`${latency}ms\``);
  }
}

export default PingCommand;
