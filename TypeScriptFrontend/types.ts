import { IDItem } from "./idItem";

export type ValidationFunction = (data: IDItem[]) => boolean;
export type Point = [number, number];