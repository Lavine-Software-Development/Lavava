import { AbilityVisual } from "../immutable_visuals"; // Assuming these are defined
import { ClickType } from "../enums"; // Assuming this is defined
import { ValidationFunction } from "../types"; // Assuming this is defined
import { ABILITY_SIZE, ABILITY_FONT, FONT_GAP } from "../constants"; // Assuming these are defined

export class ReloadAbility {
    visual: AbilityVisual;
    clickCount: number;
    clickType: ClickType;
    verificationFunc: ValidationFunction;
    credits: number;
    reload: number;
    remaining: number;
    percentage: number;

    constructor(
        visual: AbilityVisual,
        clickCount: number,
        clickType: ClickType,
        verificationFunc: ValidationFunction,
        credits: number,
        reload: number,
        remaining: number = 0,
        percentage: number = 1.0
    ) {
        this.visual = visual;
        this.clickCount = clickCount;
        this.clickType = clickType;
        this.verificationFunc = verificationFunc;
        this.credits = credits;
        this.reload = reload;
        this.remaining = remaining;
        this.percentage = percentage;
    }

    get gameDisplayNum(): number {
        return this.remaining;
    }

    get selectable(): boolean {
        return this.remaining > 0 && this.percentage === 1.0;
    }

    draw(scene, x, y, isSelected) {
        const graphics = scene.add.graphics();
        const btn_size = ABILITY_SIZE * scene.height;  // Ensure you have defined `ABILITY_SIZE` appropriately.
        const border_thickness = 5;

        // Color calculations
        const darker_color = Phaser.Display.Color.ValueToColor(this.visual.color).darken(10).color;
        const lighter_color = Phaser.Display.Color.ValueToColor(this.visual.color).brighten(10).color;

        if (isSelected) {
            graphics.fillStyle(lighter_color, 1);
            graphics.fillRect(x - border_thickness, y - border_thickness, btn_size + 2 * border_thickness, btn_size + 2 * border_thickness);
        }

        // Draw the button background
        graphics.fillStyle(darker_color, 1);
        graphics.fillRect(x, y, btn_size, btn_size);

        // Drawing text
        let style = { font: `${int(scene.height * ABILITY_FONT)}px Arial`, fill: '#ffffff' };
        scene.add.text(x + (btn_size / 2), y + (btn_size / 2), this.visual.letter, style).setOrigin(0.5, 0.5);

        scene.add.text(x + (btn_size / 2), y + btn_size - (FONT_GAP * scene.height), this.visual.name, style).setOrigin(0.5, 1);
        scene.add.text(x + 10, y + 10, `${this.credits}`, style);
    }
}
