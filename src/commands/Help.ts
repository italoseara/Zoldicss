import { SlashCommand, command } from "@/util";
import { ChatInputCommandInteraction } from "discord.js";

@command({
  name: "help",
  description: "📚 Lista de comandos disponíveis",
})
class Help extends SlashCommand {
  async execute(interaction: ChatInputCommandInteraction) {
    await interaction.reply("TODO: Implementar o comando de ajuda");
  }
}

export default Help;
