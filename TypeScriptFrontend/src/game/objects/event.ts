import { EventVisual } from "./immutable_visuals"; // Assuming these are defined
import { ClickType } from "./enums"; // Assuming this is defined
import { ValidationFunction } from "./types"; // Assuming this is defined


export class Event {
    visual: EventVisual;
    clickCount: number;
    clickType: ClickType;
    verificationFunc: ValidationFunction;
    addons: any = {};

    constructor(visual: EventVisual, clickCount: number, clickType: ClickType, verificationFunc: ValidationFunction, addons: Set<number> = new Set<number>()) {
        this.visual = visual;
        this.clickCount = clickCount;
        this.clickType = clickType;
        this.verificationFunc = verificationFunc;
        this.addons = addons;
    }
}