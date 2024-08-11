import * as fs from "fs";
import * as path from "path";

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

  getFilesRecursive(dir);
  return files;
}
