import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "../enums";
import { Node } from "./node";
import { Colors } from "../constants";

export class Edge extends IDItem {
    fromNode: Node;
    toNode: Node;
    dynamic: boolean;
    on: boolean;
    flowing: boolean;
    graphics: Phaser.GameObjects.Graphics;
    line: Phaser.Geom.Line;

    constructor(scene: Phaser.Scene, id: number, fromNode: Node, toNode: Node, dynamic: boolean, on = false, flowing = false) {
        super(id, ClickType.EDGE); // Example ID logic
        this.fromNode = fromNode;
        this.toNode = toNode;
        this.dynamic = dynamic;
        this.on = on;
        this.flowing = flowing;
        this.graphics = scene.add.graphics();
        this.line = new Phaser.Geom.Line(fromNode.pos.x, fromNode.pos.y, toNode.pos.x, toNode.pos.y);
    }

    get color(): readonly [number, number, number] {
        if (this.fromNode.effects.has('rage')) {
            return Colors.GREEN;
        }
        return this.on ? this.fromNode.color : [50, 50, 50];
    }

    controlledBy(player: OtherPlayer): boolean {
        return this.fromNode.owner === player || (this.dynamic && this.toNode.owner === player && this.toNode.full);
    }

    other(node: Node): Node {
        if (node === this.fromNode) {
            return this.toNode;
        } else if (node === this.toNode) {
            return this.fromNode;
        }
        throw new Error("Node not in edge");
    }

    get phaserColor(): number {
        const col = this.color;
        return Phaser.Display.Color.GetColor(col[0], col[1], col[2]);
    }

    
    draw(): void {

        const startX = this.fromNode.pos.x;
        const startY = this.fromNode.pos.y;
        const endX = this.toNode.pos.x;
        const endY = this.toNode.pos.y;
        
        const dx = endX - startX;
        const dy = endY - startY;
        const magnitude = Math.sqrt(dx * dx + dy * dy);

        const normX = dx / magnitude;
        const normY = dy / magnitude;

        const color = this.phaserColor;

        if (!this.dynamic) {
            // Draw Arrow
            this.drawArrow(startX, startY, normX, normY, magnitude, color);
        } else {
            // Draw Circles
            this.drawCircle(startX, startY, normX, normY, magnitude, color);
        }
    }

    drawArrow(startX: number, startY: number, normX: number, normY: number, magnitude: number, color: number): void {
        const triangleSize = 11;
        const minSpacing = 11;

        const numTriangles = Math.floor((magnitude - 2 * triangleSize) / minSpacing);
        const spacing = (magnitude - 2 * triangleSize) / numTriangles;

        for (let i = 1; i <= numTriangles; i++) {
            let x = startX + i * spacing * normX + triangleSize * normX;
            let y = startY + i * spacing * normY + triangleSize * normY;
            let angle = Math.atan2(normY, normX);

            this.graphics.beginPath();
            this.graphics.moveTo(x, y);
            this.graphics.lineTo(x - Math.cos(angle - Math.PI / 6) * triangleSize, y - Math.sin(angle - Math.PI / 6) * triangleSize);
            this.graphics.lineTo(x - Math.cos(angle + Math.PI / 6) * triangleSize, y - Math.sin(angle + Math.PI / 6) * triangleSize);
            this.graphics.closePath();

            if (this.flowing) {
                this.graphics.fillStyle(color);
                this.graphics.fillPath();
            } else {
                let point1 = { x, y };
                let point2 = {
                    x: x - Math.cos(angle - Math.PI / 6) * triangleSize,
                    y: y - Math.sin(angle - Math.PI / 6) * triangleSize
                };
                let point3 = {
                    x: x - Math.cos(angle + Math.PI / 6) * triangleSize,
                    y: y - Math.sin(angle + Math.PI / 6) * triangleSize
                };
                this.graphics.lineStyle(1, color); // Set stroke style
                this.graphics.beginPath();
                this.graphics.moveTo(point1.x, point1.y);
                this.graphics.lineTo(point2.x, point2.y);
                this.graphics.lineTo(point3.x, point3.y);
                this.graphics.closePath();
                this.graphics.strokePath();
            }
        }
        }
        

    drawCircle(startX: number, startY: number, normX: number, normY: number, magnitude: number, color: number): void {
        const circleRadius = 3;
        const minSpacing = 8;
        const triangleSize = 13;
    
        const numCircles = Math.floor((magnitude - 2 * circleRadius) / minSpacing);
        const spacing = (magnitude - 2 * circleRadius) / numCircles;
    
        for (let i = 1; i < numCircles - 1; i++) {
            let x = startX + i * spacing * normX + circleRadius * normX;
            let y = startY + i * spacing * normY + circleRadius * normY;
    
            this.graphics.beginPath();
            this.graphics.arc(x, y, circleRadius, 0, 2 * Math.PI);
    
            if (this.flowing) {
                this.graphics.fillStyle(color);
                this.graphics.fillPath();
            } else {
                this.graphics.lineStyle(1, color); // Set stroke style
                this.graphics.strokeCircle(x, y, circleRadius);
            }
        }

        let x = startX + (numCircles) * spacing * normX;
        let y = startY + (numCircles) * spacing * normY;
        let angle = Math.atan2(normY, normX);

        this.graphics.fillStyle(Phaser.Display.Color.GetColor(153, 255, 51)); // Light green
        this.graphics.fillTriangle(
            x, y,
            x - Math.cos(angle - Math.PI / 6) * triangleSize, y - Math.sin(angle - Math.PI / 6) * triangleSize,
            x - Math.cos(angle + Math.PI / 6) * triangleSize, y - Math.sin(angle + Math.PI / 6) * triangleSize
        );
    }

    isNear(position: Phaser.Math.Vector2): boolean {
        const pointerCircle = new Phaser.Geom.Circle(position.x, position.y, 10); // 10 pixels radius
        return Phaser.Geom.Intersects.LineToCircle(this.line, pointerCircle);
    }
}