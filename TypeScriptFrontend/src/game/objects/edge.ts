import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "./enums";
import { Node } from "./node";
import { Colors } from "./constants";
import { phaserColor } from "./utilities";
import { IEdge } from "./graphTypeInterfaces";

export class Edge extends IDItem implements IEdge {
    private _fromNode: Node;
    to_node: Node;
    private _dynamic: boolean;
    private _on: boolean;
    private _flowing: boolean;
    line: Phaser.Geom.Line;
    hover_line: Phaser.Geom.Line;
    graphics: Phaser.GameObjects.Graphics;
    my_scene: Phaser.Scene;
    sprites: Phaser.GameObjects.Sprite[];
    last_spacing: number;
    redraw: boolean;
    recolor: boolean;

    constructor(
        id: number,
        fromNode: Node,
        toNode: Node,
        dynamic: boolean,
        _scene?: Phaser.Scene
    ) {
        super(id, ClickType.EDGE); // Example ID logic
        this._fromNode = fromNode;
        this.to_node = toNode;
        this._dynamic = dynamic;
        this._on = false;
        this._flowing = false;
        if (_scene) {
            this.my_scene = _scene;
            this.graphics = _scene.add.graphics();
        }
        this.hover_line = new Phaser.Geom.Line(
            this._fromNode.pos.x,
            this._fromNode.pos.y,
            this.to_node.pos.x,
            this.to_node.pos.y
        );
        this.line = new Phaser.Geom.Line(
            this._fromNode.pos.x,
            this._fromNode.pos.y,
            this.to_node.pos.x,
            this.to_node.pos.y
        );

        this.sprites = [];
        this.last_spacing = 0;
        this.to_node.edges.push(this);
        this._fromNode.edges.push(this);
        this.redraw = true;
    }

    relocate_lines(): void {

    }

    delete(): void {
        // Clear all sprites
        this.clearSprites();
    
        // Remove the graphics object if it exists
        if (this.graphics) {
            this.graphics.clear();
            this.graphics.destroy();
        }
    }

    get color(): readonly [number, number, number] {
        if (this._fromNode.effects.has("rage")) {
            return Colors.DARK_GREEN;
        }
        return this.on ? this._fromNode.color : [50, 50, 50];
    }

    get on(): boolean {
        return this._on;
    }

    set on(value: boolean) {
        if (this._on !== value) {
            this._on = value;
            this.recolor = true;
        }
    }

    get from_node(): Node {
        return this._fromNode;
    }

    set from_node(value: Node) {
        if (this._fromNode !== value) {
            this._fromNode = value;
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
            (this.dynamic && this.to_node.owner === player && this.to_node.full)
        );
    }

