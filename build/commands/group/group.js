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
const core_1 = require("../../core");
const test_1 = require("./test");
const group = new core_1.CommandGroup({ name: "group", description: "Example group" });
let Subcommand = class Subcommand extends core_1.SlashCommand {
    execute(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            interaction.reply("Subcommand executed!");
        });
    }
};
Subcommand = __decorate([
    group.subcommand({
        name: "subcommand",
        description: "Example subcommand",
    })
], Subcommand);
let Subcommand2 = class Subcommand2 extends core_1.SlashCommand {
    execute(interaction) {
        return __awaiter(this, void 0, void 0, function* () {
            interaction.reply({
                content: "Subcommand 2 executed!",
                components: [new test_1.TestView(), new test_1.Test2View()],
            });
        });
    }
};
Subcommand2 = __decorate([
    group.subcommand({
        name: "subcommand2",
        description: "Example subcommand 2",
    })
], Subcommand2);
exports.default = group;
