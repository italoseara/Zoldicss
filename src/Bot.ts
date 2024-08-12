import "reflect-metadata";
import {
  ChatInputCommandInteraction,
  Client,
  GatewayIntentBits,
  REST,
  Routes,
  SlashCommandBuilder,
} from "discord.js";
import { getFiles, CommandGroup, SlashCommand, View, Event } from "@/util";
import * as config from "config.json";

export default class Bot extends Client {
  token: string;

  commands: Map<string, new () => SlashCommand> = new Map();
  commandGroups: Map<string, CommandGroup> = new Map();
  components: Map<string, Function> = new Map();

  constructor() {
    super({
      intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildModeration,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildIntegrations,
      ],
    });
  }

  async load() {
    const views = [];
    const events = [];
    const commands = [];
    const commandGroups = [];

    const files = getFiles(__dirname).filter((file) => file.endsWith(".ts"));

    for (const path of files) {
      const exported: any[] = Object.values(require(path));
      if (!exported) continue;

      for (const module of exported) {
        if (module.prototype instanceof View) views.push(module);
        else if (module.prototype instanceof Event) events.push(module);
        else if (module.prototype instanceof SlashCommand) commands.push(module);
        else if (module instanceof CommandGroup) commandGroups.push(module);
      }
    }

    await this.loadCommands(commands, commandGroups);
    await this.loadEvents(events);
    await this.loadComponents(views);
  }

  async loadComponents(views: (new () => View)[]) {
    console.log("🔧 Loading components...");

    for (const ViewClass of views) {
      const components = Reflect.getMetadata("discord:components", ViewClass);

      for (const component of components) {
        const { customId, execute, type } = component;

        if (this.components.has(customId)) {
          console.log(`🟠 Skipping duplicate component: ${customId} (${type})`);
          continue;
        }

        this.components.set(customId, execute);
        console.log(`🟢 Loaded component: ${customId} (${type})`);
      }
    }

    if (views.length === 0) console.log("🟠 No components found");
    console.log();
  }

  async loadEvents(events: (new () => Event)[]) {
    console.log("🔧 Loading events...");

    for (const EventClass of events) {
      const meta = Reflect.getMetadata("discord:event", EventClass);
      this[meta.once ? "once" : "on"](meta.name, async (...args: any[]) => {
        const instance = new EventClass();
        instance.execute(...args);
      });
      console.log(`🟢 Loaded event: ${EventClass.name}`);
    }

    if (events.length === 0) console.log("🟠 No events found");
    console.log();
  }

  async loadCommands(commands: (new () => SlashCommand)[], commandGroups: CommandGroup[]) {
    console.log("🔧 Loading application (/) commands...");

    for (const commandGroup of commandGroups) {
      const name = commandGroup.name;
      const commands = commandGroup.commands.keys();
      this.commandGroups.set(name, commandGroup);

      console.log(`🟢 Loaded command group: /${name} (${[...commands].join(", ")})`);
    }

    for (const command of commands) {
      const name = Reflect.getMetadata("discord:command", command).name;
      this.commands.set(name, command);

      console.log(`🟢 Loaded command: /${name}`);
    }

    await this.registerCommands();
    if (commands.length === 0 && commandGroups.length === 0) console.log("🟠 No commands found");
    console.log();
  }

  async registerCommands() {
    try {
      if (config.dev) {
        const data = [];

        // Build the commands
        for (const [_, command] of this.commands) {
          const meta = Reflect.getMetadata("discord:command", command);
          const builder = new SlashCommandBuilder()
            .setName(meta.name)
            .setDescription(meta.description);

          if (meta.permissions) builder.setDefaultMemberPermissions(meta.permissions);
          if (meta.options) {
            for (const option of meta.options) {
              const { type, name, description, required, choices } = option;
              builder[`add${type}Option`]((option) => {
                option.setName(name).setDescription(description).setRequired(required);
                if (choices.length > 0) option.addChoices(choices);
                return option;
              });
            }
          }

          data.push(builder.toJSON());
        }

        // Build the command groups
        for (const [_, commandGroup] of this.commandGroups) {
          const builder = new SlashCommandBuilder()
            .setName(commandGroup.name)
            .setDescription(commandGroup.description);

          if (commandGroup.permissions)
            builder.setDefaultMemberPermissions(commandGroup.permissions);

          for (const [_, command] of commandGroup.commands) {
            const meta = Reflect.getMetadata("discord:command", command);
            builder.addSubcommand((subcommand) => {
              subcommand.setName(meta.name).setDescription(meta.description);
              if (meta.options) {
                for (const option of meta.options) {
                  const { type, name, description, required, choices } = option;
                  subcommand[`add${type}Option`]((option) => {
                    option.setName(name).setDescription(description).setRequired(required);
                    if (choices.length > 0) option.addChoices(choices);
                    return option;
                  });
                }
              }
              return subcommand;
            });
          }

          data.push(builder.toJSON());
        }

        // Register the commands
        const rest = new REST().setToken(this.token);
        const result = await rest.put(
          Routes.applicationGuildCommands(config.applicationId, config.guildId),
          { body: data }
        );

        if (Array.isArray(result)) {
          const length = result.length;
          console.log(`🟢 Successfully registered ${length} command` + (length > 1 ? "s" : ""));
        }
      } else {
        console.error("🔴 Global command registration is not implemented yet");
      }
    } catch (error) {
      console.error("🔴 Failed to register commands:", error);
    }
  }

  getCommand(interaction: ChatInputCommandInteraction) {
    const { commandName, options } = interaction;
    const subcommand = options.getSubcommand(false);

    if (subcommand) {
      const commandGroup = this.commandGroups.get(commandName);
      return commandGroup?.commands.get(subcommand);
    }

    return this.commands.get(commandName);
  }

  async start(token: string) {
    this.token = token;
    await this.load();
    await this.login(token);
  }
}
