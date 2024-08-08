import { Node, PortNode, WallNode } from "../objects/node";
import { Highlight } from "../objects/highlight";
import { CannonState, stateDict } from "../objects/States";
import {
    Colors,
    KeyCodes,
    NameToCode,
    stateCodes,
    EventCodes,
    PRE_STRUCTURE_RANGES,
    PlayerColors,
    NUKE_OPTION_STRINGS,
    NUKE_OPTION_CODES, 
    MINI_BRIDGE_RANGE,
    attackCodes,
} from "../objects/constants";
import { PlayerStateEnum as PSE, GameStateEnum as GSE } from "../objects/enums";
import { AbstractAbility, CreditAbility, ElixirAbility } from "../objects/ReloadAbility";
import { Event } from "../objects/event";
import { AbstractAbilityManager, CreditAbilityManager, ElixirAbilityManager } from "../objects/abilityManager";
import { OtherPlayer } from "../objects/otherPlayer";
import { MyCreditPlayer, MyElixirPlayer } from "../objects/myPlayer";
import {
    makeEventValidators,
    unownedNode,
    makeAbilityValidators,
} from "../objects/ability_validators";
import { IDItem } from "../objects/idItem";
import { CLICKS, EVENTS, VISUALS } from "../objects/default_abilities";
import { Network } from "../objects/network";
import {
    abilityCountsConversion,
    cannonAngle,
    phaserColor,
} from "../objects/utilities";

import { Scene } from "phaser";

import { Edge } from "../objects/edge";

const positions = [
    { xPercent: 2, yPercent: 99 },    // 2% from left, 99% from top
    { xPercent: 24, yPercent: 99 },   // 27% from left, 99% from top
    { xPercent: 46, yPercent: 99 },   // 52% from left, 99% from top
    { xPercent: 68, yPercent: 99 }    // 77% from left, 99% from top
];

export class MainScene extends Scene {
    private nodes: { [key: string]: Node } = {};
    private edges: { [key: string]: Edge } = {};
    private highlight: Highlight;
    private ps: PSE;
    private gs: GSE;
    private abilityManager: AbstractAbilityManager;
    private mainPlayer: OtherPlayer;
    private otherPlayers: OtherPlayer[] = [];
    private network: Network;
    private burning: Node[] = [];
    private abilityCounts: { [key: string]: number };

    private graphics: Phaser.GameObjects.Graphics;
    private board: any;
    private countdown: number;
    private full_capitals: number[];
    private lastCounts: number [];

    private timerText: Phaser.GameObjects.Text;
    private capitalTexts: Phaser.GameObjects.Text[] = [];
    private countTexts: Phaser.GameObjects.Text[] = [];
    private statusText: Phaser.GameObjects.Text;
    private eliminatedText: Phaser.GameObjects.Text;
    private eloText: Phaser.GameObjects.Text;
    private eloDifference: Phaser.GameObjects.Text; //text example
    private leaveMatchButton: Phaser.GameObjects.Text;
    private navigate: Function;
    private reconnectionEvent: Phaser.Time.TimerEvent | null = null;
    private ratio: [number, number];
    private settings: any;
    private mode: string;

    private progressBar: Phaser.GameObjects.Graphics;
    private progressLine: Phaser.GameObjects.Graphics;
    private overtimeColor: number = 0xFF69B4; // Hot Pink
    private mainTimeColor: number;
    private barWidth: number;
    private barHeight: number = 20; // Increased height
    private barY: number = 10; // Space from the top
    private markerTexts: Phaser.GameObjects.Text[] = [];

    private rainbowColors: string[] = [
        "#B8860B", // Dark Goldenrod
        "#8B4513", // Saddle Brown
        "#006400", // Dark Green
        "#800000", // Maroon
        "#4B0082", // Indigo
    ];
    private rainbowIndex: number = 0;

    constructor(config, props, network: Network, navigate: Function) {
        super({ key: "MainScene" });
        this.board = props;
        this.network = network;
        this.navigate = navigate;
        this.network.updateCallback = this.update_data.bind(this);
        this.network.leaveGameCallback = this.leaveMatchDirect.bind(this);
        this.burning = [];
        const storedAbilities = sessionStorage.getItem("selectedAbilities");

        const abilitiesFromStorage = storedAbilities
            ? JSON.parse(storedAbilities)
            : [];

        // Create a map from ability code to count using the NameToCode mapping
        this.abilityCounts = abilityCountsConversion(abilitiesFromStorage);

        this.countdown = 0;
        this.full_capitals = [0, 0];
    }

