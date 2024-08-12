import { ActivityType, Events } from "discord.js";
import { event, Event } from "@/util";
import Bot from "@/Bot";
import * as messages from "messages.json";

@event({
  name: Events.ClientReady,
  once: true,
})
class Ready extends Event {
  async execute(bot: Bot) {
    console.log("🤖 Bot is ready!");
    console.log(`🚀 Logged in as ${bot.user.tag}`);
    console.log();

    let i = 0;
    setInterval(() => {
      bot.user.setActivity(messages.activities[i], { type: ActivityType.Custom });
      i = ++i % messages.activities.length;
    }, 10000);
  }
}

export default Ready;
