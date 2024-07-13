import { NameToCode } from "./constants";

export function random_equal_distributed_angles(count: number): number[] {
    const ports: number[] = [Math.random() * 360];
    for (let i = 1; i < count; i++) {
        ports.push(ports[0] + i * 360 / count);
    }
    return ports;
}

export function cannonAngle(node, x, y) {
    let dx = x - node.pos.x;
    let dy = y - node.pos.y;
    node.state.angle = Math.atan2(dy, dx) * (180 / Math.PI); // Angle in degrees
}

export function phaserColor(color: readonly [number, number, number]): number {
    return Phaser.Display.Color.GetColor(color[0], color[1], color[2]);
}

export function abilityCountsConversion(abilitiesFromStorage: any): { [x: string]: number } {
    return abilitiesFromStorage.reduce(
        (
            acc: { [x: string]: any },
            ability: { name: string; count: number }
        ) => {
            const code = NameToCode[ability.name];
            if (code) {
                acc[code] = ability.count;
            }
            return acc;
        },
        {}
    );
}

