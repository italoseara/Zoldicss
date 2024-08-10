"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
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
const discord_js_1 = require("discord.js");
const core_1 = require("../core");
let InteractionCreate = class InteractionCreate extends core_1.Event {
    handleSlashCommand(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            var _a;
            const bot = interaction.client;
            const { commandName, user, options } = interaction;
            const subcommand = options.getSubcommand(false);
            const executed = subcommand ? `/${commandName} ${subcommand}` : `/${commandName}`;
            console.log(`🔔 @${user.tag} executed command: ${executed}`);
            const command = bot.getCommand(interaction);
            if (!command) {
                console.error("🔴 Command not found:", executed);
                return;
            }
            try {
                const instance = new command();
                const commandOptions = Reflect.getMetadata("discord:command", command).options || [];
                for (const option of commandOptions) {
                    const value = (_a = options[`get${option.type}`](option.name)) !== null && _a !== void 0 ? _a : option.default;
                    instance[option.name] = value;
                }
                yield instance.execute(interaction);
            }
            catch (error) {
                console.error("🔴 Error while executing command:", commandName, error);
                interaction.reply({
                    content: "❌ There was an error while executing this command.",
                    ephemeral: true,
                });
            }
        });
    }
    handleComponent(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            const bot = interaction.client;
            const { user, customId } = interaction;
            const callback = bot.components.get(customId);
            if (!callback) {
                console.error("🔴 Component callback not found:", customId);
                interaction.reply({
                    content: "❌ This component is not working.",
                    ephemeral: true,
                });
                return;
            }
            console.log(`🔔 @${user.tag} interacted with a component: ${customId}`);
            callback(interaction);
        });
    }
    execute(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            if (interaction.isChatInputCommand()) {
                yield this.handleSlashCommand(interaction);
            }
            else if (interaction.isButton() || interaction.isStringSelectMenu()) {
                yield this.handleComponent(interaction);
            }
        });
    }
};
InteractionCreate = __decorate([
    (0, core_1.event)({ name: discord_js_1.Events.InteractionCreate })
], InteractionCreate);
exports.default = InteractionCreate;
