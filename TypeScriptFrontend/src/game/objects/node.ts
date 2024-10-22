import { State } from "./States";
import { Colors, PORT_COUNT } from "./constants";
import { OtherPlayer } from "./otherPlayer";
import { IDItem } from "./idItem";
import { ClickType } from "./enums";
import { phaserColor, cannonAngle } from "./utilities";
import { CannonState } from "./States";
import { INode, IEdge } from "./graphTypeInterfaces";
import { random_equal_distributed_angles } from "./utilities";


export class Node extends IDItem implements INode {
    pos: Phaser.Math.Vector2;
    percents: [number, number];
    private _state: State;
    private _value: number;
    delayChange = false;
    delayedValue = 0;
    delayedOwner: OtherPlayer | null = null;
    private _effects: Set<string>;
    private _owner: OtherPlayer | null;
    private _scene: Phaser.Scene;
    graphics: Phaser.GameObjects.Graphics;
    private cannonGraphics: Phaser.GameObjects.Graphics;
    edges: IEdge[];

    constructor(
        id: number,
        pos: [number, number],
        state: State,
        value: number,
        _scene: Phaser.Scene
    ) {
        super(id, ClickType.NODE);
        this.percents = [pos[0] / 1000, pos[1] / 700];
        this.pos = new Phaser.Math.Vector2(pos[0], pos[1]);

        this.state = state;
        this.value = value;
        this.edges = [];
        this.effects = new Set();
        this.owner = null;
        this.scene = _scene;
        this.graphics = _scene.add.graphics();
        this.cannonGraphics = _scene.add.graphics();
    }

    get value(): number {
        return this._value;
    }

    hasRelevantEdges(player: OtherPlayer): boolean {
        // Check incoming edges
        const relevantIncomingEdges = this.edges.some(edge => 
            edge.to_node === this && 
            edge.from_node.owner === player && 
            !edge.on
        );

        if (relevantIncomingEdges) {
            return true;
        }
        else if (this.owner !== player) {
            return false;
        }

        // Check outgoing edges
        const relevantOutgoingEdges = this.edges.some(edge => 
            edge.from_node === this && 
            edge.to_node.owner === player && 
            edge.dynamic
        );

        return relevantOutgoingEdges;
    }

    hasRelevantOffEdges(player: OtherPlayer): boolean {
        // Check incoming edges
        const relevantIncomingEdges = this.edges.some(edge => 
            edge.to_node === this && 
            edge.from_node.owner === player && 
            edge.on
        );

        return relevantIncomingEdges;
    }

    set value(value: number) {
        if (!this.delayChange) {
            this._value = value;
        } else {
            this.delayedValue = value;
        }
    }

    set state(state: State) {
        if (this._state) {
            this._state.removeSprites();
            
            this.destroyCannon();
        }
        this._state = state;
    }

    get state() {
        return this._state;
    }

    public delete(): void {
        // Remove graphics from the scene
        if (this.graphics) {
            this.graphics.clear();
            this.graphics.destroy();
        }

        this.destroyCannon();
    }

    destroyCannon() {
        if (this.cannonGraphics) {
            this.cannonGraphics.clear();
        }
    }

    select(on: boolean): void {
        this.state.select(on);
    }

    get owner(): OtherPlayer | null {
        return this._owner;
    }

    set owner(owner: OtherPlayer | null) {
        if (!this.delayChange) {
            this._owner = owner;
            this.influencedEdges.forEach((edge) => (edge.recolor = true));
        } else {
            this.delayedOwner = owner;
        }
    }

    endDelay(): void {
        this.delayChange = false;
        if (this.delayedOwner) {
            this.owner = this.delayedOwner;
            this.delayedOwner = null;
        }
        if (this.delayedValue) {
            this.value = this.delayedValue;
            this.delayedValue = 0;
        }
    }

    get effects(): Set<string> {
        return this._effects;
    }

    set effects(effects: Set<string>) {
        this._effects = effects;
        this.outwardEdges.forEach((edge) => (edge.recolor = true));
    }

