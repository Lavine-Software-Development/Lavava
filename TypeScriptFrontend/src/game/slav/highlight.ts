import { IDItem } from "./Objects/idItem"; // Assume these are defined in the conversation// Assumed imports based on prior context
import { Node } from "./Objects/node"; // Assume this is defined
import { Edge } from "./Objects/edge"; // Assume this is defined
import { ClickType } from "./enums"; // Assume this is defined
import { AbilityVisual } from "./immutable_visuals"; // Assume this is defined
import { VISUALS } from "./default_abilities"; // Assume this is defined
import { KeyCodes, EventCodes } from "./constants";

export class Highlight {
    private graphics: Phaser.GameObjects.Graphics;
    item: IDItem | null = null;
    usage: number | null = null;
    playerColor: readonly [number, number, number];

    constructor(scene: Phaser.Scene, playerColor: readonly [number, number, number]) {
        this.graphics = scene.add.graphics();
        this.playerColor = playerColor;
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

    get highlighted(): boolean {
        return !!this.item;
    }

    get color(): readonly [number, number, number] {
        if (this.usage && this.usage !== KeyCodes.SPAWN_CODE) {
            const visual = VISUALS[this.usage] as AbilityVisual; // Assuming AbilityVisual has a color property
            return visual.color;
        }
        return this.playerColor;
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
        return { coda, items };
    }

    draw(): void {
        if (this.item) {
            if (this.type === ClickType.NODE) {
                const node = this.item as Node;
                const [r, g, b] = this.color;
                this.graphics.lineStyle(2, Phaser.Display.Color.GetColor(r, g, b), 1); // Set line color and alpha
                this.graphics.strokeCircle(node.pos.x, node.pos.y, node.value + 3); // Assuming `x`, `y` coordinates and radius
                this.graphics.closePath();
            } else if (this.type === ClickType.EDGE) {
                const edge = this.item as Edge;
                const [r, g, b] = this.color;
                this.graphics.lineStyle(2, Phaser.Display.Color.GetColor(r, g, b), 1); // Set line color and alpha
                const leftLine = new Phaser.Geom.Line(edge.line.x1 - 6, edge.line.y1, edge.line.x2 - 6, edge.line.y2);
                const rightLine = new Phaser.Geom.Line(edge.line.x1 + 6, edge.line.y1, edge.line.x2 + 6, edge.line.y2);
                this.graphics.strokeLineShape(leftLine);
                this.graphics.strokeLineShape(rightLine);
                this.graphics.closePath();
            }
        }
    }
}