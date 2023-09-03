using UnityEngine;
using System.Collections.Generic;
using System;

public class Node
{
    public int Value { get; set; }
    public Player Owner { get; set; }
    public Player Clicker { get; set; }
    public List<Edge> Incoming { get; set; } // Assuming Edge is a class you have
    public List<Edge> Outgoing { get; set; } // Assuming Edge is a class you have
    public int Id { get; private set; }
    public Vector2 Pos { get; private set; }

    private const int GROWTH_RATE = 1; // Replace with your constant
    private const int GROWTH_STOP = 100; // Replace with your constant
    private static readonly Color BLACK = Color.black; // Replace with your constant

    public Node(int id, Vector2 pos)
    {
        Value = 0;
        Owner = null;
        Clicker = null;
        Incoming = new List<Edge>();
        Outgoing = new List<Edge>();
        Id = id;
        Pos = pos;
    }

    public override string ToString()
    {
        return Id.ToString();
    }

    public void Grow()
    {
        if (!Full)
        {
            Value += GROWTH_RATE;
            Owner.Money += GROWTH_RATE;
        }
    }

    public void Click(Player clicker, int button)
    {
        Clicker = clicker;
        if (button == 1)
        {
            LeftClick();
        }
    }

    public void LeftClick()
    {
        if (Owner == null)
        {
            if (Clicker.BuyNode())
            {
                Capture();
            }
        }
    }

    public void Expand()
    {
        foreach (var edge in Outgoing)
        {
            if (edge.Contested)
            {
                if (Owner.AutoAttack)
                {
                    edge.Switch(true);
                    edge.Popped = true;
                }
            }
            else if (!edge.Owned && Owner.AutoExpand)
            {
                edge.Switch(true);
                edge.Popped = false;
            }
        }
    }

    public void CheckEdgeStati()
    {
        foreach (var edge in Incoming)
        {
            edge.CheckStatus();
        }
        foreach (var edge in Outgoing)
        {
            edge.CheckStatus();
        }
    }

    public void Capture(Player clicker = null)
    {
        if (clicker == null)
        {
            clicker = Clicker;
        }
        Owner = clicker;
        clicker.Count += 1;
        CheckEdgeStati();
        Expand();
    }

    public bool Killed()
    {
        if (Value < 0)
        {
            Value *= -1;
            if (Owner != null)
            {
                Owner.Count -= 1;
            }
            return true;
        }
        return false;
    }

    public float SizeFactor()
    {
        if (Value < 5)
        {
            return 0;
        }
        return Math.Max(Mathf.Log10(Value / 10f) / 2f + Value / 1000f + 0.15f, 0);
    }

    public int Size
    {
        get { return (int)(5 + SizeFactor() * 18); }
    }

    public Color NodeColor
    {
        get
        {
            if (Owner != null)
            {
                return Owner.Color;
            }
            return BLACK;
        }
    }

    public bool Full
    {
        get { return Value >= GROWTH_STOP; }
    }
}
