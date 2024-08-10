import "dotenv/config"
import Bot from "./bot";

const client = new Bot();
client.start(process.env.TOKEN);