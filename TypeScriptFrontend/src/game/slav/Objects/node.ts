import { State } from "./States";
import { Colors, GROWTH_STOP } from "../constants";
import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "../enums";
import { phaserColor } from "../utilities";
import { CapitalState, CannonState } from "./States";

export class Node extends IDItem {
    pos: Phaser.Math.Vector2;
    isPort: boolean;
    portPercent: number;
    ports: Array<number>;
    state: State;
    value: number;
    effects: Set<string>;
    owner: OtherPlayer | null;
    private scene: Phaser.Scene;
    private graphics: Phaser.GameObjects.Graphics;
    private cannonGraphics: Phaser.GameObjects.Graphics;

    constructor(
        id: number,
        pos: [number, number],
        isPort: boolean,
        portPercent: number,
        ports: Array<any>,
        state: State,
        value: number,
        owner: OtherPlayer | null = null,
        effects = new Set<string>(),
        scene?: Phaser.Scene
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
        this.scene = scene;
        if (this.scene) {
            this.graphics = scene.add.graphics();
            this.cannonGraphics = scene.add.graphics();
        }
    }

    get color(): readonly [number, number, number] {
        if (!this.owner) {
            return this.isPort ? Colors.BROWN : Colors.BLACK;
        }
        return this.owner.color;
    }

    get phaserColor(): number {
        return phaserColor(this.color);
    }

    get size(): number {
        return 5 + this.sizeFactor * 18;
    }

    get sizeFactor(): number {
        if (this.value < 5) return 0;
        return Math.max(
            Math.log10(this.value / 10) / 2 + this.value / 1000 + 0.15,
            0
        );
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

    draw(): void {
        this.graphics.clear();
        if (this.stateName === "zombie") {
            // Handle drawing for zombie state
            this.graphics.fillStyle(this.phaserColor, 1); // Set the fill color for the rectangle
            this.graphics.fillRect(
                this.pos.x - this.size / 2,
                this.pos.y - this.size / 2,
                this.size,
                this.size
            );
            return; // Return early to prevent drawing the normal node graphics
        }

        if (this.effects.has("poison")) {
            this.graphics.lineStyle(6, phaserColor(Colors.PURPLE), 1);
            this.graphics.strokeCircle(this.pos.x, this.pos.y, this.size + 4);
        }

        if (this.owner) {
            if (this.isPort) {
                this.drawPorts(Colors.BROWN);
            } else if (this.ports.length > 0) {
                this.drawPorts(Colors.ORANGE);
            }
        }
        this.graphics.fillStyle(this.phaserColor, 1);
        this.graphics.fillCircle(this.pos.x, this.pos.y, this.size);

        if (this.effects.has("rage")) {
            this.graphics.lineStyle(3, phaserColor(Colors.DARK_GREEN), 1);
            this.graphics.strokeCircle(this.pos.x, this.pos.y, this.size - 2);
        }
        if (this.full) {
            this.graphics.lineStyle(2, phaserColor(Colors.BLACK), 1);
            this.graphics.strokeCircle(this.pos.x, this.pos.y, this.size + 1);
            if (this.stateName === "capital") {
                this.graphics.lineStyle(2, phaserColor(Colors.PINK), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size + 3
                );
            }
        }

        if (
            this.stateName === "capital" &&
            (this.state as CapitalState).capitalized
        ) {
            this.drawStar(this.graphics, phaserColor(Colors.BLACK), false);
            this.drawStar(this.graphics, phaserColor(Colors.PINK), true);
        } else if (this.state instanceof CannonState) {
            if (this.state.selected) {
                this.cannonGraphics.clear();
                let mousePos = this.scene.input.activePointer.position;
                // Calculate angle between the spot and the mouse cursor
                let dx = mousePos.x - this.pos.x;
                let dy = mousePos.y - this.pos.y;
                this.state.angle = Math.atan2(dy, dx) * (180 / Math.PI); // Angle in degrees
            }
            this.drawRotatedRectangle(
                this.state.angle,
                this.size * 2,
                this.size,
                Colors.GREY,
                this.cannonGraphics
            );
        }
    }

    drawPorts(color: readonly [number, number, number]): void {
        const portWidth = this.size;
        const portHeight = this.size * 1.3;
        this.ports.forEach((angle) => {
            this.drawRotatedRectangle(angle, portWidth, portHeight, color);
        });
    }

    drawRotatedRectangle(
        angle: number,
        portWidth: number,
        portHeight: number,
        col: readonly [number, number, number],
        graphics: Phaser.GameObjects.Graphics = this.graphics
    ): void {
        const rad = Phaser.Math.DegToRad(angle);
        const halfWidth = portWidth / 2;
        const halfHeight = portHeight / 2;
        const distanceFromCenter = this.size * 1.2; // Define how far each port should be from the center of the node

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
        ].map((corner) => {
            // Rotate and then translate each corner
            return corner.rotate(rad).add(portCenter);
        });

        // Change graphics fill style here if needed
        graphics.fillStyle(
            Phaser.Display.Color.GetColor(col[0], col[1], col[2]),
            1
        ); // Set the color to Orange

        // Draw the polygon
        graphics.beginPath();
        graphics.moveTo(corners[0].x, corners[0].y);
        corners.forEach((corner, index) => {
            if (index > 0) graphics.lineTo(corner.x, corner.y);
        });
        graphics.closePath();
        graphics.fillPath();
    }

    drawStar(
        graphics: Phaser.GameObjects.Graphics,
        color: number,
        filled: boolean = true
    ): void {
        const innerRadius = this.size / 3;
        const outerRadius = this.size / 1.5;
        const starPoints = [];

        for (let i = 0; i < 5; i++) {
            // Outer points
            let angle = Phaser.Math.DegToRad(i * 72 + 55); // Start at top point
            starPoints.push(
                new Phaser.Math.Vector2(
                    this.pos.x + outerRadius * Math.cos(angle),
                    this.pos.y + outerRadius * Math.sin(angle)
                )
            );

            // Inner points
            angle += Phaser.Math.DegToRad(36); // Halfway between outer points
            starPoints.push(
                new Phaser.Math.Vector2(
                    this.pos.x + innerRadius * Math.cos(angle),
                    this.pos.y + innerRadius * Math.sin(angle)
                )
            );
        }

        // Draw the star
        graphics.beginPath();
        graphics.fillStyle(color, 1);
        graphics.moveTo(starPoints[0].x, starPoints[0].y);
        starPoints.forEach((point, index) => {
            if (index > 0) graphics.lineTo(point.x, point.y);
        });
        graphics.closePath();

        if (filled) {
            graphics.fillPath();
        } else {
            graphics.lineStyle(1, color);
            graphics.strokePath();
        }
    }
}

