import { ActivityType, Events } from "discord.js";
import { event, Event } from "@/util";
import Bot from "@/bot";

@event({
  name: Events.ClientReady,
  once: true,
})
class Ready extends Event {
  async execute(bot: Bot) {
    console.log("🤖 Bot is ready!");
    console.log(`🚀 Logged in as ${bot.user.tag}`);
    console.log();

    // Change the bot's status
    bot.user.setActivity("Em desenvolvimento...", { type: ActivityType.Custom });
  }
}

export default Ready;
