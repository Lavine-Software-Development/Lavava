import { Scene } from 'phaser';

export class Preloader extends Scene
{
    constructor() {
        super('Preloader');
    }

    preload() {

        // Prepare graphics assets
        this.createShapeTextures();
    }

    drawStar(graphics, centerX, centerY, radius) {
        let points = 5;
        let innerRadius = radius / 2;
    
        graphics.beginPath();
        graphics.moveTo(
            centerX + radius * Math.cos(0),
            centerY + radius * Math.sin(0)
        );
    
        for (let i = 1; i < points * 2; i++) {
            const angle = Math.PI / points * i;
            const r = (i % 2 === 0) ? radius : innerRadius;
            graphics.lineTo(
                centerX + r * Math.cos(angle),
                centerY + r * Math.sin(angle)
            );
        }
    
        graphics.closePath();
        graphics.fillPath();
        graphics.strokePath();
    }

    createShapeTextures() {
        const centre = 30;
        const siz = 0.8;
        const radius = 4 * siz; 

        let filledTriangle = this.add.graphics({ fillStyle: { color: 0xffffff } });
        filledTriangle.fillTriangle(centre + 0, centre - 8 * siz, centre - 7 * siz, centre + 4 * siz, centre + 7 * siz, centre + 4 * siz)
        filledTriangle.generateTexture('filledTriangle', 60, 60); // Bigger texture size
        filledTriangle.destroy();
    
        let outlinedTriangle = this.add.graphics({ lineStyle: { width: 0.5, color: 0xffffff } });
        outlinedTriangle.strokeTriangle(centre + 0, centre - 8 * siz, centre - 7 * siz, centre + 4 * siz, centre + 7 * siz, centre + 4 * siz); // Larger triangle
        outlinedTriangle.generateTexture('outlinedTriangle', 60, 60); // Bigger texture size
        outlinedTriangle.destroy();

        let filledCircle = this.add.graphics({ fillStyle: { color: 0xffffff } });
        filledCircle.fillCircle(centre, centre, radius);
        filledCircle.generateTexture('filledCircle', 60, 60);
        filledCircle.destroy();
    
        let outlinedCircle = this.add.graphics({ lineStyle: { width: 0.5, color: 0xffffff } });
        outlinedCircle.strokeCircle(centre, centre, radius);
        outlinedCircle.generateTexture('outlinedCircle', 60, 60);
        outlinedCircle.destroy();

        let star = this.add.graphics({ fillStyle: { color: 0xff69b4 }, lineStyle: { width: 0.5, color: 0x000000 } });
        this.drawStar(star, centre, centre, siz * 12); // siz * 12 to make the star large
        star.generateTexture('star', 60, 60);
        star.destroy();
    }

    create() {
        // Transition to next scene
        this.scene.start('MainScene');
    }
}
