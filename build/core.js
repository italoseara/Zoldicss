"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Event = exports.SlashCommand = exports.CommandGroup = exports.View = void 0;
exports.button = button;
exports.select = select;
exports.event = event;
exports.command = command;
exports.option = option;
require("reflect-metadata");
const discord_js_1 = require("discord.js");
// ========================
//      User Interface
// ========================
function button(info) {
    return (target, _key, descriptor) => {
        const components = Reflect.getMetadata("discord:components", target.constructor) || [];
        info.style = info.style || discord_js_1.ButtonStyle.Primary;
        info.disabled = info.disabled || false;
        components.push(Object.assign(Object.assign({}, info), { type: "Button", execute: descriptor.value }));
        Reflect.defineMetadata("discord:components", components, target.constructor);
    };
}
function select(info) {
    return (target, _key, descriptor) => {
        const components = Reflect.getMetadata("discord:components", target.constructor) || [];
        info.disabled = info.disabled || false;
        info.minValues = info.minValues || 1;
        info.maxValues = info.maxValues || 1;
        components.push(Object.assign(Object.assign({}, info), { type: "StringSelect", execute: descriptor.value }));
        Reflect.defineMetadata("discord:components", components, target.constructor);
    };
}
class View extends discord_js_1.ActionRowBuilder {
    constructor() {
        super();
        const meta = Reflect.getMetadata("discord:components", this.constructor) || [];
        for (const component of meta) {
            if (component.type === "Button") {
                const button = new discord_js_1.ButtonBuilder()
                    .setCustomId(component.customId)
                    .setLabel(component.label)
                    .setStyle(component.style)
                    .setDisabled(component.disabled);
                if (component.emoji)
                    button.setEmoji(component.emoji);
                this.addComponents(button);
            }
            else if (component.type === "StringSelect") {
                const select = new discord_js_1.StringSelectMenuBuilder()
                    .setCustomId(component.customId)
                    .setPlaceholder(component.placeholder)
                    .setDisabled(component.disabled)
                    .setMinValues(component.minValues)
                    .setMaxValues(component.maxValues)
                    .addOptions(component.options.map((option) => {
                    const selectOption = new discord_js_1.StringSelectMenuOptionBuilder()
                        .setLabel(option.label)
                        .setValue(option.value);
                    if (option.description)
                        selectOption.setDescription(option.description);
                    if (option.emoji)
                        selectOption.setEmoji(option.emoji);
                    if (option.default)
                        selectOption.setDefault();
                    return selectOption;
                }));
                this.addComponents(select);
            }
        }
    }
}
exports.View = View;
// ========================
//      Slash Commands
// ========================
class CommandGroup {
    constructor(info) {
        this.commands = new Map();
        this.name = info.name;
        this.description = info.description;
        this.permissions = info.permissions;
    }
    subcommand(info) {
        return (target) => {
            const meta = Reflect.getMetadata("discord:command", target) || {};
            Reflect.defineMetadata("discord:command", Object.assign(Object.assign({}, meta), info), target);
            this.commands.set(info.name, target);
        };
    }
}
exports.CommandGroup = CommandGroup;
class SlashCommand {
}
exports.SlashCommand = SlashCommand;
class Event {
}
exports.Event = Event;
function event(info) {
    return (target) => {
        const meta = Reflect.getMetadata("discord:event", target) || {};
        Reflect.defineMetadata("discord:event", Object.assign(Object.assign({}, meta), info), target);
    };
}
function command(info) {
    return function (target) {
        const meta = Reflect.getMetadata("discord:command", target) || {};
        Reflect.defineMetadata("discord:command", Object.assign(Object.assign({}, meta), info), target);
    };
}
function option(info) {
    return (target, key) => {
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
        Reflect.defineMetadata("discord:command", Object.assign(Object.assign({}, meta), { options }), target.constructor);
    };
}
