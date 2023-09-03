using UnityEngine;
using System.Collections.Generic;

public class DynamicEdge : Edge
{
    public DynamicEdge(Node node1, Node node2, int id) : base(node1, node2, id)
    {
    }

    public override void UpdateNodes()
    {
        base.UpdateNodes();
        ToNode.Incoming.Add(this);
        FromNode.Outgoing.Add(this);
    }

    public void SwapDirection()
    {
        Node temp = ToNode;
        ToNode = FromNode;
        FromNode = temp;
    }

    public override void Click(Player clicker, int button)
    {
        base.Click(clicker, button);
        if (button == 3)
        {
            if (!Contested && OwnedBy(clicker))
            {
                SwapDirection();
            }
        }
    }

    public override void CheckStatus()
    {
        Owned = false;
        Contested = false;
        if (ToNode.Owner == null || FromNode.Owner == null)
        {
            if (FromNode.Owner == null)
            {
                SwapDirection();
            }
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

    public override void Update()
    {
        base.Update();
        if (Contested)
        {
            if (ToNode.Value > FromNode.Value)
            {
                SwapDirection();
            }
        }
    }
}
