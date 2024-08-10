"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
require("reflect-metadata");
const config = __importStar(require("./config/config.json"));
const utils_1 = require("./utils");
const core_1 = require("./core");
const discord_js_1 = require("discord.js");
class Bot extends discord_js_1.Client {
    constructor() {
        super({
            intents: [
                discord_js_1.GatewayIntentBits.Guilds,
                discord_js_1.GatewayIntentBits.GuildMembers,
                discord_js_1.GatewayIntentBits.GuildMessages,
                discord_js_1.GatewayIntentBits.GuildModeration,
                discord_js_1.GatewayIntentBits.MessageContent,
                discord_js_1.GatewayIntentBits.GuildIntegrations,
            ],
        });
        this.commands = new Map();
        this.commandGroups = new Map();
        this.components = new Map();
    }
    load() {
        return __awaiter(this, void 0, void 0, function* () {
            const views = [];
            const events = [];
            const commands = [];
            const commandGroups = [];
            const files = (0, utils_1.getFiles)(".").filter((file) => file.endsWith(".js"));
            for (const path of files) {
                const exported = Object.values(require(path));
                if (!exported)
                    continue;
                for (const module of exported) {
                    if (module.prototype instanceof core_1.View)
                        views.push(module);
                    else if (module.prototype instanceof core_1.Event)
                        events.push(module);
                    else if (module.prototype instanceof core_1.SlashCommand)
                        commands.push(module);
                    else if (module instanceof core_1.CommandGroup)
                        commandGroups.push(module);
                }
            }
            yield this.loadCommands(commands, commandGroups);
            yield this.loadEvents(events);
            yield this.loadComponents(views);
        });
    }
    loadComponents(views) {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("🔧 Loading components...");
            for (const ViewClass of views) {
                const components = Reflect.getMetadata("discord:components", ViewClass);
                for (const component of components) {
                    const { customId, execute, type } = component;
                    if (this.components.has(customId)) {
                        console.log(`🔴 Skipping duplicate component: ${customId} (${type})`);
                        continue;
                    }
                    this.components.set(customId, execute);
                    console.log(`🟢 Loaded component: ${customId} (${type})`);
                }
            }
            console.log();
        });
    }
    loadEvents(events) {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("🔧 Loading events...");
            for (const EventClass of events) {
                const meta = Reflect.getMetadata("discord:event", EventClass);
                this[meta.once ? "once" : "on"](meta.name, (...args) => __awaiter(this, void 0, void 0, function* () {
                    const instance = new EventClass();
                    instance.execute(...args);
                }));
                console.log(`🟢 Loaded event: ${meta.name}`);
            }
            console.log();
        });
    }
    loadCommands(commands, commandGroups) {
        return __awaiter(this, void 0, void 0, function* () {
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
            yield this.registerCommands();
            console.log();
        });
    }
    registerCommands() {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                if (config.devMode) {
                    const data = [];
                    // Build the commands
                    for (const [_, command] of this.commands) {
                        const meta = Reflect.getMetadata("discord:command", command);
                        const builder = new discord_js_1.SlashCommandBuilder()
                            .setName(meta.name)
                            .setDescription(meta.description);
                        if (meta.permissions)
                            builder.setDefaultMemberPermissions(meta.permissions);
                        if (meta.options) {
                            for (const option of meta.options) {
                                const { type, name, description, required, choices } = option;
                                builder[`add${type}Option`]((option) => {
                                    option.setName(name).setDescription(description).setRequired(required);
                                    if (choices.length > 0)
                                        option.addChoices(choices);
                                    return option;
                                });
                            }
                        }
                        data.push(builder.toJSON());
                    }
                    // Build the command groups
                    for (const [_, commandGroup] of this.commandGroups) {
                        const builder = new discord_js_1.SlashCommandBuilder()
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
                                            if (choices.length > 0)
                                                option.addChoices(choices);
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
                    const rest = new discord_js_1.REST().setToken(this.token);
                    const result = yield rest.put(discord_js_1.Routes.applicationGuildCommands(config.applicationId, config.guildId), { body: data });
                    if (Array.isArray(result)) {
                        const length = result.length;
                        console.log(`🟢 Successfully registered ${length} command` + (length > 1 ? "s" : ""));
                    }
                }
                else {
                    console.error("🔴 Global command registration is not implemented yet");
                }
            }
            catch (error) {
                console.error("🔴 Failed to register commands:", error);
            }
        });
    }
    getCommand(interaction) {
        const { commandName, options } = interaction;
        const subcommand = options.getSubcommand(false);
        if (subcommand) {
            const commandGroup = this.commandGroups.get(commandName);
            return commandGroup === null || commandGroup === void 0 ? void 0 : commandGroup.commands.get(subcommand);
        }
        return this.commands.get(commandName);
    }
    start(token) {
        return __awaiter(this, void 0, void 0, function* () {
            this.token = token;
            yield this.load();
            yield this.login(token);
        });
    }
}
exports.default = Bot;
