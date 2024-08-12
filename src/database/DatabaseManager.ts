import { DataSource } from "typeorm";
import Player from "./entities/Player";

class DatabaseManager {
  static connection: DataSource;

  static async connect() {
    console.log("🔧 Connecting to the database...");

    this.connection = new DataSource({
      type: "postgres",
      host: process.env.DATABASE_HOST,
      port: parseInt(process.env.DATABASE_PORT),
      username: process.env.DATABASE_USER,
      password: process.env.DATABASE_PASSWORD,
      database: process.env.DATABASE_NAME,
      entities: [Player],
      synchronize: true,
    });

    try {
      await this.connection.initialize();
    } catch (error: any) {
      console.error("❌ Failed to connect to the database");
      console.error(error);
      process.exit(1);
    }

    console.log(`📁 Connected to '${process.env.DATABASE_NAME}' database`);
    console.log();
  }
}

export default DatabaseManager;
