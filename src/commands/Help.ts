import { SlashCommand, command } from "@/util";
import { ChatInputCommandInteraction } from "discord.js";

@command({
  name: "help",
  description: "📚 Mostra uma lista de comandos do bot",
})
class Help extends SlashCommand {
  async execute(interaction: ChatInputCommandInteraction) {
    await interaction.reply("TODO: Implementar o comando de ajuda");
  }
}

export default Help;
