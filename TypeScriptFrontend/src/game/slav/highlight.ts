import { IDItem } from "./Objects/idItem"; // Assume these are defined in the conversation// Assumed imports based on prior context
import { Node } from "./Objects/node"; // Assume this is defined
import { ClickType } from "./enums"; // Assume this is defined
import { AbilityVisual } from "./immutable_visuals"; // Assume this is defined
import { VISUALS } from "./default_abilities"; // Assume this is defined
import { Colors, KeyCodes } from "./constants";

export class Highlight {
    private graphics: Phaser.GameObjects.Graphics;
    item: IDItem | null = null;
    usage: number | null = null;

    constructor(scene: Phaser.Scene) {
        this.graphics = scene.add.graphics();
    }


    wipe(): void {
        this.item = null;
        this.usage = null;
        this.graphics.clear(); 
    }

    set(item: IDItem, usage: number): void {
        this.item = item;
        this.usage = usage;
    }

    get color(): readonly [number, number, number] {
        if (this.usage && this.usage !== KeyCodes.SPAWN_CODE) {
            const visual = VISUALS[this.usage] as AbilityVisual; // Assuming AbilityVisual has a color property
            return visual.color;
        }
        return Colors.GREY;
    }

    get type(): ClickType {
        if (this.item) {
            return this.item.type;
        }
        return ClickType.BLANK;
    }

    sendFormat(items?: number[], code?: number): object {
        const coda = code ?? this.usage;
        items = items || (this.item ? [this.item.id] : []);
        return { code, items };
    }

    draw(): void {
        if (this.item && this.item.type === ClickType.NODE) {
            const node = this.item as Node;
            const [r, g, b] = this.color;
            this.graphics.lineStyle(2, Phaser.Display.Color.GetColor(r, g, b), 1); // Set line color and alpha
            this.graphics.strokeCircle(node.pos.x, node.pos.y, node.value + 3); // Assuming `x`, `y` coordinates and radius
            this.graphics.closePath();
        }
    }
}