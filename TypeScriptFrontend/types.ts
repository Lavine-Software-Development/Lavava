import { IDItem } from "./Objects/idItem";

export type ValidationFunction = (data: IDItem[]) => boolean;
export type Point = [number, number];