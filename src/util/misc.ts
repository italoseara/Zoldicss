import * as fs from "fs";
import * as path from "path";

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

  getFilesRecursive(dir);
  return files;
}

export function message(
  message: string | Record<string, any>,
  placeholders: Record<string, any> = {}
): string {
  if (typeof message === "object") {
    message = message.join("\n");
  }

  return message.replace(/{([^}]+)}/g, (_: any, key: string | number) =>
    placeholders[key].toString()
  );
}
