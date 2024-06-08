import { AbilityVisual } from "../immutable_visuals"; // Assuming these are defined
import { ClickType } from "../enums"; // Assuming this is defined
import { ValidationFunction } from "../types"; // Assuming this is defined
import { phaserColor } from "../utilities";

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
        const squareSize = 150;  // Size of the square
        const borderThickness = 3;  // Thickness of the border
    
        // Calculate colors
        const colorValue = phaserColor(this.visual.color);
        const darkColor = Phaser.Display.Color.ValueToColor(colorValue).darken(35).color; // Darker shade of the ability color
        const borderColor = isSelected ? 0x990000 : 0x000000; // Dark red if selected, black otherwise
    
        // Draw the background square with darker color
        graphics.fillStyle (darkColor, 1);
        graphics.fillRect(x, y, squareSize, squareSize);

        // Load the ability icon - greyed out
        const imageKey = this.visual.name; // Use a unique key for the image
        let transparency = 0.3;      
        this.addImageToScene(scene, x, y, imageKey, squareSize, transparency, this.percentage);
    
        // Draw the filled part based on the percentage
        graphics.fillStyle(colorValue, 1);
        graphics.fillRect(x, y + (squareSize * (1 - this.percentage)), squareSize, squareSize * this.percentage);
    
        // Draw the border around the square
        graphics.lineStyle(borderThickness, borderColor, 1); // Use conditional border color
        graphics.strokeRect(x, y, squareSize, squareSize);

        // Load the ability icon - brighter 
        transparency = 1;      
        this.addImageToScene(scene, x, y, imageKey, squareSize, transparency, this.percentage);
    
        // Draw the name at the bottom of the square
        const textStyle = {
            font: '24px Arial',
            fill: '#ffffff',
            stroke: '#000000',
            strokeThickness: 3
        };
        const text = scene.add.text(x + squareSize / 2, y + squareSize - 5, this.visual.name, textStyle);
        text.setOrigin(0.5, 1);  // Center the text horizontally and align to the bottom
    
        // Draw the remaining number in the top left corner
        const numberStyle = {
            font: '18px Arial',
            fill: '#ffffff',
            stroke: '#000000',
            strokeThickness: 3
        };
        scene.add.text(x + 5, y + 5, `${this.remaining}`, numberStyle); // Positioned slightly inside the top-left corner
    }
    
    addImageToScene(scene: Phaser.Scene, x: number, y: number, imageKey: string, squareSize: number, transparency: number, percentage: number) {
        const imageSize = 90;
        const image = scene.add.image(x + squareSize / 2, y + (squareSize / 2) - 10, imageKey);
        image.setDisplaySize(imageSize, imageSize);
        image.setOrigin(0.5, 0.5); // Center the image
        image.setAlpha(transparency); // Set transparency to 50%

        if (transparency == 1) {
            // Calculate the offset
            const offset = squareSize / 2 - imageSize / 2 - 10;

            // Set the crop on the image from the top, keeping the bottom portion
            // the 0.1 and 10 have to do with the offset in the image centering
            // no clue where 2.5 comes in
            image.setCrop(0, squareSize - (offset * (percentage - 0.1) * 10) + 2.5, squareSize, squareSize);
        }
    }
    
    
}
