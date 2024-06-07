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
    }

    create() {
        // Transition to next scene
        this.scene.start('MainScene');
    }
}
