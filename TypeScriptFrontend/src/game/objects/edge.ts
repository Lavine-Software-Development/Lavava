import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "./enums";
import { Node } from "./node";
import { Colors } from "./constants";
import { phaserColor } from "./utilities";

export class Edge extends IDItem {
    private _fromNode: Node;
    private _toNode: Node;
    private _dynamic: boolean;
    on: boolean;
    private _flowing: boolean;
    line: Phaser.Geom.Line;
    hover_line: Phaser.Geom.Line;
    graphics: Phaser.GameObjects.Graphics;
    my_scene: Phaser.Scene;
    sprites: Phaser.GameObjects.Sprite[];
    spacing: number;
    redraw: boolean;

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
        this._fromNode = fromNode;
        this._toNode = toNode;
        this._dynamic = dynamic;
        this.on = on;
        this._flowing = flowing;
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
        if (this._fromNode.effects.has("rage")) {
            return Colors.GREEN;
        }
        return this.on ? this._fromNode.color : [50, 50, 50];
    }

    get from_node(): Node {
        return this._fromNode;
    }

    set from_node(value: Node) {
        if (this._fromNode !== value) {
            this._fromNode = value;
        }
    }

    // Getter and Setter for toNode
    get to_node(): Node {
        return this._toNode;
    }

    set to_node(value: Node) {
        if (this._toNode !== value) {
            this._toNode = value;
            this.redraw = true;
        }
    }

    get dynamic(): boolean {
        return this._dynamic;
    }

    set dynamic(value: boolean) {
        if (this._dynamic !== value) {
            this._dynamic = value;
            this.redraw = true;
        }
    }

    get flowing(): boolean {
        return this._flowing;
    }

    set flowing(value: boolean) {
        if (this._flowing !== value) {
            this._flowing = value;
            this.redraw = true;
        }
    }

    controlledBy(player: OtherPlayer): boolean {
        return (
            this._fromNode.owner === player ||
            (this.dynamic && this._toNode.owner === player && this._toNode.full)
        );
    }

    other(node: Node): Node {
        if (node === this._fromNode) {
            return this._toNode;
        } else if (node === this._toNode) {
            return this._fromNode;
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
        const startX = this._fromNode.pos.x;
        const startY = this._fromNode.pos.y;
        const endX = this._toNode.pos.x;
        const endY = this._toNode.pos.y;

        const dx = endX - startX;
        const dy = endY - startY;
        const magnitude = Math.sqrt(dx * dx + dy * dy);

        const normX = dx / magnitude;
        const normY = dy / magnitude;

        // Calculate adjusted starting coordinates
        const adjustedStartX = startX + normX * this._fromNode.size;
        const adjustedStartY = startY + normY * this._fromNode.size;

        // Calculate adjusted starting coordinates from the other end
        const adjustedEndX = endX - normX * this._toNode.size;
        const adjustedEndY = endY - normY * this._toNode.size;

        // Adjust the magnitude for both node sizes
        const adjustedMagnitude =
            magnitude - (this._toNode.size + this._fromNode.size);

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

        let color = this._fromNode.effects.has("rage") ? phaserColor(Colors.DARK_GREEN) : this.phaserColor;

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
                adjustedEndX,
                adjustedEndY,
                -normX,
                -normY,
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
        const minSpacing = 12;
    
        const numTriangles = Math.floor(magnitude / minSpacing);
        const spacing = magnitude / numTriangles;
        let angle = Math.atan2(normY, normX) + Math.PI / 2;

        if (this.redraw) {
            this.redraw = false;
            this.spacing = 0;
            // First, clear any inappropriate sprites
            this.sprites.forEach((sprite) => sprite.destroy());
            this.sprites = [];
        }
    
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
        let bias = 0.4;
        for (let i = 0; i < numTriangles; i++) {
            let triangleSprite = this.sprites[i];
            if (spacing != this.spacing) {
                let x = startX + (i - bias) * spacing * normX + triangleSize * normX;
                let y = startY + (i - bias) * spacing * normY + triangleSize * normY;
        
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
        if (this.sprites.length === 0 || this.redraw) {
            this.redraw = false;
            this.spacing = 0;
            // First, clear any inappropriate sprites
            this.sprites.forEach((sprite) => sprite.destroy());
            this.sprites = [];

            // Add the triangle sprite at the end
            let triangleSprite = this.my_scene.add.sprite(0, 0, 'filledTriangle');
            triangleSprite.setTint(Phaser.Display.Color.GetColor(153, 255, 51));
            let angle = Math.atan2(normY, normX);
            triangleSprite.setRotation(angle - Math.PI / 2);
            this.sprites.push(triangleSprite);
    
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
        } else {
            // Adjust sprite array if necessary
            while (this.sprites.length > numCircles) {
                let spriteToRemove = this.sprites.pop();
                spriteToRemove.destroy();
            }
            while (this.sprites.length < numCircles) {
                let circleSprite = this.my_scene.add.sprite(0, 0, this.flowing ? 'filledCircle' : 'outlinedCircle');
                circleSprite.setTint(color);
                this.sprites.push(circleSprite);  // Add to the start
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
        let triangleSprite = this.sprites[0];
        if (spacing != this.spacing) {
            triangleSprite.x = startX + spacing * normX;
            triangleSprite.y = startY + spacing * normY;
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

