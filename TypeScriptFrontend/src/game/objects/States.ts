import { CANNON_ATTACK_RANGE, CAPITAL_ATTACK_RANGE, Colors, CAPITAL_FULL_SIZE, MineVisuals, PUMP_ATTACK_RANGE, ZOMBIE_FULL_SIZE, CANNON_FULL_SIZE, PUMP_FULL_SIZE, } from "./constants";
import { random_equal_distributed_angles } from "./utilities"; // Ensure you import the angles function
import * as Phaser from "phaser";

export class State {
    name: string;
    graphic_override: boolean;
    attack_range: number;
    full_size: number;

    constructor(name: string, full_size: number, attack_range: number = 0, gaphic_override: boolean = false) {
        this.name = name;
        this.attack_range = attack_range;
        this.full_size = full_size;
        this.graphic_override = gaphic_override;
    }

    select(on: boolean) {
        
    }

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        // Draw the state
    }

    removeSprites() {

    }
}

export class ZombieState extends State {
    zombieSprite: Phaser.GameObjects.Image | null = null;

    constructor(name: string) {
        super(name, 0, ZOMBIE_FULL_SIZE, true);
    }

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        if (!this.zombieSprite) {
            this.zombieSprite = scene.add.image(pos.x, pos.y, "blackSquare");
            this.zombieSprite.setOrigin(0.5, 0.5); // Set origin to center for proper scaling
        }
        let currentScale = size / 20; // displayWidth considers current scale
        if (Math.abs(this.zombieSprite.scaleX - currentScale) > 0.01) {
            // threshold to avoid minor changes
            this.zombieSprite.setScale(currentScale);
        }
    }

    removeSprites() {
        this.zombieSprite?.destroy()
    }
}

export class MineState extends State {
    bubble: number;
    ringColor: readonly [number, number, number];
    unfilledColor: readonly [number, number, number];

    constructor(
        name: string,
        bubble: number,
        ringColor: readonly [number, number, number],
        unfilledColor: readonly [number, number, number] = Colors.GREY
    ) {
        super(name, MINE_FULL_SIZE);
        this.bubble = bubble;
        this.ringColor = ringColor;
        this.unfilledColor = unfilledColor;
    }
 }

export class CapitalState extends State {
    capitalized: boolean;
    private starSprite: Phaser.GameObjects.Image | null = null;

    constructor(name: string, capitalized: boolean = false) {
        super(name, CAPITAL_FULL_SIZE, CAPITAL_ATTACK_RANGE);
        this.capitalized = capitalized;
    }

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        if (this.capitalized) {
            if (!this.starSprite) {
                this.starSprite = scene.add.image(pos.x, pos.y, "star");
                this.starSprite.setOrigin(0.5, 0.5); // Set origin to center for proper scaling
            }
            let currentScale = size / 12; // displayWidth considers current scale
            if (Math.abs(this.starSprite.scaleX - currentScale) > 0.01) {
                // threshold to avoid minor changes
                this.starSprite.setScale(currentScale);
            }
        } else if (this.starSprite) {
            this.starSprite.destroy();
            this.starSprite = null;
        }
    }

    removeSprites() {
        this.starSprite?.destroy()
    }
}

export class CannonState extends State {
    angle: number;
    selected: boolean;

    constructor(
        name: string,
        angle: number = random_equal_distributed_angles(1)[0]
    ) {
        super(name, CANNON_FULL_SIZE, CANNON_ATTACK_RANGE);
        this.angle = angle;
        this.selected = false;
    }

    select(on: boolean) {
        this.selected = on;
    }
}

export class PumpState extends State {
    private plusSprite: Phaser.GameObjects.Image | null = null;

    constructor(name: string) {
        super(name, PUMP_FULL_SIZE, PUMP_ATTACK_RANGE);
    }

    draw(scene: Phaser.Scene, size: number, pos: Phaser.Math.Vector2) {
        if (!this.plusSprite) {
            this.plusSprite = scene.add.image(pos.x, pos.y, 'plus');
            this.plusSprite.setOrigin(0.5, 0.5); // Set origin to center for proper scaling
        }
        let currentScale = size / 12; // displayWidth considers current scale
        if (Math.abs(this.plusSprite.scaleX - currentScale) > 0.01) { // threshold to avoid minor changes
            this.plusSprite.setScale(currentScale);
        }
    }

    removeSprites() {
        this.plusSprite?.destroy();
    }

}

export const stateDict: { [key: number]: (full_size: number) => State } = {
    0: (full_size) => new State("default", full_size),
    1: (full_size) => new ZombieState("zombie"),
    2: (full_size) => new CapitalState("capital", true),
    3: (full_size) =>
        new MineState("mine", MineVisuals.RESOURCE_BUBBLE, Colors.DARK_YELLOW),
    4: (full_size) =>
        new MineState(
            "mine",
            MineVisuals.ISLAND_RESOURCE_BUBBLE,
            Colors.YELLOW
        ),
    5: (full_size) => new CannonState("cannon"),
    6: (full_size) => new PumpState("pump"),
};

