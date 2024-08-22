import { AbstractAbility, CreditAbility, ElixirAbility } from "./ReloadAbility";
import { IDItem } from "./idItem";
import { Highlight } from "./highlight";
import { Event } from "./event";
import { Node } from "./node";
import { phaserColor } from "./utilities";
import { Colors, AbilityElixir, AbilityCredits, AbilityReloadTimes } from "./constants";
import { ClickType } from "./enums";
import { VISUALS, CLICKS, } from "./default_abilities";
import { AbilityVisual } from "../objects/immutable_visuals";
import { ValidationFunction as ValidatorFunc}  from "./types";

/**
 * Represents an abstract class for managing abilities in a game.
 * Child classes must implement the `clickable`, and `makeAbilities` method.
 */
export class AbstractAbilityManager {
    abilities: { [key: number]: AbstractAbility };
    private events: { [key: number]: Event };
    private mode: number | null = null;
    private backupMode: number | null = null;
    clicks: IDItem[] = [];
    abilityText: Phaser.GameObjects.Text;
    BridgeGraphics: Phaser.GameObjects.Graphics;
    extraData: Set<number>;

    constructor(
        scene: Phaser.Scene,
        ability_values: any,
        validators: { [key: string]: ValidatorFunc },
        events: { [key: number]: Event },
    ) {
        this.abilities = {};
        this.makeAbilities(ability_values, validators, scene);
        this.events = events;
        this.BridgeGraphics = scene.add.graphics();

        const x = scene.sys.canvas.width - 10; // 10 pixels from the right edge
        const y = scene.sys.canvas.height - 30;

        this.abilityText = scene.add.text(x, y, "", {
            fontSize: "36px",
            align: "right",
            color: "#000000",
        });

        // Set origin to (1, 1) to align text to the bottom right
        this.abilityText.setOrigin(1, 1);
        this.extraData = new Set<number>();
    }

    makeAbilities(ability_values: any, validators: { [key: string]: ValidatorFunc }, scene: Phaser.Scene): void {
        throw new Error("Method not implemented.");
    }

    forfeit(): void {
        this.reset();
    }

    getMode(): number | null {
        return this.mode;
    }

    delete(): void {
        // Clear all graphics
        this.BridgeGraphics.clear();
        this.BridgeGraphics.destroy();
    
        // Remove the ability text if it exists
        if (this.abilityText) {
            this.abilityText.destroy();
        }
    
        // Call delete on each ability
        for (const key in this.abilities) {
            this.abilities[key].delete();
        }
    }