    other(node: Node): Node {
        if (node === this._fromNode) {
            return this.to_node;
        } else if (node === this.to_node) {
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

    colorSprites(): void {
        if (this.recolor) {
            this.sprites.forEach((sprite) => {
                sprite.setTint(this.phaserColor);
            });
            if (this.dynamic) {
                this.sprites[0].setTint(Phaser.Display.Color.GetColor(153, 255, 51));
            }
            this.recolor = false;
        }
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
        const endX = this.to_node.pos.x;
        const endY = this.to_node.pos.y;

        const dx = endX - startX;
        const dy = endY - startY;
        const magnitude = Math.sqrt(dx * dx + dy * dy);

        const normX = dx / magnitude;
        const normY = dy / magnitude;

        // Calculate adjusted starting coordinates
        const adjustedStartX = startX + normX * this._fromNode.size;
        const adjustedStartY = startY + normY * this._fromNode.size;

        // Calculate adjusted starting coordinates from the other end
        const adjustedEndX = endX - normX * this.to_node.size;
        const adjustedEndY = endY - normY * this.to_node.size;

        // Adjust the magnitude for both node sizes
        const adjustedMagnitude =
            magnitude - (this.to_node.size + this._fromNode.size);

        // update this.hover_line to start at the adjusted values and be magnitude long
        this.calculateHoverLine(adjustedStartX, normX, adjustedMagnitude, adjustedStartY, normY);

        if (this.redraw) {
            this.clearSprites();
            this.redraw = false;
        }

        if (!this.dynamic) {
            this.drawArrow(adjustedStartX, adjustedStartY, normX, normY, adjustedMagnitude);
        } else {
            this.drawCircle(adjustedEndX, adjustedEndY, -normX, -normY, adjustedMagnitude);
        }

        this.colorSprites();
    }

    private calculateHoverLine(adjustedStartX: number, normX: number, adjustedMagnitude: number, adjustedStartY: number, normY: number) {
        const shorterStartX = adjustedStartX + normX * adjustedMagnitude * 0.15; // Move start point inwards
        const shorterStartY = adjustedStartY + normY * adjustedMagnitude * 0.15;
        const shorterEndX = adjustedStartX + normX * adjustedMagnitude * 0.85; // Move end point inwards
        const shorterEndY = adjustedStartY + normY * adjustedMagnitude * 0.85;

        this.hover_line.setTo(shorterStartX, shorterStartY, shorterEndX, shorterEndY
        );
    }

    drawArrow(
        startX: number,
        startY: number,
        normX: number,
        normY: number,
        magnitude: number,
    ): void {
        const triangleSize = 11;
        const minSpacing = 12;
    
        const numTriangles = Math.floor(magnitude / minSpacing);
        const spacing = magnitude / numTriangles;
        let angle = Math.atan2(normY, normX) + Math.PI / 2;

        let constant_sprites = this.sprites.length == numTriangles;

        while (this.sprites.length < numTriangles) {
            let triangleSprite = this.my_scene.add.sprite(
                0,
                0,
                this.flowing ? "filledTriangle" : "outlinedTriangle"
            );
            triangleSprite.setRotation(angle);
            triangleSprite.setTint(this.phaserColor);
            this.sprites.push(triangleSprite);
        }
        while (this.sprites.length > numTriangles) {
            let sprite = this.sprites.pop();
            if (sprite) {
                sprite.destroy();
            }
        }

        if ((!constant_sprites) || (Math.abs(spacing - this.last_spacing) > 0.2)) {

        // Update positions of existing sprites
            let bias = 0.4;
            for (let i = 0; i < numTriangles; i++) {
                let triangleSprite = this.sprites[i];
                triangleSprite.x = startX + (i - bias) * spacing * normX + triangleSize * normX;
                triangleSprite.y = startY + (i - bias) * spacing * normY + triangleSize * normY;
            }

            this.last_spacing = spacing
        }
    }


    drawCircle(
        startX: number,
        startY: number,
        normX: number,
        normY: number,
        magnitude: number,
    ): void {
        const circleRadius = 3;
        const minSpacing = 8;

        const numCircles = Math.floor(
            (magnitude - 2 * circleRadius) / minSpacing
        );
        const spacing = (magnitude - 2 * circleRadius) / numCircles;

        // Initialize the triangle sprite if not already present or if there are no sprites at all
        if (this.sprites.length === 0) {
            // Add the triangle sprite at the end
            let triangleSprite = this.my_scene.add.sprite(0, 0, 'filledTriangle');
            triangleSprite.setTint(Phaser.Display.Color.GetColor(153, 255, 51));
            let angle = Math.atan2(normY, normX);
            triangleSprite.setRotation(angle - Math.PI / 2);
            this.sprites.push(triangleSprite);
        }

        let constant_sprites = this.sprites.length == numCircles;
        while (this.sprites.length > numCircles) {
            let spriteToRemove = this.sprites.pop();
            if (spriteToRemove) {
                spriteToRemove.destroy();
            }
        }
        while (this.sprites.length < numCircles) {
            let circleSprite = this.my_scene.add.sprite(0, 0, this.flowing ? 'filledCircle' : 'outlinedCircle');
            circleSprite.setTint(this.phaserColor);
            this.sprites.push(circleSprite);  // Add to the start
        }

        // Update positions of existing circle sprites
        if ((!constant_sprites) || (Math.abs(spacing - this.last_spacing) > 0.2)) {
            for (let i = 1; i < numCircles; i++) {
                let circleSprite = this.sprites[i];
                circleSprite.x = startX + (i + 1) * spacing * normX;
                circleSprite.y = startY + (i + 1) * spacing * normY;
            }
            let triangleSprite = this.sprites[0];
            triangleSprite.x = startX + spacing * normX;
            triangleSprite.y = startY + spacing * normY;
            this.last_spacing = spacing;
        }

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

