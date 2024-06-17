import { AbilityVisual } from "../immutable_visuals"; // Assuming these are defined
import { ClickType } from "../enums"; // Assuming this is defined
import { ValidationFunction } from "../types"; // Assuming this is defined
import { phaserColor } from "../utilities";
import { IDItem } from "./idItem";

export class ReloadAbility extends IDItem {
    visual: AbilityVisual;
    clickCount: number;
    clickType: ClickType;
    verificationFunc: ValidationFunction;
    credits: number;
    reload: number;
    remaining: number;
    percentage: number;
    graphics: Phaser.GameObjects.Graphics;
    nameText: Phaser.GameObjects.Text;
    numberText: Phaser.GameObjects.Text;
    imageGreyed: Phaser.GameObjects.Image;
    imageVisible: Phaser.GameObjects.Image;
    pointerTriangle: Phaser.GameObjects.Image;
    pointerTriangleText: Phaser.GameObjects.Text;

    constructor(
        visual: AbilityVisual,
        clickCount: number,
        clickType: ClickType,
        verificationFunc: ValidationFunction,
        credits: number,
        reload: number,
        id: number,
        remaining: number = 0,
        percentage: number = 1.0,
        scene: Phaser.Scene
    ) {
        super(id, ClickType.ABILITY);
        this.visual = visual;
        this.clickCount = clickCount;
        this.clickType = clickType;
        this.verificationFunc = verificationFunc;
        this.credits = credits;
        this.reload = reload;
        this.remaining = remaining;
        this.percentage = percentage;
        this.graphics = scene.add.graphics();
    }

    get gameDisplayNum(): number {
        return this.remaining;
    }

    get selectable(): boolean {
        return this.remaining > 0 && this.percentage === 1.0;
    }

    overlapsWithPosition(position: Phaser.Math.Vector2) {
        // Assuming pointerTriangle has x, y, width, and height properties
        if (this.pointerTriangle) {
            const bounds = new Phaser.Geom.Rectangle(
                this.pointerTriangle.x - this.pointerTriangle.originX * this.pointerTriangle.width,
                this.pointerTriangle.y - this.pointerTriangle.originY * this.pointerTriangle.height,
                this.pointerTriangle.width,
                this.pointerTriangle.height
            );

            return bounds.contains(position.x, position.y);
        }
        return false;
    }

    draw(scene, x, y, isSelected, clickable) {
        this.graphics.clear();
        const squareSize = 150;  // Size of the square
        const borderThickness = 3;  // Thickness of the border
    
        // Calculate colors
        const colorValue = phaserColor(this.visual.color);
        const darkColor = Phaser.Display.Color.ValueToColor(colorValue).darken(35).color; // Darker shade of the ability color
        const borderColor = isSelected ? 0x990000 : 0x000000; // Dark red if selected, black otherwise
    
        // Draw the background square with darker color
        this.graphics.fillStyle (darkColor, 1);
        this.graphics.fillRect(x, y, squareSize, squareSize);

        const imageKey = this.visual.name;
        this.addImageToScene(scene, x, y, imageKey, squareSize, this.percentage);

        // Draw the filled part based on the percentage
        this.graphics.fillStyle(colorValue, 1);
        this.graphics.fillRect(x, y + (squareSize * (1 - this.percentage)), squareSize, squareSize * this.percentage);

        // Draw the border around the square
        this.graphics.lineStyle(borderThickness, borderColor, 1); // Use conditional border color
        this.graphics.strokeRect(x, y, squareSize, squareSize);
    
        // Draw the name at the bottom of the square
        if (!this.nameText) {
            this.nameText = scene.add.text(x + squareSize / 2, y + squareSize - 5, this.visual.name, {
                font: '24px Arial',
                fill: '#ffffff',
                stroke: '#000000',
                strokeThickness: 3
            });
            this.nameText.setOrigin(0.5, 1);
        }
    
        if (!this.numberText) {
            this.numberText = scene.add.text(x + 5, y + 5, `${this.remaining}`, {
                font: '18px Arial',
                fill: '#ffffff',
                stroke: '#000000',
                strokeThickness: 3
            });
        }

        if (clickable) {
            if (!this.pointerTriangle) {
                // If clickable is true and the pointerTriangle doesn't exist, create it
                this.pointerTriangle = scene.add.sprite(x - 30, y + squareSize / 2, 'filledTriangle');
                this.pointerTriangle.setTint(Phaser.Display.Color.GetColor(255, 102, 102)); // Light red color
                this.pointerTriangle.setOrigin(0.5, 0.5);
                this.pointerTriangle.setScale(4); // Scale up the triangle to make it bigger
                this.pointerTriangle.angle = 90; // Pointing to the right
        
                // Create the text associated with the pointerTriangle
                let z = 3 - this.credits;  // Calculate the value of z
                this.pointerTriangleText = scene.add.text(x - 45, y + squareSize / 2, `+${z}`, {
                    font: 'bold 24px Arial',
                    fill: '#000000'
                });
                this.pointerTriangleText.setOrigin(1, 0.5); // Align right to the triangle, centered vertically
            }
        } else {
            if (this.pointerTriangle) {
                // If clickable is false and the pointerTriangle exists, destroy both it and the text
                this.pointerTriangle.destroy();
                this.pointerTriangle = null; // Clean up by setting to null
        
                // Destroy the text as well
                this.pointerTriangleText.destroy();
                this.pointerTriangleText = null;
            }
        }
        
    }
    
    addImageToScene(scene, x, y, imageKey, squareSize, percentage) {
        const imageSize = 90;
        // Check and initialize greyed-out image
        if (!this.imageGreyed) {
            this.imageGreyed = scene.add.image(x + squareSize / 2, y + (squareSize / 2) - 10, imageKey);
            this.imageGreyed.setOrigin(0.5, 0.5);
            this.imageGreyed.setDisplaySize(imageSize, imageSize);
            this.imageGreyed.setAlpha(0.3);  // Set low transparency for greyed-out effect
        }
    
        // Check and initialize fully visible image
        if (!this.imageVisible) {
            this.imageVisible = scene.add.image(x + squareSize / 2, y + (squareSize / 2) - 10, imageKey);
            this.imageVisible.setOrigin(0.5, 0.5);
            this.imageVisible.setDisplaySize(imageSize, imageSize);
        }
    
        // Apply cropping to show progression
        const offset = squareSize / 2 - imageSize / 2 - 10;
        this.imageVisible.setCrop(0, squareSize - (offset * (percentage - 0.1) * 10) + 2.5, squareSize, squareSize);
        
    }
    
    
}
