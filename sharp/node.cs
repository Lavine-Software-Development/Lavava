using System;
using System.Collections.Generic;

public class Node
{
    private const double GROWTH_RATE = 0.1;
    private const double TRANSFER_RATE = 0.02;
    private static readonly Tuple<int, int, int> BLACK = new Tuple<int, int, int>(0, 0, 0);

    public int Value { get; private set; }
    public object Owner { get; private set; } // Assuming owner is an object. Adjust type accordingly.
    private object Clicker { get; set; }
    public bool Pressed { get; private set; }
    public double ThreatenScore { get; private set; }
    public List<object> Incoming { get; } = new List<object>(); // Assuming edge is an object. Adjust type accordingly.
    public List<object> Outgoing { get; } = new List<object>(); // Assuming edge is an object. Adjust type accordingly.
    public int Id { get; }
    public object Pos { get; } // Assuming pos is an object. Adjust type accordingly.
    public bool Hovered { get; private set; }

    public Node(int id, object pos) // Assuming pos is an object. Adjust type accordingly.
    {
        Id = id;
        Pos = pos;
    }

    public override string ToString()
    {
        return Id.ToString();
    }

    public void Grow()
    {
        Value += (int)(GROWTH_RATE);
        // Assuming owner has a score property. Adjust accordingly.
        Owner.Score += (int)(GROWTH_RATE); 
    }

    public Tuple<bool, bool> Click(object clicker, bool press)
    {
        Clicker = clicker;
        if (Owner == null)
        {
            if (!Expand())
            {
                Console.WriteLine("buying clicker");
                return new Tuple<bool, bool>(Clicker.BuyNode(this), false); // Assuming BuyNode method exists in Clicker.
            }
            return new Tuple<bool, bool>(true, false);
        }
        else if (Owner == Clicker)
        {
            Pressed = press;
            return new Tuple<bool, bool>(true, true);
        }
        else if (Owner != Clicker)
        {
            return new Tuple<bool, bool>(Capture(), false);
        }
        return new Tuple<bool, bool>(false, false);
    }

        public void Absorb()
    {
        foreach (var edge in Incoming)
        {
            // Assuming edge has properties 'Owned' and 'Flowing'
            if (edge.Owned && edge.Flowing)
            {
                Share(edge);
            }
        }
    }

    public void Expel()
    {
        double transferAmount = Value * TRANSFER_RATE * -1;
        foreach (var edge in Outgoing)
        {
            if (edge.Owned && edge.Flowing)
            {
                Transfer(Neighbor(edge), transferAmount);
            }
        }
    }

    private object Neighbor(object edge)
    {
        // Assuming edge has a method or property 'OpposingNodes'
        return edge.OpposingNodes[Id];
    }

    public bool Expand()
    {
        bool success = false;
        foreach (var edge in Incoming)
        {
            if (Neighbor(edge).Owner == Clicker)
            {
                edge.Owned = true;
                success = true;
                Share(edge);
            }
        }

        if (success)
        {
            Own();
        }

        return success;
    }

    private void Own()
    {
        Owner = Clicker;
        CheckEdgeStati();
    }

    private void CheckEdgeStati()
    {
        foreach (var edge in Incoming)
        {
            // Assuming edge has a method 'CheckStatus'
            edge.CheckStatus();
        }
        foreach (var edge in Outgoing)
        {
            edge.CheckStatus();
        }
    }

    public bool Capture()
    {
        if (Threatened)
        {
            AttackLoss();
            Own();
            Value = 1;
            return true;
        }
        return false;
    }

    private void AttackLoss()
    {
        double threatenedDifference = 1 - Value / ThreatenScore;
        foreach (var edge in Incoming)
        {
            // Assuming edge has properties 'Flowing' and 'Contested'
            if (edge.Flowing && edge.Contested)
            {
                Neighbor(edge).Value *= threatenedDifference; // Assuming Neighbor has a Value property
            }
        }
    }

    public void CalculateThreatenedScore()
    {
        double score = 0;
        foreach (var edge in Incoming)
        {
            if (edge.Flowing && edge.Contested)
            {
                score += Neighbor(edge).Value; // Assuming Neighbor has a Value property
            }
        }
        ThreatenScore = score;
    }

    private void Share(object edge)
    {
        var neighbor = Neighbor(edge);
        double transferAmount = neighbor.Value * TRANSFER_RATE; // Assuming Neighbor has a Value property
        Transfer(neighbor, transferAmount);
    }

    private void Transfer(object neighbor, double amount)
    {
        Value += (int)amount;
        neighbor.Value -= (int)amount; // Assuming Neighbor has a Value property
    }

    public void Hover(bool status)
    {
        Hovered = status;
    }


    public Tuple<int, int, int> Color
    {
        get
        {
            if (Owner != null)
            {
                if (Hovered)
                {
                    return new Tuple<int, int, int>(Owner.Color.Item1, 150, Owner.Color.Item3); // Assuming Owner has a Color property of type Tuple.
                }
                return Owner.Color; // Assuming Owner has a Color property of type Tuple.
            }
            return BLACK;
        }
    }

    public bool Threatened => ThreatenScore > Value;
}
