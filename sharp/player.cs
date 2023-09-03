using UnityEngine;

public class Player
{
    public int Money { get; private set; }
    public int Count { get; set; }
    public bool Begun { get; set; }
    public Color Color { get; private set; }
    public int Id { get; private set; }
    public bool AutoExpand { get; set; }
    public bool AutoAttack { get; set; }
    public bool ConsideringEdge { get; private set; }
    public Node NewEdgeStart { get; set; } // Assuming Node is a class you have
    public Node HighlightedNode { get; set; } // Assuming Node is a class you have

    private const int START_MONEY = 1000; // Replace with your constant
    private const int BUY_NODE_COST = 100; // Replace with your constant
    private const int BUILD_EDGE_COST = 50; // Replace with your constant

    public Player(Color color, int id)
    {
        Money = START_MONEY;
        Count = 0;
        Begun = false;
        Color = color;
        Id = id;
        AutoExpand = true;
        AutoAttack = false;
        ConsideringEdge = false;
        NewEdgeStart = null;
        HighlightedNode = null;
    }

    public bool BuyNode()
    {
        if (Money >= BUY_NODE_COST)
        {
            Money -= BUY_NODE_COST;
            return true;
        }
        return false;
    }

    public bool BuyEdge()
    {
        if (Money >= BUILD_EDGE_COST)
        {
            Money -= BUILD_EDGE_COST;
            return true;
        }
        return false;
    }

    public void SwitchConsidering()
    {
        ConsideringEdge = !ConsideringEdge;
        if (Money < BUILD_EDGE_COST)
        {
            ConsideringEdge = false;
        }
        NewEdgeStart = null;
    }

    public bool NewEdgeStarted()
    {
        return NewEdgeStart != null;
    }
}