import {
  BaseInteraction,
  ChatInputCommandInteraction,
  Colors,
  EmbedBuilder,
  Events,
} from "discord.js";
import { Event, event, message } from "@/util";
import { Player } from "@/database";
import * as messages from "messages.json";

@event({ name: Events.InteractionCreate })
class Welcome extends Event {
  async execute(interaction: BaseInteraction) {
    if (!interaction.isChatInputCommand()) return;

    const { user } = interaction as ChatInputCommandInteraction;
    const player = await Player.findOne({ where: { discordId: user.id } });
    if (player) return; // Player already exists

    await Player.create({ discordId: user.id }).save();
    await interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setAuthor({ name: user.tag, iconURL: user.displayAvatarURL() })
          .setTitle(message(messages.welcome.title, { user: user.displayName }))
          .setDescription(message(messages.welcome.description))
          .setThumbnail(messages.welcome.thumbnail)
          .setColor(Colors.Green),
      ],
    });
  }
}

export default Welcome;
