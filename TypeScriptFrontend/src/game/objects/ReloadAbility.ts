import { AbilityVisual } from "./immutable_visuals"; // Assuming these are defined
import { ClickType } from "./enums"; // Assuming this is defined
import { ValidationFunction } from "./types"; // Assuming this is defined
import { phaserColor } from "./utilities";
import { IDItem } from "./idItem";

export class ReloadAbility extends IDItem {
    visual: AbilityVisual;
    clickCount: number;
    clickType: ClickType;
    verificationFunc: ValidationFunction;
    credits: number;
    reload: number;
    private _remaining: number;
    percentage: number;
    graphics: Phaser.GameObjects.Graphics;
    nameText: Phaser.GameObjects.Text;
    letterText: Phaser.GameObjects.Text;
    numberText: Phaser.GameObjects.Text;
    imageGreyed: Phaser.GameObjects.Image;
    imageVisible: Phaser.GameObjects.Image;
    pointerTriangle: Phaser.GameObjects.Image;
    pointerTriangleText: Phaser.GameObjects.Text;
    x: number;
    y: number;
    redraw: boolean;

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
        this._remaining = remaining;
        this.percentage = percentage;
        this.graphics = scene.add.graphics();
        this.x = 0;
        this.y = 0;
        this.redraw = false;
    }

    get gameDisplayNum(): number {
        return this.remaining;
    }

    get selectable(): boolean {
        return this.remaining > 0 && this.percentage === 1.0;
    }

    get remaining(): number {
        return this._remaining;
    }

    set remaining(value: number) {
        this._remaining = value;
        this.redraw = true;
    }

    delete(): void {
        // Destroy graphics
        if (this.graphics) {
            this.graphics.clear();
            this.graphics.destroy();
        }
    
        // Destroy text objects
        if (this.nameText) this.nameText.destroy();
        if (this.letterText) this.letterText.destroy();
        if (this.numberText) this.numberText.destroy();
        if (this.pointerTriangleText) this.pointerTriangleText.destroy();
    
        // Destroy image objects
        if (this.imageGreyed) this.imageGreyed.destroy();
        if (this.imageVisible) this.imageVisible.destroy();
        if (this.pointerTriangle) this.pointerTriangle.destroy();

        // Reset other properties
        this.x = 0;
        this.y = 0;
        this.redraw = false;
    }

    overlapsWithPosition(position: Phaser.Math.Vector2): boolean {
        // Assuming pointerTriangle has x, y, width, and height properties
        if (this.pointerTriangle) {
            const bounds = new Phaser.Geom.Rectangle(
                this.pointerTriangle.x - this.pointerTriangle.originX * this.pointerTriangle.width,
                this.pointerTriangle.y - this.pointerTriangle.originY * this.pointerTriangle.height,
                this.pointerTriangle.width,
                this.pointerTriangle.height
            );

            return bounds.contains(position.x, position.y);
        } else {
            const bounds = new Phaser.Geom.Rectangle(
                this.x, this.y, 150, 150
            );

            return bounds.contains(position.x, position.y);
        }
    }

    setPos(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    draw(scene, isSelected, clickable) {
        this.graphics.clear();
        const squareSize = 150;  // Size of the square
          // Thickness of the border
    
        // Calculate colors
        const colorValue = phaserColor(this.visual.color);
        const darkColor =
            Phaser.Display.Color.ValueToColor(colorValue).darken(35).color; // Darker shade of the ability color
        const borderColor = isSelected ? 0x990000 : 0x000000; // Dark red if selected, black otherwise
        const borderThickness = isSelected ? 7 : 3;
    
        // Draw the background square with darker color
        this.graphics.fillStyle (darkColor, 1);
        this.graphics.fillRect(this.x, this.y, squareSize, squareSize);

        const imageKey = this.visual.name;
        this.addImageToScene(scene, this.x, this.y, imageKey, squareSize, this.percentage);

        // Draw the filled part based on the percentage
        this.graphics.fillStyle(colorValue, 1);
        this.graphics.fillRect(this.x, this.y + (squareSize * (1 - this.percentage)), squareSize, squareSize * this.percentage);

        // Draw the border around the square
        this.graphics.lineStyle(borderThickness, borderColor, 1); // Use conditional border color
        this.graphics.strokeRect(this.x, this.y, squareSize, squareSize);
    
        // Draw the name at the bottom of the square
        if (!this.nameText) {
            this.nameText = scene.add.text(this.x + squareSize / 2, this.y + squareSize - 5, this.visual.name, {
                font: '24px Arial',
                fill: '#ffffff',
                stroke: '#000000',
                strokeThickness: 3
            });
            this.nameText.setOrigin(0.5, 1);
        }

        if (!this.numberText || this.redraw) {
            this.numberText?.destroy();
            this.redraw = false;
            this.numberText = scene.add.text(this.x + 5, this.y + 5, `${this.remaining}`, {
                font: '18px Arial',
                fill: '#ffffff',
                stroke: '#000000',
                strokeThickness: 3
            });
        }

        if (!this.letterText) {
            this.letterText = scene.add.text(this.x + squareSize - 5, this.y + 5, this.visual.letter, {
                font: '24px Arial',
                fill: '#ffffff',
                stroke: '#000000',
                strokeThickness: 3
            });
            this.letterText.setOrigin(1, 0);
        }

        if (clickable) {
            if (!this.pointerTriangle) {
                // If clickable is true and the pointerTriangle doesn't exist, create it
                this.pointerTriangle = scene.add.sprite(this.x - 30, this.y + squareSize / 2, 'filledTriangle');
                this.pointerTriangle.setTint(Phaser.Display.Color.GetColor(255, 102, 102)); // Light red color
                this.pointerTriangle.setOrigin(0.5, 0.5);
                this.pointerTriangle.setScale(4); // Scale up the triangle to make it bigger
                this.pointerTriangle.angle = 90; // Pointing to the right
        
                // Create the text associated with the pointerTriangle
                let z = 3 - this.credits;  // Calculate the value of z
                this.pointerTriangleText = scene.add.text(this.x - 45, this.y + squareSize / 2, `+${z}`, {
                    font: 'bold 24px Arial',
                    fill: '#000000'
                });
                this.pointerTriangleText.setOrigin(1, 0.5); // Align right to the triangle, centered vertically
            }
        } else {
            if (this.pointerTriangle) {
                // If clickable is false and the pointerTriangle exists, destroy both it and the text
                this.pointerTriangle.destroy();
        
                // Destroy the text as well
                this.pointerTriangleText.destroy();
            }
        }
        
    }

    addImageToScene(scene, x, y, imageKey, squareSize, percentage) {
        const imageSize = 90;
        // Check and initialize greyed-out image
        if (!this.imageGreyed) {
            this.imageGreyed = scene.add.image(
                x + squareSize / 2,
                y + squareSize / 2 - 10,
                imageKey
            );
            this.imageGreyed.setOrigin(0.5, 0.5);
            this.imageGreyed.setDisplaySize(imageSize, imageSize);
            this.imageGreyed.setAlpha(0.3); // Set low transparency for greyed-out effect
        }

        // Check and initialize fully visible image
        if (!this.imageVisible) {
            this.imageVisible = scene.add.image(
                x + squareSize / 2,
                y + squareSize / 2 - 10,
                imageKey
            );
            this.imageVisible.setOrigin(0.5, 0.5);
            this.imageVisible.setDisplaySize(imageSize, imageSize);
        }

        // Apply cropping to show progression
        const offset = squareSize / 2 - imageSize / 2 - 10;
        this.imageVisible.setCrop(
            0,
            squareSize - offset * (percentage - 0.1) * 10 + 2.5,
            squareSize,
            squareSize
        );
    }
}

