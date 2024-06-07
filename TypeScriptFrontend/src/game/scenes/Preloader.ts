import { Scene } from 'phaser';

export class Preloader extends Scene
{
    constructor() {
        super('Preloader');
    }

    preload() {

        // Prepare graphics assets
        this.createTriangleTextures();
    }

    createTriangleTextures() {
        const centre = 30;
        const siz = 0.8;

        // Create a black filled triangle, make it larger for visibility
        let filledTriangle = this.add.graphics({ fillStyle: { color: 0xffffff } });
        filledTriangle.fillTriangle(centre + 0, centre - 8 * siz, centre - 7 * siz, centre + 4 * siz, centre + 7 * siz, centre + 4 * siz)
        filledTriangle.generateTexture('filledTriangle', 60, 60); // Bigger texture size
        filledTriangle.destroy();
    
        // Create a black outlined triangle, make it larger for visibility
        let outlinedTriangle = this.add.graphics({ lineStyle: { width: 0.5, color: 0xffffff } });
        outlinedTriangle.strokeTriangle(centre + 0, centre - 8 * siz, centre - 7 * siz, centre + 4 * siz, centre + 7 * siz, centre + 4 * siz); // Larger triangle
        outlinedTriangle.generateTexture('outlinedTriangle', 60, 60); // Bigger texture size
        outlinedTriangle.destroy();
    }

    create() {
        // Transition to next scene
        this.createTriangleTextures();
        this.scene.start('MainScene');
    }
}
