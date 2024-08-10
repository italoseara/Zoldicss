"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
exports.Test2View = exports.TestView = void 0;
const core_1 = require("../../core");
const discord_js_1 = require("discord.js");
class TestView extends core_1.View {
    select(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            const selected = interaction.values.join(", ");
            interaction.reply({
                content: `You selected: ${selected}`,
                ephemeral: true,
            });
        });
    }
}
exports.TestView = TestView;
__decorate([
    (0, core_1.select)({
        customId: "selectme",
        placeholder: "Select Me",
        options: [
            { label: "Option 1", value: "1", description: "Option 1 description", emoji: "🍔" },
            { label: "Option 2", value: "2", description: "Option 2 description", emoji: "🍟" },
            { label: "Option 3", value: "3", description: "Option 3 description", emoji: "🍕" },
        ],
    }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [discord_js_1.StringSelectMenuInteraction]),
    __metadata("design:returntype", Promise)
], TestView.prototype, "select", null);
class Test2View extends core_1.View {
    button1(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            interaction.reply({
                content: "Button 1 clicked!",
                ephemeral: true,
            });
        });
    }
    button2(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            interaction.reply({
                content: "Button 2 clicked!",
                ephemeral: true,
            });
        });
    }
    button3(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            interaction.reply({
                content: "Button 3 clicked!",
                ephemeral: true,
            });
        });
    }
}
exports.Test2View = Test2View;
__decorate([
    (0, core_1.button)({
        customId: "button1",
        label: "Button 1",
        emoji: "🍔",
    }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [discord_js_1.ButtonInteraction]),
    __metadata("design:returntype", Promise)
], Test2View.prototype, "button1", null);
__decorate([
    (0, core_1.button)({
        customId: "button2",
        label: "Button 2",
        emoji: "🍟",
        style: discord_js_1.ButtonStyle.Danger,
    }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [discord_js_1.ButtonInteraction]),
    __metadata("design:returntype", Promise)
], Test2View.prototype, "button2", null);
__decorate([
    (0, core_1.button)({
        customId: "button3",
        label: "Button 3",
        emoji: "🍕",
        style: discord_js_1.ButtonStyle.Secondary,
    }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [discord_js_1.ButtonInteraction]),
    __metadata("design:returntype", Promise)
], Test2View.prototype, "button3", null);
