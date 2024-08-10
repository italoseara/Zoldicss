import { CommandInteraction } from "discord.js";
import { CommandGroup, SlashCommand } from "@/core";
import { TestView, Test2View } from "./test";

const group = new CommandGroup({ name: "group", description: "Example group" });

@group.subcommand({
  name: "subcommand",
  description: "Example subcommand",
})
class Subcommand extends SlashCommand {
  async execute(interaction: CommandInteraction) {
    interaction.reply("Subcommand executed!");
  }
}

@group.subcommand({
  name: "subcommand2",
  description: "Example subcommand 2",
})
class Subcommand2 extends SlashCommand {
  async execute(interaction: CommandInteraction) {
    interaction.reply({
      content: "Subcommand 2 executed!",
      components: [new TestView(), new Test2View()],
    });
  }
}

export default group;
