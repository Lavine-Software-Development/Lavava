export interface IEdge {
    from_node: INode,
    on: boolean,
    recolor: boolean,
}

export interface INode {
    edges: IEdge[]
}