export function random_equal_distributed_angles(count: number): number[] {
    const ports: number[] = [Math.random() * 360];
    for (let i = 1; i < count; i++) {
        ports.push(ports[0] + i * 360 / count);
    }
    return ports;
}
