import { DataSource } from "typeorm";
import UserEntity from "./entities/UserEntity";

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
      entities: [UserEntity],
      synchronize: true,
    });

    await this.connection.initialize();

    console.log(`📁 Connected to '${process.env.DATABASE_NAME}' database`);
    console.log();
  }
}

export default DatabaseManager;
