import { IDItem } from "./GameObjects";

export type ValidationFunction = (data: IDItem[]) => boolean;
export type Point = [number, number];