    updateSelection(): void {
        if (this.clicks.length > 0 && this.clicks[this.clicks.length - 1].type === ClickType.NODE) {
            let node = this.clicks[this.clicks.length - 1] as Node;
            node.select(true);
        }
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
        this.updateSelection();
        if (this.completeCheck(highlight.usage)) {
            const clickIds = this.clicks.map((click) => click.id);
            const extraDataArray = Array.from(this.extraData);
            const send_info = [...clickIds, ...extraDataArray];
            this.backupReset();
            return send_info;
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
            this.updateSelection();
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

    clickSelect(position): number | null {
        for (const key in this.abilities) {
            const ability = this.abilities[key];
            if (ability.overlapsWithSquare(position)) {
                return ability.id;
            }
        }
        return null;
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
        for (const click of this.clicks) {
            if (click.type === ClickType.NODE) {
                let node = click as Node;
                node.select(false);
            }
        }
        this.clicks = [];
        this.BridgeGraphics.clear();
        this.extraData.clear();
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
        return false;
    }

    select(key: number): boolean {
        if (this.event?.addons.has(key) && this.abilities[key].selectable) {    
            this.extraData.add(key);
        }
        else {
            if (this.mode) {
                this.wipe();
            }
            if (this.mode === key) {
                this.mode = null;
            } else if (this.abilities[key].selectable) {
                return this.switchTo(key);
            }
        }
        return false;
    }

    validate(item: IDItem): [IDItem, number] | false {
        if (
            this.event &&
            (item.type === this.event.clickType || item.type === ClickType.ABILITY) &&
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

    get ability(): AbstractAbility | null {
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
            this.abilityText.setText( this.ability.visual.name);
            if (
                (this.ability?.visual.name == "Bridge" || this.ability?.visual.name == "D-Bridge" || this.ability?.visual.name == "Mini-Bridge") &&
                this.clicks.length > 0
            ) {
                this.drawBridge(scene);   
            }
        } else {
            this.abilityText.setText("");
        }
    
        for (let key in this.abilities) {
            const isSelected = this.mode === parseInt(key);
            let clickable = this.clickable(key);
            this.abilities[key].draw(scene, isSelected, clickable);
        }
    }

    clickable(key): boolean {
        throw new Error("Method not implemented.");
    }

    private drawBridge(scene: Phaser.Scene) {
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
        if (this.ability?.visual.name == "D-Bridge" || this.ability?.visual.name == "Mini-Bridge") {
            this.drawArrowWithCircles(startX, startY, normX, normY, magnitude, phaserColor(Colors.YELLOW));
        }
        else {
            this.drawArrow(startX, startY, normX, normY, magnitude, phaserColor(Colors.YELLOW));
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
        const minSpacing = 12;

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

    drawArrowWithCircles(
        startX: number,
        startY: number,
        normX: number,
        normY: number,
        magnitude: number,
        color: number
    ): void {
        const circleRadius = 3;
        const triangleSize = 11;
        const minSpacing = 8;
    
        // Calculate the number of circles to draw based on the space and circle radius
        const numCircles = Math.floor((magnitude - triangleSize) / minSpacing);
        const spacing = (magnitude - triangleSize) / numCircles;
    
        for (let i = 1; i < numCircles; i++) {
            let x = startX + i * spacing * normX;
            let y = startY + i * spacing * normY;
    
            this.BridgeGraphics.beginPath();
            this.BridgeGraphics.arc(x, y, circleRadius, 0, 2 * Math.PI);
            this.BridgeGraphics.closePath();
    
            this.BridgeGraphics.fillStyle(color);
            this.BridgeGraphics.fill();
        }
    
        // Draw the final triangle in light green
        let finalX = startX + (magnitude - spacing) * normX;
        let finalY = startY + (magnitude - spacing) * normY;
        let angle = Math.atan2(normY, normX);
    
        this.BridgeGraphics.beginPath();
        this.BridgeGraphics.moveTo(finalX, finalY);
        this.BridgeGraphics.lineTo(
            finalX - Math.cos(angle - Math.PI / 6) * triangleSize,
            finalY - Math.sin(angle - Math.PI / 6) * triangleSize
        );
        this.BridgeGraphics.lineTo(
            finalX - Math.cos(angle + Math.PI / 6) * triangleSize,
            finalY - Math.sin(angle + Math.PI / 6) * triangleSize
        );
        this.BridgeGraphics.closePath();
    
        // Define the light green color for the final triangle
        this.BridgeGraphics.fillStyle(Phaser.Display.Color.GetColor(144, 238, 144)); // Light green
        this.BridgeGraphics.fill();
    }
    
}

export class CreditAbilityManager extends AbstractAbilityManager {

    _credits: number = 0;
    bonusCreditsText: Phaser.GameObjects.Text;

    constructor(
        scene: Phaser.Scene,
        ability_values: { [x: string]: number },
        validators:  { [key: string]: ValidatorFunc } ,
        events: { [key: number]: Event },
    ) {
        super(scene, ability_values, validators, events);
        this.bonusCreditsText = scene.add.text(scene.sys.canvas.width - 90, 35 + (165 * ability_values.length), "", {
            fontSize: "60px",
            align: "right",
            color: "#000000",
        });
    }

    makeAbilities(abilityCounts: { [x: string]: number }, validators: { [key: string]: ValidatorFunc }, scene: Phaser.Scene): void {

        let y_position = 20;
        const spacing = 15; // Spacing between squares
        const squareSize = 150; // Size of each square
        const unaltered_x_position = scene.scale.width - squareSize - 10;

        Object.entries(abilityCounts).forEach(([abk, count]) => {
            // abk here is the ability code (converted from the name via NameToCode)
            const abilityCode = parseInt(abk);
            this.abilities[abilityCode] = new CreditAbility(
                VISUALS[abilityCode] as AbilityVisual,
                CLICKS[abilityCode][0],
                CLICKS[abilityCode][1],
                validators[abilityCode],
                AbilityCredits[abilityCode],
                AbilityReloadTimes[abilityCode],
                abilityCode,
                count, // Use the count from abilityCounts
                unaltered_x_position,
                y_position,
                scene,
                squareSize
            );
    
            y_position += squareSize + spacing;
        });
    }

    clickable(key): boolean {
        return this.credits >= this.abilities[key].credits;
    }

    get credits(): number {
        return this._credits;
    }

    set credits(value: number) {
        this._credits = value;
        if (value == 0) {
            this.bonusCreditsText.setText("");
            return
        }
        else {
            this.updateBonusCreditsText(value);
        }
    }

    updateBonusCreditsText(value: number): void {
        this.bonusCreditsText.setText(`+${value}`);
    }

    triangle_validate(position: Phaser.Math.Vector2): [IDItem, number] | false {
        // loop through all the abilities values, and pass them into validate
        for (const key in this.abilities) {
            const ability = this.abilities[key] as CreditAbility;
            if (ability.overlapsWithTriangle(position)) {
                const item = this.validate(ability);
                if (item) {
                    return item;
                }
            }
        }
        return false;
    }

    delete() {
        super.delete();
        
        if (this.bonusCreditsText) {
            this.bonusCreditsText.destroy();
        }
    }
}


export class ElixirAbilityManager extends AbstractAbilityManager {
    private _elixir: number = 0;
    private elixirCapacity: number;
    private elixirBar: Phaser.GameObjects.Graphics;
    private barWidth: number;
    private barPadding: number;
    private bar_color: readonly [number, number, number];

    constructor(
        scene: Phaser.Scene,
        ability_values: { [x: string]: number },
        validators:  { [key: string]: ValidatorFunc } ,
        events: { [key: number]: Event },
        capacity: number,
        bar_color: readonly [number, number, number]
    ) {
        super(scene, ability_values, validators, events);
        this.elixirCapacity = capacity;
        this._elixir = 0;
        this.bar_color = bar_color;

        // Create the elixir bar
        this.elixirBar = scene.add.graphics();
        this.barWidth = 30;
        this.barPadding = 5;
        this.updateElixirBar(scene);
    }

    makeAbilities(abilityCounts: { [x: string]: number }, validators: { [key: string]: ValidatorFunc }, scene: Phaser.Scene): void {

        this.barWidth = 30;
        this.barPadding = 5;
        console.log(abilityCounts)

        let y_position = 20;
        const spacing = 15; // Spacing between squares
        const topPadding = 20;
        const absHeight = scene.sys.canvas.height - topPadding - 60 - this.barPadding * 2;
        const squareSize = Math.min((absHeight - (spacing * (Object.keys(abilityCounts).length - 1))) / Object.keys(abilityCounts).length, 180); // Size of each square
        const unaltered_x_position = scene.scale.width - squareSize - this.barWidth - this.barPadding - 10;
        console.log("Square size: ", squareSize);

        Object.entries(abilityCounts).forEach(([abk, count]) => {
            const abilityCode = parseInt(abk);
            this.abilities[abilityCode] = new ElixirAbility(
                VISUALS[abilityCode] as AbilityVisual,
                CLICKS[abilityCode][0],
                CLICKS[abilityCode][1],
                validators[abilityCode],
                AbilityElixir[abilityCode], // Assuming this exists, replace with actual elixir cost
                abilityCode,
                unaltered_x_position,
                y_position,
                scene,
                squareSize
            );
    
            y_position += squareSize + spacing;
        });
    }

    get elixir(): number {
        return this._elixir;
    }

    set elixir(value: number) {
        this._elixir = Math.min(value, this.elixirCapacity);
        this.updateElixirBar(this.elixirBar.scene);

        // garbage code right here. Do better
        for (const key in this.abilities) {
            const ability = this.abilities[key] as ElixirAbility;
            if (ability.percentage === 0) {
                ability.percentage = Math.min(this._elixir / AbilityElixir[key], 1);
            }
        }
    }

    clickable(key: string): boolean {
        return this.elixir >= this.abilities[key].elixir;
    }

    private updateElixirBar(scene: Phaser.Scene): void {
        const canvasHeight = scene.sys.canvas.height;
        const canvasWidth = scene.sys.canvas.width;
        const topPadding = 20;

        const barHeight = canvasHeight - topPadding - 60 - this.barPadding * 2;
        const barX = canvasWidth - this.barWidth - this.barPadding;
        const barY = topPadding;

        this.elixirBar.clear();

        // Draw background
        this.elixirBar.fillStyle(0xcccccc);
        this.elixirBar.fillRect(barX, barY, this.barWidth, barHeight);

        // Draw filled portion
        const fillHeight = (this._elixir / this.elixirCapacity) * barHeight;
        this.elixirBar.fillStyle(phaserColor(this.bar_color));
        this.elixirBar.fillRect(barX, barY + barHeight - fillHeight, this.barWidth, fillHeight);

        // Draw section dividers
        const sectionHeight = barHeight / this.elixirCapacity;
        const dividerThickness = 1;
        const dividerSpacing = 1;

        for (let i = 1; i < this.elixirCapacity; i++) {
            const dividerY = barY + barHeight - i * sectionHeight;

            // Draw first black line
            this.elixirBar.fillStyle(0x000000);
            this.elixirBar.fillRect(barX, dividerY - dividerThickness, this.barWidth, dividerThickness);

            // Draw white space/line
            this.elixirBar.fillStyle(0xFFFFFF);
            this.elixirBar.fillRect(barX, dividerY - dividerThickness + dividerSpacing, this.barWidth, dividerThickness);

            // Draw second black line
            this.elixirBar.fillStyle(0x000000);
            this.elixirBar.fillRect(barX, dividerY - dividerThickness + 2 * dividerSpacing, this.barWidth, dividerThickness);
        }

        // Draw border
        this.elixirBar.lineStyle(2, 0x000000);
        this.elixirBar.strokeRect(barX, barY, this.barWidth, barHeight);
    }

    delete() {
        super.delete();
        if (this.elixirBar) {
            this.elixirBar.destroy();
        }
    }
}