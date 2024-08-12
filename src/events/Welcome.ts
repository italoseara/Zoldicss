import { ChatInputCommandInteraction, Colors, EmbedBuilder, Events } from "discord.js";
import { Event, event, replace } from "@/util";
import { Player } from "@/database";
import * as messages from "messages.json";

@event({ name: Events.InteractionCreate })
class Welcome extends Event {
  async execute(interaction: any) {
    if (!interaction.isChatInputCommand()) return;

    const { user, client } = interaction as ChatInputCommandInteraction;
    const player = await Player.findOne({ where: { discordId: user.id } });
    if (player) return; // Player already exists

    await Player.create({ discordId: user.id }).save();
    await interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setAuthor({ name: user.tag, iconURL: user.displayAvatarURL() })
          .setTitle(replace(messages.events.welcome.title, { user: user.displayName }))
          .setDescription(messages.events.welcome.description)
          .setColor(Colors.Green)
          .setFooter({ text: messages.events.welcome.footer })
          .setThumbnail(client.user.displayAvatarURL()),
      ],
    });
  }
}

export default Welcome;