    preload() {
        //  load ability icon assets
        this.load.setPath("assets/abilityIcons/");

        this.load.image("Bridge", "Bridge.png");
        this.load.image("Burn", "Burn.png");
        this.load.image("Cannon", "Cannon.png");
        this.load.image("Capital", "Capital.png");
        this.load.image("D-Bridge", "D-Bridge.png");
        this.load.image("Mini-Bridge", "D-Bridge.png");
        this.load.image("Freeze", "Freeze.png");
        this.load.image("Nuke", "Nuke.png");
        this.load.image("Poison", "Poison.png");
        this.load.image("Rage", "Rage.png");
        this.load.image("Spawn", "Spawn.png");
        this.load.image("Zombie", "Zombie.png");

        this.load.image('Pump', 'Pump.png');

        this.load.image("Over-Grow", "Over-Grow.png");
        this.load.image("Catapult", "Catapult.png");
        this.load.image("Wormhole", "Wormhole.png");
        this.load.image("Wall", "Wall.png");
    }

    create(): void {
        this.graphics = this.add.graphics();

        this.initialize_data();

        this.highlight = new Highlight(this, this.mainPlayer.color);
        this.ps = PSE.START_SELECTION;
        this.gs = GSE.START_SELECTION;

        this.createAbilityManager();

        this.createLeaveMatchButton();

        this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
            if (pointer.leftButtonDown()) {
                this.mouseButtonDownEvent(EventCodes.STANDARD_LEFT_CLICK);
            } else if (pointer.rightButtonDown()) {
                this.mouseButtonDownEvent(EventCodes.STANDARD_RIGHT_CLICK);
            }
        });

        this.input.keyboard!.on("keydown", (event: KeyboardEvent) => {
            this.keydown(event.key.charCodeAt(0));
            this.checkHighlight();
        });

        this.input.on("pointermove", (pointer: Phaser.Input.Pointer) => {
            this.checkHighlight();
        });

        this.scale.on("resize", this.handleResize, this);

        this.startReconnectionCheck();

        Object.values(this.nodes).forEach((node) => node.draw());
        Object.values(this.edges).forEach((edge) => edge.draw());

        // main time is color is light purple
        this.mainTimeColor = 0x9370DB;
        this.createProgressBar();
    }

    getEdges(): Edge[] {
        return Object.values(this.edges);
    }

    private createProgressBar(): void {
        const gameWidth = this.sys.game.config.width as number;
        this.barWidth = gameWidth * 0.5; // Half the screen width
        const barX = gameWidth * 0.6 - this.barWidth / 2; // Centered at 60%
    
        this.progressBar = this.add.graphics();
        this.progressLine = this.add.graphics();
    
        // Draw the main time portion of the bar
        this.progressBar.fillStyle(this.mainTimeColor, 1);
        this.progressBar.fillRect(barX, this.barY, this.barWidth * (this.settings.main_time / (this.settings.main_time + this.settings.overtime)), this.barHeight);
    
        // Draw the overtime portion of the bar
        this.progressBar.fillStyle(this.overtimeColor, 1);
        this.progressBar.fillRect(
            barX + this.barWidth * (this.settings.main_time / (this.settings.main_time + this.settings.overtime)), 
            this.barY, 
            this.barWidth * (this.settings.overtime / (this.settings.main_time + this.settings.overtime)), 
            this.barHeight
        );
    
        // Draw accessibility marks if needed
        if (this.settings.iterative_make_accessible) {
            this.drawAccessibilityMarks(barX);
        }
    
        // Initialize the progress line (taller than the bar)
        this.progressLine.fillStyle(0x000000, 1); // Black line
        this.progressLine.fillRect(barX, this.barY - 5, 4, this.barHeight + 10); // 2 pixels wide, extending beyond the bar


        const overtimeWidth = this.barWidth * (this.settings.overtime / (this.settings.main_time + this.settings.overtime));
        const overtimeX = barX + this.barWidth * (this.settings.main_time / (this.settings.main_time + this.settings.overtime));
        this.add.text(overtimeX + overtimeWidth / 2, this.barY + this.barHeight / 2, "Overtime", {
            fontFamily: 'Arial',
            fontSize: '14px',
            color: '#FFFFFF'
        }).setOrigin(0.5);
    }
    
    private drawAccessibilityMarks(barX: number): void {
        this.progressBar.fillStyle(0x000000, 0.5); // Semi-transparent black
        this.settings.accessibility_times.forEach(time => {
            const markX = barX + (time / this.settings.main_time) * this.barWidth * (this.settings.main_time / (this.settings.main_time + this.settings.overtime));
            this.progressBar.fillRect(markX, this.barY - 5, 2, this.barHeight + 10) ; // 2-pixel wide marks
            this.markerTexts.push(
                this.add.text(markX, this.barY + this.barHeight + 5, "Walls Down", {
                    fontFamily: 'Arial',
                    fontSize: '10px',
                    color: '#000000'
                }).setOrigin(0.5, 0)
            );
        });
    }
    
    private updateProgressBar(): void {
        const gameWidth = this.sys.game.config.width as number;
        const barX = gameWidth * 0.6 - this.barWidth / 2;
        const totalTime = this.settings.main_time + this.settings.overtime;
        let progress = 0;
    
        if (this.gs < GSE.PLAY) {
            progress = 0;
        } else if (this.gs === GSE.PLAY) {
            progress = (this.settings.main_time - this.countdown) / totalTime;
        } else if (this.gs >= GSE.END_GAME) {
            progress = (this.settings.main_time + (this.settings.overtime - this.countdown)) / totalTime;
        }
    
        // Ensure progress doesn't exceed 1
        progress = Math.min(progress, 1);
    
        // Update the position of the progress line
        this.progressLine.clear();
        this.progressLine.fillStyle(0x000000, 1);
        this.progressLine.fillRect(barX + this.barWidth * progress, this.barY - 5, 4, this.barHeight + 10);
    }

    private createAbilityManager() {
        const ev = makeEventValidators(this.mainPlayer, this.getEdges.bind(this));
        const ab_validators = makeAbilityValidators(
            this.mainPlayer,
            this.ratio,
            this.settings,
            Object.values(this.nodes),
            this.getEdges.bind(this)
        );
        const events: { [key: number]: Event } = {};
        Object.values(EventCodes).forEach((eb: number) => {
            events[eb] = new Event(
                VISUALS[eb],
                EVENTS[eb][0],
                EVENTS[eb][1],
                ev[eb]
            );
        });

        if (this.mode == "Royale") {
            this.abilityManager = new ElixirAbilityManager(
                this,
                this.settings.deck,
                ab_validators,
                events,
                this.settings.elixir_cap,
                this.mainPlayer.color
            );
        }
        else {
            this.abilityManager = new CreditAbilityManager(this, this.abilityCounts, ab_validators, events);
        }

    }

    private getRainbowColor(): string {
        const color = this.rainbowColors[this.rainbowIndex];
        this.rainbowIndex = (this.rainbowIndex + 1) % this.rainbowColors.length;
        return color;
    }

    startReconnectionCheck(): void {
        // Clear any existing event first
        if (this.reconnectionEvent) {
            this.reconnectionEvent.remove();
        }

        // Use Phaser's time events instead of setInterval
        this.reconnectionEvent = this.time.addEvent({
            delay: 1000, // Check every 5 seconds
            callback: this.checkConnection,
            callbackScope: this,
            loop: true,
        });
    }

    checkConnection(): void {
        if (
            !this.network.socket ||
            this.network.socket.readyState === WebSocket.CLOSED
        ) {
            console.log("Detected disconnection, attempting to reconnect...");
            this.network.attemptReconnect();
        }
    }

    forfeit(code: number): void {
        console.log("Forfeiting");
        this.simple_send(code);
        this.abilityManager.forfeit();
    }

    keydown(key: number): void {
        if (key === stateCodes.OVERRIDE_RESTART_CODE) {
            this.simple_send(stateCodes.RESTART_CODE);
        } else if (this.ps === PSE.VICTORY && key === stateCodes.RESTART_CODE) {
            this.simple_send(stateCodes.RESTART_CODE);
        } else if (this.ps === PSE.PLAY) {
            this.abilitySelection(key);
            if (key === stateCodes.FORFEIT_CODE) {
                this.simple_send(stateCodes.FORFEIT_CODE);
            }
        } else {
            console.log("Not playing");
        }
    }

    handleResize(gameSize) {
        console.log("Resizing");
    }

    abilitySelection(key: number): void {
        if (this.abilityManager.inAbilities(key)) {
            if (this.abilityManager.select(key)) {
                this.simple_send(key);
            }
        }
    }

    private drawScaledCircle(
        node: Node,
        radius: number,
        color: readonly [number, number, number]
    ): void {
        const [ratioX, ratioY] = this.ratio;
        this.graphics.lineStyle(3, phaserColor(color), 1);

        // Draw the ellipse, scaling it appropriately
        this.graphics.strokeEllipse(
            node.pos.x,
            node.pos.y,
            radius * 2 * ratioX, // radus * 2 to get diameter
            radius * 2 * ratioY
        );
    }

    update(): void {
        this.graphics.clear();
        this.abilityManager.draw(this);

        // Iterate over the values of the dictionary to draw each node

        if ( attackCodes.includes(this.abilityManager.getMode()) ) {
            if (this.settings.attack_type == 'structure_range') {
                const structures = Object.values(this.nodes).filter(
                    (node) =>
                        NUKE_OPTION_STRINGS.includes(node.stateName) &&
                        node.owner === this.mainPlayer
                );
    
                structures.forEach((node) => {
                    this.drawScaledCircle(node, node.value * node.state.attack_range, Colors.BLACK);
                });
            } else if (this.settings.attack_type == 'neighbor') {
                const neighbors = Object.values(this.nodes).filter(
                    (node) => node.owner != this.mainPlayer && node.edges.some((edge) => edge.other(node).owner === this.mainPlayer)
                );
    
                neighbors.forEach((node) => {
                    this.graphics.strokeCircle(
                        node.pos.x,
                        node.pos.y,
                        node.size + 8
                    );
                });
            }

        } else if (this.highlight.usage !== null && NUKE_OPTION_CODES.includes(this.highlight.usage)) {
            const highlightedNode = this.highlight.item as Node;
            this.drawScaledCircle(highlightedNode, PRE_STRUCTURE_RANGES[this.highlight.usage], Colors.BLACK);
        } else if (
            this.highlight.usage == KeyCodes.MINI_BRIDGE_CODE &&
            this.abilityManager.clicks.length == 0
        ) {
            const node = this.highlight.item as Node;
            this.drawScaledCircle(node, MINI_BRIDGE_RANGE, Colors.PINK);
        } else if (
            this.abilityManager.getMode() == KeyCodes.MINI_BRIDGE_CODE &&
            this.abilityManager.clicks.length > 0
        ) {
            const node = this.abilityManager.clicks[0] as Node;
            this.drawScaledCircle(node, MINI_BRIDGE_RANGE, Colors.PINK);
        }
    }

    addToBurn(node: Node): void {
        this.burning.push(node);
    }

    checkHighlight(): void {
        if (this.ps > PSE.PLAY) {
            return;
        }
        let pointer = this.input.activePointer;
        let hoverResult = this.validHover(
            new Phaser.Math.Vector2(pointer.x, pointer.y)
        );

        if (hoverResult !== false) {
            this.highlight.set(hoverResult[0], hoverResult[1]);
        } else {
            this.highlight.wipe();
        }
        this.highlight.draw();
    }

    validHover(position: Phaser.Math.Vector2): [IDItem, number] | false {
        for (const node of Object.values(this.nodes)) {
            if (node.pos.distance(position) < node.size) {
                // Assuming a proximity check
                if (this.ps === PSE.START_SELECTION) {
                    if (unownedNode([node])) {
                        return [node, KeyCodes.SPAWN_CODE];
                    }
                } else if (this.ps === PSE.PLAY) {
                    let validation = this.abilityManager.validate(node);
                    if (validation) {
                        return validation;
                    }
                }
            }
        }

        for (const edge of Object.values(this.edges)) {
            if (edge.isNear(position)) {
                // You need to define how to check proximity to an edge
                if (this.ps === PSE.PLAY) {
                    return this.abilityManager.validate(edge);
                }
            }
        }

        if (this.ps === PSE.PLAY && this.mode === "Original") {
            let manager = this.abilityManager as CreditAbilityManager;
            let ability = manager.triangle_validate(position);
            if (ability) {
                return ability;
            }
        }

        return false;
    }

    mouseButtonDownEvent(button: number): void {
        if (this.highlight.highlighted) {
            if (this.ps === PSE.START_SELECTION) {
                this.send();
            } else {
                if (this.abilityManager.useAbility(this.highlight)) {
                    const completion = this.abilityManager.completeAbility();
                    if (completion !== false) {
                        this.send(completion);
                    }
                } else {
                    const event_data = this.abilityManager.useEvent(
                        this.highlight
                    );
                    if (event_data !== false) {
                        if (
                            button === EventCodes.STANDARD_RIGHT_CLICK &&
                            this.highlight.usage ===
                                EventCodes.STANDARD_LEFT_CLICK
                        ) {
                            this.send(
                                event_data,
                                EventCodes.STANDARD_RIGHT_CLICK
                            );
                        } else {
                            this.send(event_data);
                        }
                    }
                }
            }
        } else {
            // added this else
            let key = this.abilityManager.clickSelect(
                this.input.activePointer.position
            );
            if (key && this.ps === PSE.PLAY) {
                this.abilitySelection(key);
            }
        }
    }

    send(items?: number[], code?: number): void {
        this.network.sendMessage(this.highlight.sendFormat(items, code));
    }
    simple_send(code: number): void {
        this.network.sendMessage({ code: code, items: {} });
    }

    private createLeaveMatchButton(): void {
        this.leaveMatchButton = this.add.text(10, 10, "Forfeit", {
            fontFamily: "Arial",
            fontSize: "20px",
            backgroundColor: this.rgbToHex(this.mainPlayer.color),
            padding: { x: 10, y: 5 },
            color: "#fff",
        });
        this.leaveMatchButton.setInteractive({ useHandCursor: true });
        this.leaveMatchButton.on("pointerdown", () => this.leaveMatch());
    }

    private leaveMatch(code: number = stateCodes.FORFEIT_CODE): void {
        if (this.ps < PSE.ELIMINATED) {
            this.forfeit(code);
        } else {
            this.leaveMatchDirect();
        }
    }

    private leaveMatchDirect(): void {
        console.log("Leaving match...");
        this.network.disconnectWebSocket();
        this.navigate("/home");
    }

    initialize_data(): void {
        this.ratio = [
            (this.sys.game.config.width as number) / 1000,
            (this.sys.game.config.height as number) / 700,
        ];

        let startData = this.board;
        const pi = Number(startData.player_id.toString());
        const pc = startData.player_count;
        const n = startData.board.nodes;
        const e = startData.board.edges;
        const display = startData.display_names_list;

        this.settings = startData.settings;
        this.mode = startData.mode;
        
        if (this.mode === "Royale") {
            this.mainPlayer = new MyElixirPlayer(String(pi), PlayerColors[pi]);
        } else {
            this.mainPlayer = new MyElixirPlayer(String(pi), PlayerColors[pi]);
        }
        
        this.otherPlayers = Array.from({ length: pc }, (_, index) => {
            const id = index.toString();
            return id !== pi.toString()
                ? new OtherPlayer(id, PlayerColors[index])
                : this.mainPlayer;
        });

        this.displayNames(display);

        this.nodes = {};

        if (this.settings.walls) {
            this.nodes = Object.fromEntries(
                Object.keys(n).map((id) => [
                    id,
                    new WallNode(
                        Number(id),
                        n[id]["pos"] as [number, number],
                        n[id]["wall_count"],
                        stateDict[n[id]["state"]](this.settings.full_size),
                        n[id]["value"],
                        this
                    ),
                ])
            );
        } else {
            this.nodes = Object.fromEntries(
                Object.keys(n).map((id) => [
                    id,
                    new PortNode(
                        Number(id),
                        n[id]["pos"] as [number, number],
                        n[id]["is_port"],
                        stateDict[n[id]["state"]](this.settings.full_size),
                        n[id]["value"],
                        this
                    ),
                ])
            );
        }

        this.parse(this.edges, e, false);

        VISUALS[NameToCode["Spawn"]].color = this.mainPlayer.color;
    }

    delete_data(): void {
        Object.values(this.nodes).forEach((node) => node.delete());
        Object.values(this.edges).forEach((edge) => edge.delete());
        this.abilityManager.delete();
        this.progressBar.destroy();
        this.progressLine.destroy();
        this.timerText.destroy();
        this.nodes = {};
        this.edges = {};
        // destroy all the texts in markerTexts
        this.markerTexts.forEach(text => text.destroy());
    }

    update_data(new_data) {
        if (new_data != "Players may join") {
            if (!("abilities" in new_data)) {
                if (this.ps != new_data["player"]["ps"]) {
                    this.ps = new_data["player"]["ps"] as PSE;
                    if (this.statusText) this.statusText.destroy();
                    if (this.ps >= PSE.ELIMINATED) {
                        this.leaveMatchButton.setText("Leave Match");
                    }
                    if (this.ps > PSE.ELIMINATED) {
                        this.delete_data();
                        this.statusText = this.add.text(
                            (this.sys.game.config.width as number) - 100,
                            0,
                            `${PSE[this.ps]}`,
                            {
                                fontFamily: "Arial",
                                fontSize: "48px",
                                color: this.rgbToHex(this.mainPlayer.color),
                            }
                        );
                        this.statusText.setOrigin(1, 0);
                    }
                }

                if ('credits' in new_data["player"]) {
                    let mainPlayer = this.mainPlayer as MyCreditPlayer;
                    if (new_data["player"]["credits"] !== mainPlayer.credits) {
                        mainPlayer.credits = new_data["player"]["credits"];
                        let manager = this.abilityManager as CreditAbilityManager;
                        manager.credits = new_data["player"]["credits"];
                    }
                } else if ('a_elixir' in new_data["player"]) {
                    let mainPlayer = this.mainPlayer as MyElixirPlayer;
                    if (new_data["player"]["a_elixir"] !== mainPlayer.elixir) {
                        mainPlayer.elixir = new_data["player"]["a_elixir"];
                        let manager = this.abilityManager as ElixirAbilityManager;
                        manager.elixir = new_data["player"]["a_elixir"];
                    }
                }

                if (this.gs != new_data["gs"]) {
                    this.gs = new_data["gs"] as GSE;
                    this.updateProgressBar();
                }

                if (!this.eloText && new_data.hasOwnProperty("new_elos")) {
                    let difference =
                        Number(new_data["new_elos"][1]) -
                        Number(new_data["new_elos"][0]);
                    let color = difference > 0 ? Colors.GREEN : Colors.RED;
                    let symbol = difference > 0 ? "+" : "";
                    this.eloText = this.add.text(
                        300,
                        400,
                        `Elo: ${new_data["new_elos"][0]} -> ${new_data["new_elos"][1]}`,
                        {
                            fontFamily: "Arial",
                            fontSize: "24px",
                            color: "#000000",
                        }
                    );
                    this.eloText.setOrigin(0, 0);
                    this.eloDifference = this.add.text(
                        310,
                        360,
                        `(${symbol}${difference})`,
                        {
                            fontFamily: "Arial",
                            fontSize: "24px",
                            color: this.rgbToHex(color),
                        }
                    );
                }

                if (this.countdown != new_data["countdown_timer"].toFixed(0)) {
                    // make into integer
                    this.countdown = new_data["countdown_timer"].toFixed(0);

                    if (this.timerText) this.timerText.destroy();

                    let timerColor: string;
                    let timerWords: string;

                    if (this.ps < PSE.PLAY) {
                        timerColor = this.rgbToHex(this.mainPlayer.color);
                        timerWords = `Choose Start: ${this.countdown}`;
                    } else if (this.gs >= GSE.END_GAME) {
                        timerColor = this.getRainbowColor();
                        timerWords = `Overtime - Free Attack: ${this.countdown}`;
                    } else {
                        timerColor = this.rgbToHex(Colors.BLACK);
                        timerWords = `Standard Time: ${this.countdown}`;
                    }

                    this.timerText = this.add.text(450, 10, timerWords, {
                        fontFamily: "Arial",
                        fontSize: "24px",
                        color: timerColor,
                    });
                    this.timerText.setOrigin(1, 0);

                    this.updateProgressBar();
                }

                const updateDisplays = () => {
                    const players = Object.keys(this.lastCounts);
                
                    // Display positions for up to 4 players
                
                    // Clear existing texts
                    if (this.capitalTexts) {
                        this.capitalTexts.forEach(text => text.destroy());
                    }
                    if (this.countTexts) {
                        this.countTexts.forEach(text => text.destroy());
                    }
                
                    this.capitalTexts = [];
                    this.countTexts = [];
                
                    // Display capital counts and regular counts for up to 4 players
                    players.slice(0, 4).forEach((playerName, index) => {
                        const capitalCount = this.full_capitals[playerName];
                        const regularCount = new_data["counts"][playerName];
                        const position = positions[index];
                
                        const x = (position.xPercent / 100) * (this.sys.game.config.width as number);
                        const y = (position.yPercent / 100) * (this.sys.game.config.height as number);

                        let count_y = y - 20;
                        if (this.settings.starting_structures) {
                            count_y = y -  40;
                        }
                
                        const playerColor = this.rgbToHex(this.otherPlayers[playerName].color);
                
                        // Display regular count
                        const countText = this.add.text(
                            x,
                            count_y, // 30 pixels above the capital count
                            `Count: `,
                            {
                                fontFamily: "Arial",
                                fontSize: "19px", // Slightly smaller font
                                color: playerColor,
                            }
                        );
                        countText.setOrigin(0, 1);  // Align to bottom-left
                        
                        const countNumber = this.add.text(
                            countText.x + countText.width,
                            count_y,
                            `${regularCount}`,
                            {
                                fontFamily: "Arial",
                                fontSize: "19px",
                                color: '#000000', // Black color for the number
                            }
                        );
                        countNumber.setOrigin(0, 1);
                
                        this.countTexts.push(countText, countNumber);
                
                        if (this.settings.starting_structures) {
                            // Display full capital count
                            const capitalText = this.add.text(
                                x,
                                y - 15,
                                `Full Capitals: `,
                                {
                                    fontFamily: "Arial",
                                    fontSize: "23px",
                                    color: playerColor,
                                }
                            );
                            capitalText.setOrigin(0, 1);  // Align to bottom-left
                    
                            const capitalNumber = this.add.text(
                                capitalText.x + capitalText.width,
                                y - 15,
                                `${capitalCount}`,
                                {
                                    fontFamily: "Arial",
                                    fontSize: "23px",
                                    color: '#000000', // Black color for the number
                                }
                            );
                            capitalNumber.setOrigin(0, 1);

                            this.capitalTexts.push(capitalText, capitalNumber);
                        }

                    });
                };

                if (JSON.stringify(this.lastCounts) !== JSON.stringify(new_data["counts"])) {
                    this.lastCounts = {...new_data["counts"]};
                    updateDisplays();
                }

                if ("full_player_capitals" in new_data["board"] &&
                    JSON.stringify(this.full_capitals) !== JSON.stringify(new_data["board"]["full_player_capitals"])) {
                    this.full_capitals = new_data["board"]["full_player_capitals"];
                    updateDisplays();
                }

                if ("extra_info" in new_data) {
                    new_data["extra_info"].forEach((tuple) => {
                        this.parse_extra_info(tuple);
                    });
                }


                this.parse(this.nodes, new_data["board"]["nodes"], new_data["isRefresh"], true);
                this.parse(this.edges, new_data["board"]["edges"], new_data["isRefresh"]);
                this.parse(this.abilityManager.abilities, new_data["player"]["abilities"], false);
                Object.values(this.edges).forEach((edge) => edge.draw());
            } else {
            }
        }
    }

    private parse_extra_info(tuple) {
        if (tuple[0] === "cannon_shot") {
            let cannon = this.nodes[tuple[1][0]] as Node;
            let target = this.nodes[tuple[1][1]] as Node;
            if (tuple[1].length > 3) {
                this.cannonShot(cannon, target, tuple[1][2], tuple[1][3]);
            } else {
                this.cannonShot(cannon, target, tuple[1][2], tuple[1][2]);
            }
        } else if (tuple[0] == "player_elimination") {
            let player1 = tuple[1][0];
            let player2 = tuple[1][1];

            let eliminationText;

            if (player2 == this.mainPlayer.name && this.otherPlayers.length > 2) {
                eliminationText = this.add.text(
                    this.sys.game.config.width as number / 2,
                    20,
                    `3 credit reward for killing player ${player1}`,
                    { fontFamily: 'Arial', fontSize: '32px', color: '#000000' }
                );
            } else {
                eliminationText = this.add.text(
                    this.sys.game.config.width as number / 2,
                    20,
                    `player ${player2} killed player ${player1}`,
                    { fontFamily: 'Arial', fontSize: '32px', color: '#000000' }
                );
            }

            eliminationText.setOrigin(0.5);

            //Make the text fade out after a few seconds
            this.tweens.add({
                targets: eliminationText,
                alpha: 0,

                duration: 8000,
                ease: 'Power2',
                onComplete: () => {
                    eliminationText.destroy();
                },
            });
        } else if (tuple[0] == "timed_out") {
            let player1 = tuple[1][0];

            let eliminationText = this.add.text(
                (this.sys.game.config.width as number) / 2,
                (this.sys.game.config.height as number) / 2,
                `${player1} timed out`,
                { fontFamily: "Arial", fontSize: "32px", color: "#FF0000" }
            );

            eliminationText.setOrigin(0.5);

            //Make the text fade out after a few seconds
            this.tweens.add({
                targets: eliminationText,
                alpha: 0,
                duration: 6000,
                ease: "Power2",
                onComplete: () => {
                    eliminationText.destroy();
                },
            });
        } else if (tuple[0] == "Aborted") {
            let eliminationText = this.add.text(
                (this.sys.game.config.width as number) / 2,
                (this.sys.game.config.height as number) / 2,
                `Game Aborted due to neither player picking start node`,
                { fontFamily: "Arial", fontSize: "32px", color: "#FF0000" }
            );

            eliminationText.setOrigin(0.5);

            //Make the text fade out after a few seconds
            this.tweens.add({
                targets: eliminationText,
                alpha: 0,
                duration: 6000,
                ease: "Power2",
                onComplete: () => {
                    eliminationText.destroy();
                },
            });
            
        } else if (tuple[0] == "End Game") {
            let bonus = tuple[1] as number;
            let text = this.settings.ability_type == "credits" ? `Overtime - Free Attack - ${bonus} credits available` : `Overtime - Free Attack`;
            let bonusText = this.add.text(
                this.sys.game.config.width as number / 2,
                60,
                text,
                { fontFamily: 'Arial', fontSize: '32px', color: '#000000' }
            );

            bonusText.setOrigin(0.5);

            this.tweens.add({
                targets: bonusText,
                alpha: 0,
                duration: 6000,
                ease: "Power2",
                onComplete: () => {
                    bonusText.destroy();
                },
            });
        } else if (tuple[0] == "Walls Down") {
            let text = "Walls Down";
            let bonusText = this.add.text(
                this.sys.game.config.width as number / 2,
                40,
                text,
                { fontFamily: 'Arial', fontSize: '32px', color: '#000000' }
            );

            bonusText.setOrigin(0.5);

            this.tweens.add({
                targets: bonusText,
                alpha: 0,
                duration: 6000,
                ease: "Power2",
                onComplete: () => {
                    bonusText.destroy();
                },
            });
        }
    }

    private cannonShot(cannon: Node, target: Node, size: number, end_size: number) {
        cannonAngle(cannon, target.pos.x, target.pos.y);
        target.delayChange = true;

        let ball_size = 10 + Math.max(Math.log10(size / 10) / 2 + size / 1000 + 0.15, 0) * 24;

        // Create a Graphics object for the projectile
        const projectile = this.add.graphics();

        // Calculate the angle between cannon and target
        const angle = Phaser.Math.Angle.Between(
            cannon.pos.x,
            cannon.pos.y,
            target.pos.x,
            target.pos.y
        );

        // Draw the diamond-shaped projectile
        projectile.fillStyle(cannon.phaserColor, 1);
        projectile.beginPath();
        projectile.moveTo(0, -ball_size); // Top point
        projectile.lineTo(ball_size * 0.6, 0); // Right point
        projectile.lineTo(0, ball_size); // Bottom point
        projectile.lineTo(-ball_size * 0.6, 0); // Left point
        projectile.closePath();
        projectile.fillPath();

        // Rotate the projectile to point in the direction of travel
        projectile.rotation = angle + Math.PI / 2; // Add PI/2 because the default orientation is upward

        // Set the initial position to the cannon's position
        projectile.setPosition(cannon.pos.x, cannon.pos.y);

        // Calculate the distance between cannon and target
        const distance = Phaser.Math.Distance.Between(
            cannon.pos.x,
            cannon.pos.y,
            target.pos.x,
            target.pos.y
        );

        // Create a tween to move the projectile
        this.tweens.add({
            targets: projectile,
            scaleX: end_size / size,
            scaleY: end_size / size,
            x: target.pos.x,
            y: target.pos.y,
            duration: distance * 2, // Adjust this multiplier to change the speed
            ease: "Linear",
            onComplete: () => {
                // Destroy the projectile when it reaches the target
                projectile.destroy();
                target.endDelay();
            },
        });
    }

    private rgbToHex(color: readonly [number, number, number]): string {
        return (
            "#" +
            color
                .map((x) => {
                    const hex = x.toString(16);
                    return hex.length === 1 ? "0" + hex : hex;
                })
                .join("")
        );
    }

    parse(this, items, updates, refresh, redraw=false) {

        if (refresh === true) {
            Object.keys(items).forEach(key => {
                if (!updates.hasOwnProperty(key)) {
                    items[key].delete();
                    delete items[key];
                }
            });
        }

        for (const u in updates) {
            if (!items.hasOwnProperty(u)) {
                let new_edge = new Edge(
                    Number(u),
                    this.nodes[updates[u]["from_node"]],
                    this.nodes[updates[u]["to_node"]],
                    updates[u]["dynamic"],
                    this
                );
                this.edges[Number(u)] = new_edge;
            }

            if (updates[u] === "Deleted") {
                items[u].delete();
                delete items[u];
                continue;
            }

            let obj = items[u];
            if (typeof obj !== "object" || obj === null) {
                console.error(`Invalid item at key ${u}; expected an object.`);
                continue;
            }

            for (const [key, val] of Object.entries(updates[u])) {
                if (typeof obj[key] === "undefined") {
                    continue;
                }

                let updateVal;
                try {
                    updateVal = this.getObject(obj, key, val);
                } catch (error) {
                    console.error();
                    continue;
                }
                obj[key] = updateVal;
            }
            if (redraw) {
                obj.draw();
            }
        }
    }

    getObject(object, attribute, value) {
        if (object[attribute] instanceof Node) {
            return this.nodes[value];
        } else if (object[attribute] instanceof Edge) {
            return this.edges[value];
        } else if (attribute === "owner") {
            return this.otherPlayers[value] || null;
        } else if (attribute === "state") {
            return stateDict[value](this.settings.full_size);
        } else if (attribute === "effects") {
            return new Set(value);
        } else {
            return value;
        }
    }

    darken(color: readonly [number, number, number]): readonly [number, number, number] {
        return[Math.round(color[0] * 0.4), Math.round(color[1] * 0.4), Math.round(color[2] * 0.4)];
    }

    displayNames(namesList) {
        
        namesList.forEach((name: string, index: number) => {
            let position = positions[index];
            const playerColor = this.rgbToHex(this.darken(PlayerColors[index]));
                
            let x = (position.xPercent / 100) * (this.sys.game.config.width as number);
            let y = (position.yPercent / 100) * (this.sys.game.config.height as number);
            this.add.text(
                x, 
                y, 
                name, 
                {
                    fontSize: '16px',
                    color: playerColor,  // Changed from 'fill' to 'color'
                }
            ).setOrigin(0, 1);
        });
    }
}

