import { IDItem } from "./Objects/idItem"; // Assume these are defined in the conversation// Assumed imports based on prior context
import { Node } from "./Objects/node"; // Assume this is defined
import { Edge } from "./Objects/edge"; // Assume this is defined
import { ClickType } from "./enums"; // Assume this is defined
import { AbilityVisual } from "./immutable_visuals"; // Assume this is defined
import { VISUALS } from "./default_abilities"; // Assume this is defined
import { KeyCodes, EventCodes } from "./constants";
import { ReloadAbility } from "./Objects/ReloadAbility";

export class Highlight {
    private graphics: Phaser.GameObjects.Graphics;
    item: IDItem | null = null;
    usage: number | null = null;
    playerColor: readonly [number, number, number];
    alt_colored_item: Phaser.GameObjects.Image | null;

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
        const code_usage = code ?? this.usage;
        items = items || (this.item ? [this.item.id] : []);
        return { "code": code_usage, "items": items };
    }

    draw(): void {
        this.graphics.clear();
        if (this.alt_colored_item) {
            this.alt_colored_item.setTint(Phaser.Display.Color.GetColor(255, 102, 102));
            this.alt_colored_item = null;
        } 
        if (this.item) {
            if (this.type === ClickType.NODE) {
                const node = this.item as Node;
                const [r, g, b] = this.color;
                this.graphics.lineStyle(2, Phaser.Display.Color.GetColor(r, g, b), 1); // Set line color and alpha
                this.graphics.strokeCircle(node.pos.x, node.pos.y, node.size + 3); // Assuming `x`, `y` coordinates and radius
                this.graphics.closePath();
            } else if (this.type === ClickType.EDGE) {
                const edge = this.item as Edge;
                const [r, g, b] = this.color;
                this.graphics.lineStyle(2, Phaser.Display.Color.GetColor(r, g, b), 1); // Set line color and alpha
        
                const startX = edge.line.x1;
                const startY = edge.line.y1;
                const endX = edge.line.x2;
                const endY = edge.line.y2;
        
                const dx = endX - startX;
                const dy = endY - startY;
                const magnitude = Math.sqrt(dx * dx + dy * dy);
        
                // Normal vector components perpendicular to the line
                const perpX = -dy / magnitude;
                const perpY = dx / magnitude;
        
                const spacing = 6; // Distance to offset the parallel lines
        
                // Calculate positions for left and right lines using perpendicular vector
                const leftLine = new Phaser.Geom.Line(
                    startX + perpX * spacing,
                    startY + perpY * spacing,
                    endX + perpX * spacing,
                    endY + perpY * spacing
                );
                const rightLine = new Phaser.Geom.Line(
                    startX - perpX * spacing,
                    startY - perpY * spacing,
                    endX - perpX * spacing,
                    endY - perpY * spacing
                );
        
                // Draw the lines
                this.graphics.strokeLineShape(leftLine);
                this.graphics.strokeLineShape(rightLine);
                this.graphics.closePath();
            }
            else if (this.type === ClickType.ABILITY) {
                const ability = this.item as ReloadAbility;
                const [r, g, b] = this.color; // Your highlight color components
                const highlightColor = Phaser.Display.Color.GetColor(r, g, b);
                this.alt_colored_item = ability.pointerTriangle;
                // Set the tint of the pointerTriangle to highlight color
                ability.pointerTriangle.setTint(highlightColor);
            }
        }
    }
}