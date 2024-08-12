import {
  ButtonInteraction,
  ChatInputCommandInteraction,
  Events,
  StringSelectMenuInteraction,
} from "discord.js";
import { event, Event } from "@/util";
import Bot from "@/Bot";
import { Player } from "@/database";

@event({ name: Events.InteractionCreate })
class InteractionCreate extends Event {
  async handleSlashCommand(interaction: ChatInputCommandInteraction) {
    const bot = interaction.client as Bot;
    const { commandName, user, options } = interaction;
    const subcommand = options.getSubcommand(false);

    const executed = subcommand ? `/${commandName} ${subcommand}` : `/${commandName}`;
    console.log(`🔔 @${user.tag} executed command: ${executed}`);

    const command = bot.getCommand(interaction);
    if (!command) {
      console.error("🔴 Command not found:", executed);
      return;
    }

    try {
      const instance = new command();
      const commandOptions = Reflect.getMetadata("discord:command", command).options || [];

      for (const option of commandOptions) {
        const value = options[`get${option.type}`](option.name) ?? option.default;
        instance[option.name] = value;
      }

      await instance.execute(interaction);
    } catch (error) {
      console.error("🔴 Error while executing command:", commandName, error);
      interaction.reply({
        content: "❌ There was an error while executing this command.",
        ephemeral: true,
      });
    }
  }

  async handleComponent(interaction: ButtonInteraction | StringSelectMenuInteraction) {
    const bot = interaction.client as Bot;
    const { user, customId } = interaction;
    const callback = bot.components.get(customId);
    if (!callback) {
      console.error("🔴 Component callback not found:", customId);
      interaction.reply({
        content: "❌ This component is not working.",
        ephemeral: true,
      });
      return;
    }

    console.log(`🔔 @${user.tag} interacted with a component: ${customId}`);
    callback(interaction);
  }

  async execute(interaction: any) {
    const player = await Player.findOne({ where: { discordId: interaction.user.id } });
    if (!player) return; // Player already exists

    if (interaction.isChatInputCommand()) {
      await this.handleSlashCommand(interaction);
    } else if (interaction.isButton() || interaction.isStringSelectMenu()) {
      await this.handleComponent(interaction);
    }
  }
}

export default InteractionCreate;
