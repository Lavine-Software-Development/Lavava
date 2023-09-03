using System.Collections.Generic;
using UnityEngine;

public class Board
{
    public List<Node> Nodes { get; private set; }
    public List<Edge> Edges { get; private set; }
    public Dictionary<int, Node> IdDict { get; private set; }
    public Dictionary<int, Player> PlayerDict { get; private set; }
    public int ExtraEdges { get; private set; }

    private const int SCREEN_WIDTH = 800; // Replace with your constant
    private const int NODE_COUNT = 100; // Replace with your constant
    private const int EDGE_COUNT = 200; // Replace with your constant

    public Board(int playerCount, List<Node> nodes, List<Edge> edges)
    {
        Nodes = nodes;
        Edges = edges;
        IdDict = new Dictionary<int, Node>();
        PlayerDict = new Dictionary<int, Player>();
        ExtraEdges = 2;

        Nodes = RemoveExcessNodes();

        foreach (var node in Nodes)
        {
            IdDict[node.Id] = node;
        }
        foreach (var edge in Edges)
        {
            IdDict[edge.Id] = edge;
        }

        for (int i = 0; i < playerCount; i++)
        {
            PlayerDict[i] = new Player(ColorDict[i], i); // Assuming ColorDict is defined
        }
    }

    public List<Node> RemoveExcessNodes()
    {
        return Nodes.FindAll(node => node.Incoming.Count + node.Outgoing.Count > 0);
    }

    public void Update()
    {
        foreach (var node in Nodes)
        {
            if (node.Owner != null)
            {
                node.Grow();
            }
        }
        foreach (var edge in Edges)
        {
            edge.Update();
        }
    }

    public int? FindNode(Vector2 position)
    {
        foreach (var node in Nodes)
        {
            if (Vector2.Distance(position, node.Pos) < Mathf.Pow(node.Size, 2))
            {
                return node.Id;
            }
        }
        return null;
    }

    public int? FindEdge(Vector2 position)
    {
        foreach (var edge in Edges)
        {
            if (DistancePointToSegment(position, edge.FromNode.Pos, edge.ToNode.Pos) < 5)
            {
                return edge.Id;
            }
        }
        return null;
    }

    public int? CheckNewEdge(int nodeFrom, int nodeTo)
    {
        if (nodeTo == nodeFrom)
        {
            return null;
        }

        HashSet<(int, int)> edgeSet = new HashSet<(int, int)>();
        foreach (var edge in Edges)
        {
            edgeSet.Add((edge.FromNode.Id, edge.ToNode.Id));
        }

        if (edgeSet.Contains((nodeTo, nodeFrom)) || edgeSet.Contains((nodeFrom, nodeTo)))
        {
            return null;
        }

        return NODE_COUNT + EDGE_COUNT + ExtraEdges + IdDict[nodeFrom].Owner.Id;
    }

    public void BuyNewEdge(int id, int nodeFrom, int nodeTo)
    {
        if (IdDict[nodeFrom].Owner == null)
        {
            Debug.LogError($"ERROR: node_from has no owner, NodeFrom ID: {nodeFrom}, NodeTo Pos: {IdDict[nodeTo].Pos}");
            return;
        }

        if (IdDict[nodeFrom].Owner.BuyEdge())
        {
            Edge newEdge = new Edge(IdDict[nodeTo], IdDict[nodeFrom], id);
            newEdge.CheckStatus();
            Edges.Add(newEdge);
            IdDict[id] = newEdge;
            ExtraEdges += 2;
        }
    }
}
