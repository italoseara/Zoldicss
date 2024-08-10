import { button, select, View } from "@/core";
import { StringSelectMenuInteraction, ButtonStyle, ButtonInteraction } from "discord.js";

export class TestView extends View {
  @select({
    customId: "selectme",
    placeholder: "Select Me",
    options: [
      { label: "Option 1", value: "1", description: "Option 1 description", emoji: "🍔" },
      { label: "Option 2", value: "2", description: "Option 2 description", emoji: "🍟" },
      { label: "Option 3", value: "3", description: "Option 3 description", emoji: "🍕" },
    ],
  })
  async select(interaction: StringSelectMenuInteraction) {
    const selected = interaction.values.join(", ");
    interaction.reply({
      content: `You selected: ${selected}`,
      ephemeral: true,
    });
  }
}

export class Test2View extends View {
  @button({
    customId: "button1",
    label: "Button 1",
    emoji: "🍔",
  })
  async button1(interaction: ButtonInteraction) {
    interaction.reply({
      content: "Button 1 clicked!",
      ephemeral: true,
    });
  }

  @button({
    customId: "button2",
    label: "Button 2",
    emoji: "🍟",
    style: ButtonStyle.Danger,
  })
  async button2(interaction: ButtonInteraction) {
    interaction.reply({
      content: "Button 2 clicked!",
      ephemeral: true,
    });
  }

  @button({
    customId: "button3",
    label: "Button 3",
    emoji: "🍕",
    style: ButtonStyle.Secondary,
  })
  async button3(interaction: ButtonInteraction) {
    interaction.reply({
      content: "Button 3 clicked!",
      ephemeral: true,
    });
  }
}
