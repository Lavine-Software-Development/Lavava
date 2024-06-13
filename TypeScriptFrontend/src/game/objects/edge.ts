import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "./enums";
import { Node } from "./node";
import { Colors } from "./constants";

export class Edge extends IDItem {
    fromNode: Node;
    toNode: Node;
    dynamic: boolean;
    on: boolean;
    flowing: boolean;
    line: Phaser.Geom.Line;
    hover_line: Phaser.Geom.Line;
    graphics: Phaser.GameObjects.Graphics;
    my_scene: Phaser.Scene;
    sprites: Phaser.GameObjects.Sprite[];
    spacing: number;

    constructor(
        id: number,
        fromNode: Node,
        toNode: Node,
        dynamic: boolean,
        on = false,
        flowing = false,
        _scene?: Phaser.Scene
    ) {
        super(id, ClickType.EDGE); // Example ID logic
        this.fromNode = fromNode;
        this.toNode = toNode;
        this.dynamic = dynamic;
        this.on = on;
        this.flowing = flowing;
        if (_scene) {
            this.my_scene = _scene;
            this.graphics = _scene.add.graphics();
        }
        this.line = new Phaser.Geom.Line(
            fromNode.pos.x,
            fromNode.pos.y,
            toNode.pos.x,
            toNode.pos.y
        );
        this.hover_line = new Phaser.Geom.Line(
            fromNode.pos.x,
            fromNode.pos.y,
            toNode.pos.x,
            toNode.pos.y
        );

        this.sprites = [];
        this.spacing = 0;
    }

    get color(): readonly [number, number, number] {
        if (this.fromNode.effects.has("rage")) {
            return Colors.GREEN;
        }
        return this.on ? this.fromNode.color : [50, 50, 50];
    }

