import "reflect-metadata";
import {
  ChatInputCommandInteraction,
  ButtonBuilder,
  ActionRowBuilder,
  ButtonStyle,
  StringSelectMenuBuilder,
  StringSelectMenuOptionBuilder,
} from "discord.js";

// ========================
//      User Interface
// ========================

export function button(info: {
  customId: string;
  label: string;
  style?: number;
  disabled?: boolean;
  emoji?: string;
}) {
  return (target: any, _key: string, descriptor: PropertyDescriptor) => {
    const components = Reflect.getMetadata("discord:components", target.constructor) || [];
    info.style = info.style || ButtonStyle.Primary;
    info.disabled = info.disabled || false;

    components.push({
      ...info,
      type: "Button",
      execute: descriptor.value,
    });

    Reflect.defineMetadata("discord:components", components, target.constructor);
  };
}

export function select(info: {
  customId: string;
  placeholder: string;
  options: {
    label: string;
    value: string;
    description?: string;
    emoji?: string;
    default?: boolean;
  }[];
  minValues?: number;
  maxValues?: number;
  disabled?: boolean;
}) {
  return (target: any, _key: string, descriptor: PropertyDescriptor) => {
    const components = Reflect.getMetadata("discord:components", target.constructor) || [];
    info.disabled = info.disabled || false;
    info.minValues = info.minValues || 1;
    info.maxValues = info.maxValues || 1;

    components.push({
      ...info,
      type: "StringSelect",
      execute: descriptor.value,
    });

    Reflect.defineMetadata("discord:components", components, target.constructor);
  };
}

export abstract class View extends ActionRowBuilder<any> {
  constructor() {
    super();
    const meta = Reflect.getMetadata("discord:components", this.constructor) || [];

    for (const component of meta) {
      if (component.type === "Button") {
        const button = new ButtonBuilder()
          .setCustomId(component.customId)
          .setLabel(component.label)
          .setStyle(component.style)
          .setDisabled(component.disabled);

        if (component.emoji) button.setEmoji(component.emoji);

        this.addComponents(button);
      } else if (component.type === "StringSelect") {
        const select = new StringSelectMenuBuilder()
          .setCustomId(component.customId)
          .setPlaceholder(component.placeholder)
          .setDisabled(component.disabled)
          .setMinValues(component.minValues)
          .setMaxValues(component.maxValues)
          .addOptions(
            component.options.map((option) => {
              const selectOption = new StringSelectMenuOptionBuilder()
                .setLabel(option.label)
                .setValue(option.value);

              if (option.description) selectOption.setDescription(option.description);
              if (option.emoji) selectOption.setEmoji(option.emoji);
              if (option.default) selectOption.setDefault();

              return selectOption;
            })
          );

        this.addComponents(select);
      }
    }
  }
}

// ========================
//      Slash Commands
// ========================

export class CommandGroup {
  name: string;
  description: string;
  permissions?: bigint;
  commands: Map<string, new () => SlashCommand> = new Map();

  constructor(info: { name: string; description: string; permissions?: bigint }) {
    this.name = info.name;
    this.description = info.description;
    this.permissions = info.permissions;
  }

  subcommand(info: { name: string; description: string }) {
    return (target: any) => {
      const meta = Reflect.getMetadata("discord:command", target) || {};
      Reflect.defineMetadata("discord:command", { ...meta, ...info }, target);

      this.commands.set(info.name, target);
    };
  }
}

export abstract class SlashCommand {
  abstract execute(interaction: ChatInputCommandInteraction): Promise<void>;
}

export abstract class Event {
  abstract execute(...args: any[]): Promise<void>;
}

export function event(info: { name: string; once?: boolean }) {
  return (target: any) => {
    const meta = Reflect.getMetadata("discord:event", target) || {};
    Reflect.defineMetadata("discord:event", { ...meta, ...info }, target);
  };
}

export function command(info: { name: string; description: string; permissions?: bigint }) {
  return function (target: any) {
    const meta = Reflect.getMetadata("discord:command", target) || {};
    Reflect.defineMetadata("discord:command", { ...meta, ...info }, target);
  };
}

export function option(info: {
  name?: string;
  description: string;
  choices?: { name: string; value: string }[];
}) {
  return (target: any, key: string) => {
    // Create an instance of the class to access the field value
    const instance = new target.constructor();

    const meta = Reflect.getMetadata("discord:command", target.constructor) || {};
    const type = Reflect.getMetadata("design:type", target, key);
    const value = instance[key];
    const options = meta.options || [];

    options.push({
      name: info.name || key,
      description: info.description,
      choices: info.choices || [],
      type: type.name,
      required: value === undefined,
      default: value,
    });

    Reflect.defineMetadata("discord:command", { ...meta, options }, target.constructor);
  };
}
