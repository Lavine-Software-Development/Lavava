export function random_equal_distributed_angles(count: number): number[] {
    const ports: number[] = [Math.random() * Math.PI];
    for (let i = 1; i < count; i++) {
        ports.push(ports[0] + Math.PI * i * 2 / count);
    }
    return ports;
}