    controlledBy(player: OtherPlayer): boolean {
        return (
            this.fromNode.owner === player ||
            (this.dynamic && this.toNode.owner === player && this.toNode.full)
        );
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
    set scene(scene: Phaser.Scene) {
        this.my_scene = scene;
        this.graphics = scene.add.graphics();
    }

    clearSprites(): void {
        // Clear existing sprites from the scene
        this.sprites.forEach((sprite) => {
            sprite.destroy();
        });
        this.sprites = []; // Reset the sprite storage
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

        // Calculate adjusted starting coordinates
        const adjustedStartX = startX + normX * this.fromNode.size;
        const adjustedStartY = startY + normY * this.fromNode.size;

        // Adjust the magnitude for both node sizes
        const adjustedMagnitude =
            magnitude - (this.toNode.size + this.fromNode.size);

        // update this.hover_line to start at the adjusted values and be magnitude long

        const shorterStartX = adjustedStartX + normX * adjustedMagnitude * 0.15; // Move start point inwards
        const shorterStartY = adjustedStartY + normY * adjustedMagnitude * 0.15;
        const shorterEndX = adjustedStartX + normX * adjustedMagnitude * 0.85; // Move end point inwards
        const shorterEndY = adjustedStartY + normY * adjustedMagnitude * 0.85;

        this.hover_line.setTo(
            shorterStartX,
            shorterStartY,
            shorterEndX,
            shorterEndY
        );

        const color = this.phaserColor;

        if (!this.dynamic) {
            // Draw Arrow from adjusted start point to the adjusted length
            this.drawArrow(
                adjustedStartX,
                adjustedStartY,
                normX,
                normY,
                adjustedMagnitude,
                color
            );
        } else {
            // Draw Circles from adjusted start point to the adjusted length
            this.drawCircle(
                adjustedStartX,
                adjustedStartY,
                normX,
                normY,
                adjustedMagnitude,
                color
            );
        }
    }

    drawArrow(
        startX: number,
        startY: number,
        normX: number,
        normY: number,
        magnitude: number,
        color: number
    ): void {
        const triangleSize = 11;
        const minSpacing = 13;

        const numTriangles = Math.floor(magnitude / minSpacing);
        const spacing = magnitude / numTriangles;
        let angle = Math.atan2(normY, normX) - Math.PI / 2;

        if (this.sprites.length !== numTriangles) {
            // Adjust the number of sprites if the count has changed
            if (this.sprites.length < numTriangles) {
                // Add more sprites
                for (let i = this.sprites.length; i < numTriangles; i++) {
                    let triangleSprite = this.my_scene.add.sprite(
                        0,
                        0,
                        this.flowing ? "filledTriangle" : "outlinedTriangle"
                    );
                    triangleSprite.setRotation(angle);
                    triangleSprite.setTint(color);
                    this.sprites.push(triangleSprite);
                }
            } else {
                // Remove excess sprites
                while (this.sprites.length > numTriangles) {
                    let sprite = this.sprites.pop();
                    sprite.destroy();
                }
            }
        }

        // Update positions of existing sprites
        for (let i = 0; i < numTriangles; i++) {
            let triangleSprite = this.sprites[i];
            if (spacing != this.spacing) {
                let x = startX + i * spacing * normX + triangleSize * normX;
                let y = startY + i * spacing * normY + triangleSize * normY;

                triangleSprite.x = x;
                triangleSprite.y = y;
            }
            // Adjust properties only if needed
            triangleSprite.setTint(color);
        }

        this.spacing = spacing;
    }

    drawCircle(
        startX: number,
        startY: number,
        normX: number,
        normY: number,
        magnitude: number,
        color: number
    ): void {
        const circleRadius = 3;
        const minSpacing = 8;

        const numCircles = Math.floor(
            (magnitude - 2 * circleRadius) / minSpacing
        );
        const spacing = (magnitude - 2 * circleRadius) / numCircles;

        // Initialize the triangle sprite if not already present or if there are no sprites at all
        if (
            this.sprites.length === 0 ||
            this.sprites[this.sprites.length - 1].texture.key !==
                "filledTriangle"
        ) {
            // First, clear any inappropriate sprites
            this.sprites.forEach((sprite) => sprite.destroy());
            this.sprites = [];

            // Then, populate the array correctly
            for (let i = 0; i < numCircles; i++) {
                let circleSprite = this.my_scene.add.sprite(
                    0,
                    0,
                    this.flowing ? "filledCircle" : "outlinedCircle"
                );
                circleSprite.setTint(color);
                this.sprites.push(circleSprite);
            }
            // Add the triangle sprite at the end
            let triangleSprite = this.my_scene.add.sprite(
                0,
                0,
                "filledTriangle"
            );
            triangleSprite.setTint(Phaser.Display.Color.GetColor(153, 255, 51));
            this.sprites.push(triangleSprite);
        } else {
            // Adjust sprite array if necessary
            while (this.sprites.length - 1 > numCircles) {
                let spriteToRemove = this.sprites.shift();
                spriteToRemove.destroy();
            }
            while (this.sprites.length - 1 < numCircles) {
                let circleSprite = this.my_scene.add.sprite(
                    0,
                    0,
                    this.flowing ? "filledCircle" : "outlinedCircle"
                );
                circleSprite.setTint(color);
                this.sprites.unshift(circleSprite); // Add to the start
            }
        }

        // Update positions of existing circle sprites
        for (let i = 1; i < numCircles; i++) {
            let circleSprite = this.sprites[i];
            if (spacing != this.spacing) {
                let x = startX + (i + 1) * spacing * normX;
                let y = startY + (i + 1) * spacing * normY;

                circleSprite.x = x;
                circleSprite.y = y;
            }
            circleSprite.setTint(color);
        }

        // Always update the position and properties of the terminal triangle sprite
        let triangleSprite = this.sprites[this.sprites.length - 1];
        triangleSprite.setTint(Phaser.Display.Color.GetColor(153, 255, 51));
        if (spacing != this.spacing) {
            let x = startX + spacing * normX;
            let y = startY + spacing * normY;
            let angle = Math.atan2(normY, normX);

            triangleSprite.x = x;
            triangleSprite.y = y;
            triangleSprite.setRotation(angle - Math.PI / 2);
        }

        this.spacing = spacing;
    }

    isNear(position: Phaser.Math.Vector2): boolean {
        const pointerCircle = new Phaser.Geom.Circle(
            position.x,
            position.y,
            10
        ); // 10 pixels radius
        return Phaser.Geom.Intersects.LineToCircle(
            this.hover_line,
            pointerCircle
        );
    }
}

