import { Colors } from '../game/objects/constants';

export const abilityColors: { [key: string]: string } = {
    "Spawn": `rgb(${Colors.WHITE.slice().join(', ')})`,
    "Bridge": `rgb(${Colors.YELLOW.slice().join(', ')})`,
    "D-Bridge": `rgb(${Colors.YELLOW.slice().join(', ')})`,
    "Nuke": `rgb(${Colors.GREY.slice().join(', ')})`,
    "Poison": `rgb(${Colors.PURPLE.slice().join(', ')})`,
    "Freeze": `rgb(${Colors.LIGHT_BLUE.slice().join(', ')})`,
    "Capital": `rgb(${Colors.PINK.slice().join(', ')})`,
    "Zombie": `rgb(${Colors.DARK_GRAY.slice().join(', ')})`,
    "Burn": `rgb(${Colors.DARK_ORANGE.slice().join(', ')})`,
    "Rage": `rgb(${Colors.LIGHT_GREEN.slice().join(', ')})`,
    "Cannon": `rgb(${Colors.GREY.slice().join(', ')})`,
    "Pump": `rgb(${Colors.DARK_PURPLE.slice().join(', ')})`,
    "Mini-Bridge": `rgb(${Colors.YELLOW.slice().join(', ')})`,
    "Over-Grow": `rgb(${Colors.DARK_GREEN.slice().join(', ')})`,
    "Wall-Breaker": `rgb(${Colors.DARK_RED.slice().join(', ')})`,
    "Wormhole": `rgb(${Colors.DARK_PINK.slice().join(', ')})`,
};

export default abilityColors;