import "dotenv/config";
import Bot from "./Bot";
import { DatabaseManager } from "./database";

const main = async () => {
  const bot = new Bot();

  await DatabaseManager.connect();
  await bot.start(process.env.DISCORD_TOKEN);
};

main();
