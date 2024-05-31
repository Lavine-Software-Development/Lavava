import { State } from "../States";
import { Colors, GROWTH_STOP } from "../constants";
import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "../enums";

export class Node extends IDItem {
    pos: Phaser.Math.Vector2;
    isPort: boolean;
    portPercent: number;
    ports: Array<number>; 
    state: State;
    value: number;
    effects: Set<string>; 
    owner: OtherPlayer | null;

    constructor(
        id: number, pos: [number, number], isPort: boolean,
        portPercent: number, ports: Array<any>, state: State, value: number,
        owner: OtherPlayer | null = null, effects = new Set<string>() 
    ) {
        super(id, ClickType.NODE);
        this.pos = new Phaser.Math.Vector2(pos[0], pos[1]);
        this.isPort = isPort;
        this.portPercent = portPercent;
        this.ports = ports;
        this.state = state;
        this.value = value;
        this.effects = effects;
        this.owner = owner;
    }

    get color(): readonly [number, number, number] {
        if (!this.owner) {
            return this.isPort ? Colors.BROWN : Colors.BLACK;
        }
        return this.owner.color;
    }

    get phaserColor(): number {
        const col = this.color;
        return Phaser.Display.Color.GetColor(col[0], col[1], col[2]);
    }

    get size(): number {
        return 5 + this.sizeFactor * 18;
    }

    get sizeFactor(): number {
        if (this.value < 5) return 0;
        return Math.max(Math.log10(this.value / 10) / 2 + this.value / 1000 + 0.15, 0);
    }

    get stateName(): string {
        return this.state.name;
    }

    get full(): boolean {
        return this.value >= GROWTH_STOP;
    }

    get portCount(): number {
        return this.ports.length;
    }

    draw(scene: Phaser.Scene): void {
        let graphics = scene.add.graphics(); 
        if (this.owner) {
            if (this.isPort) {
                this.drawPorts(graphics, Colors.BROWN);
            } else if (this.ports.length > 0) {
                this.drawPorts(graphics, Colors.ORANGE);
            }
        }
        graphics.fillStyle(this.phaserColor, 1);
        graphics.fillCircle(this.pos.x, this.pos.y, this.size);
    }

    drawPorts(graphics: Phaser.GameObjects.Graphics, color: readonly [number, number, number]): void {
        const portWidth = this.size;
        const portHeight = this.size * 1.3;
        this.ports.forEach(angle => {
            this.drawRotatedRectangle(graphics, angle, portWidth, portHeight, color);
        });
    }

    drawRotatedRectangle(graphics: Phaser.GameObjects.Graphics, angle: number, portWidth: number, portHeight: number, col: readonly [number, number, number]): void {
        const rad = Phaser.Math.DegToRad(angle);
        const halfWidth = portWidth / 2;
        const halfHeight = portHeight / 2;
        const distanceFromCenter = this.size * 1.2;  // Define how far each port should be from the center of the node

        const portCenter = new Phaser.Math.Vector2(
            this.pos.x + Math.cos(rad) * distanceFromCenter,
            this.pos.y + Math.sin(rad) * distanceFromCenter
        );
    
        // Calculate the corners of the rotated rectangle
        const corners = [
            new Phaser.Math.Vector2(-halfWidth, -halfHeight),
            new Phaser.Math.Vector2(halfWidth, -halfHeight),
            new Phaser.Math.Vector2(halfWidth, halfHeight),
            new Phaser.Math.Vector2(-halfWidth, halfHeight),
        ].map(corner => {
            // Rotate and then translate each corner
            return corner.rotate(rad).add(portCenter);
        });
    
        // Change graphics fill style here if needed
        graphics.fillStyle(Phaser.Display.Color.GetColor(col[0], col[1], col[2]), 1); // Set the color to Orange
    
        // Draw the polygon
        graphics.beginPath();
        graphics.moveTo(corners[0].x, corners[0].y);
        corners.forEach((corner, index) => {
            if (index > 0) graphics.lineTo(corner.x, corner.y);
        });
        graphics.closePath();
        graphics.fillPath();
    }
    
}