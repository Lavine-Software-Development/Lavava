using UnityEngine;
using System.Collections.Generic;

public class Edge
{
    public Node ToNode { get; private set; }
    public Node FromNode { get; private set; }
    public int Id { get; private set; }
    public bool On { get; set; }
    public bool Flowing { get; set; }
    public bool Owned { get; set; }
    public bool Contested { get; set; }
    public bool Popped { get; set; }

    private const int MINIMUM_TRANSFER_VALUE = 1; // Replace with your constant
    private const int BEGIN_TRANSFER_VALUE = 2; // Replace with your constant
    private const int TRANSFER_RATE = 1; // Replace with your constant

    public Edge(Node toNode, Node fromNode, int id)
    {
        ToNode = toNode;
        FromNode = fromNode;
        Id = id;
        On = false;
        Flowing = false;
        Owned = false;
        Contested = false;
        Popped = false;
        UpdateNodes();
    }

    public void UpdateNodes()
    {
        ToNode.Incoming.Add(this);
        FromNode.Outgoing.Add(this);
    }

    public void Click(Player clicker, int button)
    {
        if (button == 1 && OwnedBy(clicker))
        {
            Switch();
        }
    }

    public void Switch(bool? specified = null)
    {
        On = specified ?? !On;
    }

    public void Update()
    {
        if (FromNode.Value < MINIMUM_TRANSFER_VALUE || !On || (ToNode.Full && !Contested))
        {
            Flowing = false;
        }
        else if (FromNode.Value > BEGIN_TRANSFER_VALUE)
        {
            Flowing = true;
        }

        if (Flowing)
        {
            Flow();
            if (!Popped)
            {
                Pop();
            }
        }
    }

    public void Pop()
    {
        Popped = true;
        if (!Contested || !FromNode.Owner.AutoAttack)
        {
            On = false;
        }
    }

    public void Flow()
    {
        int amountTransferred = TRANSFER_RATE * FromNode.Value;
        Delivery(amountTransferred);
        FromNode.Value -= amountTransferred;
    }

    public void Delivery(int amount)
    {
        if (ToNode.Owner != FromNode.Owner)
        {
            ToNode.Value -= amount;
            if (ToNode.Killed())
            {
                Capture();
            }
        }
        else
        {
            if (ToNode.Owner == null)
            {
                Capture();
            }
            ToNode.Value += amount;
        }
    }

    public void Capture()
    {
        ToNode.Capture(FromNode.Owner);
    }

    public void CheckStatus()
    {
        Owned = false;
        Contested = false;
        if (ToNode.Owner == null || FromNode.Owner == null)
        {
            return;
        }
        else if (ToNode.Owner == FromNode.Owner)
        {
            Owned = true;
        }
        else
        {
            Contested = true;
        }
    }

    public bool OwnedBy(Player player)
    {
        return FromNode.Owner == player;
    }

    public Color EdgeColor
    {
        get
        {
            if (On)
            {
                return FromNode.NodeColor;
            }
            return new Color(0.2f, 0.2f, 0.2f); // Equivalent to (50, 50, 50)
        }
    }
}
