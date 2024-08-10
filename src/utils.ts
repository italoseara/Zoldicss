import * as fs from "fs";
import * as path from "path";
import { InteractionChatInputCommandInteraction } from "discord.js";

// Type alias because the original type is too long and ugly
export type SlashCommandInteraction = InteractionChatInputCommandInteraction;

// Get all files in a directory (recursively)
export function getFiles(dir: string): string[] {
  const files: string[] = [];

  const getFilesRecursive = (directory: string): void => {
    const filesInDir = fs.readdirSync(directory);

    for (const file of filesInDir) {
      const filePath = path.join(directory, file);
      if (fs.statSync(filePath).isDirectory()) {
        getFilesRecursive(filePath);
      } else {
        files.push(filePath);
      }
    }
  };

  getFilesRecursive(path.join(__dirname, dir));
  return files;
}