    get phaserColor(): number {
        return phaserColor(this.color);
    }
;
    get color(): readonly [number, number, number] {
        throw new Error("Method not implemented.");
    }

    get accessible(): boolean {
        throw new Error("Method not implemented.");
    }

    get accepts_shot(): boolean {
        throw new Error("Method not implemented.");
    }

    get influencedEdges(): IEdge[] {
        return this.outwardEdges.filter((edge) => edge.on);
    }

    get outwardEdges(): IEdge[] {
        return this.edges.filter((edge) => edge.from_node === this);
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
        return this.value >= this.state.full_size && !this.effects.has("over_grow");
    }

    set scene(scene: Phaser.Scene) {
        this._scene = scene;
        this.resize();
        this.graphics = this._scene.add.graphics();
        this.cannonGraphics = this._scene.add.graphics();
    }

    drawSurrounding(): void {
        // pass
    }

    draw(): void {
        this.graphics.clear();
        if (this.state.graphic_override) {
            this.state.draw(this._scene, this.size, this.pos, this.owner?.color);
            return;
        } else {
            if (this.effects.has("poison")) {
                this.graphics.lineStyle(5, phaserColor(Colors.PURPLE), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size + 4
                );
            }

            if (this.owner) {
                this.drawSurrounding()
            }

            this.graphics.fillStyle(this.phaserColor, 1);
            this.graphics.fillCircle(this.pos.x, this.pos.y, this.size);

            if (this.effects.has("rage")) {
                const eff_color = this.owner?.color == Colors.RED ? Colors.DARK_RED : Colors.RED;
                this.graphics.lineStyle(3, phaserColor(eff_color), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size - 5
                );
            }
            if (this.effects.has("over_grow")) {
                const eff_color = this.owner?.color == Colors.GREEN ? Colors.DARK_GREEN : Colors.MEDIUM_GREEN;
                this.graphics.lineStyle(3, phaserColor(eff_color), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size 
                );
            }
            if (this.full) {
                this.graphics.lineStyle(2, phaserColor(Colors.BLACK), 1);
                this.graphics.strokeCircle(
                    this.pos.x,
                    this.pos.y,
                    this.size + 1
                );
                if (this.stateName === "capital") {
                    this.graphics.lineStyle(2, phaserColor(Colors.PINK), 1);
                    this.graphics.strokeCircle(
                        this.pos.x,
                        this.pos.y,
                        this.size + 3
                    );
                }
            }

            this.state.draw(this._scene, this.size, this.pos, this.owner?.color);

            if (this.state instanceof CannonState) {
                this.cannonGraphics.clear();
                if (this.state.selected) {
                    let mousePos = this._scene.input.activePointer.position;
                    // Calculate angle between the spot and the mouse cursor
                    cannonAngle(this, mousePos.x, mousePos.y);
                    let dx = mousePos.x - this.pos.x;
                    let dy = mousePos.y - this.pos.y;
            
                    // Calculate distance to mouse cursor
                    let distanceToMouse = Math.sqrt(dx * dx + dy * dy) - this.size * 1.2;
            
                    // Draw the yellow rectangle from the cannon to the mouse cursor
                    this.drawRotatedRectangle(
                        this.state.angle,
                        distanceToMouse,  // Width is the distance to the mouse
                        this.size,        // Height remains the same as the cannon
                        Colors.LIGHT_YELLOW,  // Light yellow color
                        this.cannonGraphics,
                        0.8,  // Optional: a lesser alpha for lighter visibility
                        distanceToMouse / 2
                    );
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
    }

    drawRotatedRectangle(
        angle: number,
        portWidth: number,
        portHeight: number,
        col: readonly [number, number, number],
        graphics: Phaser.GameObjects.Graphics = this.graphics,
        alpha: number = 1,  // Default opacity is 100%
        xOffset: number = 0  // Default to no offset
    ): void {
        const rad = Phaser.Math.DegToRad(angle);
        const halfWidth = portWidth / 2;
        const halfHeight = portHeight / 2;
        const distanceFromCenter = this.size * 1.2;
    
        const portCenter = new Phaser.Math.Vector2(
            this.pos.x + Math.cos(rad) * (distanceFromCenter + xOffset),
            this.pos.y + Math.sin(rad) * (distanceFromCenter + xOffset)
        );
    
        // Calculate the corners of the rotated rectangle
        const corners = [
            new Phaser.Math.Vector2(-halfWidth, -halfHeight),
            new Phaser.Math.Vector2(halfWidth, -halfHeight),
            new Phaser.Math.Vector2(halfWidth, halfHeight),
            new Phaser.Math.Vector2(-halfWidth, halfHeight),
        ].map(corner => corner.rotate(rad).add(portCenter));
    
        // Change graphics fill style here if needed
        graphics.fillStyle(
            Phaser.Display.Color.GetColor(col[0], col[1], col[2]),
            alpha
        );
    
        // Draw the polygon
        graphics.beginPath();
        graphics.moveTo(corners[0].x, corners[0].y);
        corners.forEach((corner, index) => {
            if (index > 0) graphics.lineTo(corner.x, corner.y);
        });
        graphics.closePath();
        graphics.fillPath();
    }

    resize(): void {
        // Adjust the position of the node based on newWidth and newHeight
        this.pos.x = this.percents[0] * Number(this._scene.game.config.width);
        this.pos.y = this.percents[1] * Number(this._scene.game.config.height);
        // Optionally, adjust the size or other properties here as needed
    }

}


export class PortNode extends Node {
    is_port: boolean;
    portPercent: number;
    ports: Array<number>;

    constructor(
        id: number,
        pos: [number, number],
        is_port: boolean,
        state: State,
        value: number,
        _scene: Phaser.Scene
    ) {
        super(id, pos, state, value, _scene);
        this.is_port = is_port;
        this.portPercent = 1;
        this.ports = is_port ? random_equal_distributed_angles(PORT_COUNT) : [];
    }

    get color(): readonly [number, number, number] {
        if (!this.owner) {
            return this.is_port ? Colors.BROWN : Colors.BLACK;
        }
        return this.owner.color;
    }

    get accessible(): boolean {
        return this.is_port;
    }

    get accepts_shot(): boolean {
        return true;
    }

    drawSurrounding(): void {
        if (this.is_port) {
            this.drawPorts(Colors.BROWN);
        } else if (this.ports.length > 0) {
            this.drawPorts(Colors.ORANGE);
            if (this.portPercent > 0) {
                this.portPercent -= 0.02;
            }
            else {
                this.ports = [];
            }
        }
    }

    drawPorts(color: readonly [number, number, number]): void {
        const portWidth = this.size;
        const portHeight = this.size * 1.3;
        this.ports.forEach((angle) => {
            this.drawRotatedRectangle(angle, portWidth * this.portPercent, portHeight * this.portPercent, color);
        });
    }
}

const wall_count_color = {0: Colors.BROWN, 1: Colors.GREY, 2: Colors.BLACK}

export class WallNode extends Node {
    private readonly waveCount: number = 8;
    private readonly waveAmplitude: number = 0.1;
    private readonly innerWallColor: number = phaserColor(Colors.LIGHT_GREY);
    private readonly outerWallColor: number = phaserColor(Colors.DARK_GRAY);
    private _wall_count: number;
    private wallPercent: number;

    constructor(
        id: number,
        pos: [number, number],
        wall_count: number,
        state: State,
        value: number,
        _scene: Phaser.Scene 
    ) {
        super(id, pos, state, value, _scene);
        this._wall_count = wall_count;
        this.wallPercent = 0;
    }

    set wall_count(wall_count: number) {
        if (this._wall_count && wall_count < this._wall_count) {
            this.wallPercent = 1;
        }
        this._wall_count = wall_count;
    }

    get wall_count(): number {
        return this._wall_count;
    }

    get color(): readonly [number, number, number] {
        if (!this.owner) {
            return wall_count_color[this.wall_count];
        }
        return this.owner.color;
    }

    drawSurrounding(): void {
        if (this.wall_count > 0 || this.wallPercent > 0) {
            this.drawWalls();
        }

        if (this.wallPercent > 0) {
            this.wallPercent -= 0.02;
        }
    }

    get accessible(): boolean {
        return this.wall_count === 0;
    }

    get accepts_shot(): boolean {
        // return this.wall_count === 0;
        return true;
    }

    // private drawWalls(): void {
    //     const graphics = this.graphics;
    //     const centerX = this.pos.x;
    //     const centerY = this.pos.y;

    //     if (this.wall_count === 0) {
    //         // Draw a partial inner wall if wall_count is 0 but wallPercent > 0
    //         if (this.wallPercent > 0) {
    //             this.drawWavyWall(centerX, centerY, this.size * 1.1, this.size * 1.3, this.innerWallColor, this.wallPercent);
    //         }
    //     } else {
    //         // Draw inner wall if wall_count is at least 1
    //         this.drawWavyWall(centerX, centerY, this.size * 1.1, this.size * 1.3, this.innerWallColor);

    //         // Draw outer wall if wall_count is 2 or if there's a partial wall
    //         if (this.wall_count === 2 || (this.wall_count === 1 && this.wallPercent > 0)) {
    //             const outerWallPercent = this.wall_count === 2 ? 1 : this.wallPercent;
    //             this.drawWavyWall(centerX, centerY, this.size * 1.3, this.size * 1.5, this.outerWallColor, outerWallPercent);
    //         }
    //     }
    // }

    private drawWalls(): void {
        const graphics = this.graphics;
        const centerX = this.pos.x;
        const centerY = this.pos.y;
    
        if (this.wall_count === 0) {
            // Draw a partial inner wall if wall_count is 0 but wallPercent > 0
            if (this.wallPercent > 0) {
                this.drawWavyWall(centerX, centerY, this.size * 1.1, this.size * 1.3, this.innerWallColor, this.wallPercent);
            }
        } else if (this.wall_count === 1) {
            // Draw inner wall if wall_count is 1
            this.drawWavyWall(centerX, centerY, this.size * 1.1, this.size * 1.3, this.innerWallColor);
    
            // Draw partial outer wall if there's a partial wall
            if (this.wallPercent > 0) {
                this.drawWavyWall(centerX, centerY, this.size * 1.3, this.size * 1.5, this.outerWallColor, this.wallPercent);
            }
        } else if (this.wall_count === 2) {
            // Draw a single dark wall for wall_count 2
            this.drawWavyWall(centerX, centerY, this.size * 1.1, this.size * 1.5, this.outerWallColor);
        }
    }

    private drawWavyWall(centerX: number, centerY: number, innerRadius: number, outerRadius: number, color: number, percent: number = 1): void {
        const graphics = this.graphics;
        const endAngle = 360 * percent;

        graphics.fillStyle(color, 1);
        graphics.beginPath();

        // Draw outer wavy circle
        for (let i = 0; i <= endAngle; i++) {
            const angle = Phaser.Math.DegToRad(i);
            const waveOffset = Math.sin(angle * this.waveCount) * this.waveAmplitude;
            const x = centerX + (outerRadius + waveOffset * outerRadius) * Math.cos(angle);
            const y = centerY + (outerRadius + waveOffset * outerRadius) * Math.sin(angle);

            if (i === 0) {
                graphics.moveTo(x, y);
            } else {
                graphics.lineTo(x, y);
            }
        }

        // Draw inner circle (counterclockwise)
        for (let i = endAngle; i >= 0; i--) {
            const angle = Phaser.Math.DegToRad(i);
            const x = centerX + innerRadius * Math.cos(angle);
            const y = centerY + innerRadius * Math.sin(angle);
            graphics.lineTo(x, y);
        }

        graphics.closePath();
        graphics.fillPath();

        // Add a stroke to the outer edge for definition
        graphics.strokePath();
    }

    draw(): void {
        this.drawWalls(); // Draw the walls first
        super.draw(); // Then draw the node on top
    }

}