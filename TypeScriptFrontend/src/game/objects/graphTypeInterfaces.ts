export interface IEdge {
    from_node: INode,
    to_node: INode,
    on: boolean,
    recolor: boolean,
    dynamic: boolean,
}

export interface INode {
    edges: IEdge[]
    owner: any;
}