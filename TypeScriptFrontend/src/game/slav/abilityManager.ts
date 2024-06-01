import { ReloadAbility } from "./Objects/ReloadAbility";
import { IDItem } from "./Objects/idItem";
import { Highlight } from "./highlight";
import { Event } from "./Objects/event";
import { Node } from "./Objects/node";
import { phaserColor } from "./utilities";
import { Colors } from "./constants";

export class AbstractAbilityManager {
    private abilities: { [key: number]: ReloadAbility };
    private events: { [key: number]: Event };
    private mode: number | null = null;
    private backupMode: number | null = null;
    private clicks: IDItem[] = [];
    abilityText: any;
    BridgeGraphics: Phaser.GameObjects.Graphics;

    constructor(
        scene: Phaser.Scene,
        abilities: { [key: number]: ReloadAbility },
        events: { [key: number]: Event }
    ) {
        this.abilities = abilities;
        this.events = events;
        this.BridgeGraphics = scene.add.graphics();
    }

    inAbilities(key: number): boolean {
        return key in this.abilities;
    }

    useEvent(highlight: Highlight): number[] | false {
        if (this.mode && this.mode !== highlight.usage) {
            this.backupReset();
        }
        this.mode = highlight.usage;
        this.clicks.push(highlight.item!); // Assuming item is always present
        if (this.completeCheck(highlight.usage)) {
            const clicks = this.clicks.map((click) => click.id);
            this.backupReset();
            return clicks;
        }
        return false;
    }

    useAbility(highlight: Highlight): boolean {
        if (
            this.ability &&
            highlight.usage === this.mode &&
            highlight.type === this.ability.clickType &&
            highlight.item
        ) {
            this.clicks.push(highlight.item);
            return true;
        }
        return false;
    }

    completeAbility(): number[] | false {
        if (this.completeCheck()) {
            const clicks = this.clicks.map((click) => click.id);
            this.reset();
            return clicks;
        }
        return false;
    }

    backupReset(): void {
        if (this.backupMode) {
            this.mode = this.backupMode;
            this.backupMode = null;
            this.wipe();
        } else {
            if (this.ability) {
                this.backupMode = this.mode;
            }
            this.reset();
        }
    }

    reset(): void {
        this.wipe();
        this.mode = null;
    }

    wipe(): void {
        this.clicks = [];
        this.BridgeGraphics.clear();
    }

    switchTo(key: number): boolean {
        this.mode = key;
        if (this.completeCheck()) {
            this.reset();
            return true;
        }
        return false;
    }

    completeCheck(event?: number | null): boolean {
        if (this.ability) {
            return this.ability.clickCount === this.clicks.length;
        } else if (event) {
            return this.events[event].clickCount === this.clicks.length;
        }
        console.error("ERROR, No ability or event");
        return false;
    }

    select(key: number): boolean {
        if (this.mode) {
            this.wipe();
        }
        if (this.mode === key) {
            this.mode = null;
        } else if (this.abilities[key].selectable) {
            return this.switchTo(key);
        }
        return false;
    }

    validate(item: IDItem): [IDItem, number] | false {
        if (
            this.event &&
            item.type === this.event.clickType &&
            this.event.verificationFunc(this.clicks.concat([item]))
        ) {
            return [item, this.mode!]; // Assuming mode is set
        } else if (
            this.ability &&
            item.type === this.ability.clickType &&
            this.ability.verificationFunc(this.clicks.concat([item]))
        ) {
            return [item, this.mode!]; // Assuming mode is set
        } else {
            for (const code in this.events) {
                const ev = this.events[code];
                if (item.type === ev.clickType && ev.verificationFunc([item])) {
                    return [item, parseInt(code)];
                }
            }
        }
        return false;
    }

    get ability(): ReloadAbility | null {
        if (this.mode !== null && this.abilities[this.mode]) {
            return this.abilities[this.mode];
        }
        return null;
    }

    get event(): Event | null {
        if (this.mode !== null && this.events[this.mode]) {
            return this.events[this.mode];
        }
        return null;
    }

    draw(scene: Phaser.Scene): void {
        if (this.ability) {
            // Assuming `this.ability.visual.name` contains the text you want to display
            const name = this.ability.visual.name;

            // Determine the position for the text. Adjust 'x' and 'y' to position it at the bottom right
            const x = scene.sys.canvas.width - 10; // 10 pixels from the right edge
            const y = scene.sys.canvas.height - 30; // 30 pixels from the bottom

            // Create or update the text object
            if (!this.abilityText) {
                // If the text object doesn't exist, create it
                this.abilityText = scene.add.text(x, y, name, {
                    fontSize: "24px",
                    align: "right",
                });

                // Set origin to (1, 1) to align text to the bottom right
                this.abilityText.setOrigin(1, 1);
            } else {
                // If it already exists, just update the content and position (if needed)
                this.abilityText.setText(name);
                this.abilityText.setPosition(x, y);
            }
            if (
                this.ability.visual.name == "Bridge" &&
                this.clicks.length > 0
            ) {
                this.BridgeGraphics.clear();
                const fromNode = this.clicks[0] as Node;
                let mousePos = scene.input.activePointer.position;
                const startX = fromNode.pos.x;
                const startY = fromNode.pos.y;
                const endX = mousePos.x;
                const endY = mousePos.y;

                const dx = endX - startX;
                const dy = endY - startY;
                const magnitude = Math.sqrt(dx * dx + dy * dy);

                const normX = dx / magnitude;
                const normY = dy / magnitude;

                const color = phaserColor(Colors.YELLOW);
                this.drawArrow(startX, startY, normX, normY, magnitude, color);
            }
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
        const minSpacing = 11;

        const numTriangles = Math.floor(
            (magnitude - 2 * triangleSize) / minSpacing
        );
        const spacing = (magnitude - 2 * triangleSize) / numTriangles;

        for (let i = 1; i <= numTriangles; i++) {
            let x = startX + i * spacing * normX + triangleSize * normX;
            let y = startY + i * spacing * normY + triangleSize * normY;
            let angle = Math.atan2(normY, normX);

            this.BridgeGraphics.beginPath();
            this.BridgeGraphics.moveTo(x, y);
            this.BridgeGraphics.lineTo(
                x - Math.cos(angle - Math.PI / 6) * triangleSize,
                y - Math.sin(angle - Math.PI / 6) * triangleSize
            );
            this.BridgeGraphics.lineTo(
                x - Math.cos(angle + Math.PI / 6) * triangleSize,
                y - Math.sin(angle + Math.PI / 6) * triangleSize
            );
            this.BridgeGraphics.closePath();

            this.BridgeGraphics.fillStyle(color);
            this.BridgeGraphics.fillPath();
        }
    }
}

