# **Main Idea**

This game is a real-time variation of the classic board game Risk, with some other twists. It's built around graph theory, and so rather than countries there are nodes, and instead of borders between countries (determining who can attack who), there are edges connecting nodes. The real time aspect is distinctly demonstrated in two ways. Firstly, rather than placing your troops at the beginning of each turn in select territories (as you would in Risk), each territory you own naturally grows at a constant rate, without any action. The game-term for this naturally growing resource is *energy*, shown visually through each nodes' size. Secondly, attacking, and additionally the reallocating of energy happens in real time all over the map: Each edge is directional, and can be turned on or off (this state being determined by the owner of the "from-node"). A turned on edge connecting two teammate nodes ("teammate nodes" as in that they are the same color (have the same owner)) will transfer energy from one node to the other in the direction it points. A turned on edge connecting two opposing nodes will remove energy at an equal rate from both nodes. If the attacked node (the node the edge points toward) loses all its energy before the attacking node, then ownership of the attacked node transfers to the attacker (it takes on the attacking nodes color. This mechanic is identical to Risk). Nodes continue growing and energy continually transfers along edges throughout the game until only one player still having nodes of their color remains.  
The main other twist is abilities\! Each player can select a set of up to 5 abilities from the ability menu. Each ability has a cost, in elixir, a secondary and fundamentally separate resource from energy. Elixir naturally generates every 3 seconds, with a cap of 12 elixir per player. Using an ability reduces your elixir count by its cost. Other than their cost, there is no limit on ability usage in the game. Each ability can be used as many times as you like as long as you have the elixir.

# **Phases and Ending**

# The game is broken up into 3 main phases. First, start selection. 60 seconds is allotted so that each player chooses one starting spot, during which nothing else can be done besides picking starting spots. Then there is the main game, lasting 7 minutes, during which the standard rules apply. 5 minutes into standard time, all the gray walls go down, allowing for freer attack. If no one has one by the end of the 7 minutes, the 1 minutes overtime phase begins. The overtime phase is still being experimented with but currently two things happen:

* Free attacking. Attacking an opponents node costs you no energy The goal of these changes is too stop progression, and allow the current winner to snowball.   
* Elixir growth stops. This limits both offense and defensive plays. It forces you to be strategic with your last couple ability usages.

If still no player has won after the timer for overtime phase completes, then the winner is determined by which player owns the most nodes, and ranking follows that order.

# **Other tidbits of information**

* The board is randomly generated, and has approximately 60 nodes and 80 edges.  
* The purpose of walls is to limit bridge creation. It has nothing to do with energy flow/transferring/attacking.  
* The color of objects associates to the player using them (with exceptions to certain color affecting abilities)  
  * So blue edges are stemming from and thus controllable by the blue player etc (Note that uncolored items, like black turned-off edges, may still be owned and controllable)  
* Nodes can be *full*. At this point they no longer naturally gain energy. This means you shouldn't let nodes be full unless necessary.  
* Many of the edges are in fact dynamic, meaning they can change the direction they point in. When between teammate nodes, the owner can swap their direction. When between opponent nodes they automatically point in favor of (away from) the larger node. However if both nodes are full, both players can turn it on and it will swap in their favor.  
* There are 3 different colors for currently unowned nodes. Black nodes become black walls, gray nodes become gray walls, and brown nodes do not have walls.  
* Edges can be in three states, each with a different visual cue  
  * Off: Hollow and Black  
  * On, not Flowing: Hollow and lightly colored (of the from\_node color). This occurs for 1 of 2 reasons:  
    * The from\_node is too small  
    * The to\_node is full (full nodes have a black outer ring. They cannot grow or intake energy) Clicking an edge turns it on or off. Flow can only happen when on  
  * On, Flowing: Filled and darkly colored (of the from\_node)

# **Terminology**

* Attacking: Energy flowing from your node into an opponents node  
* Transferring: Energy flowing from your node into another node of yours  
  * Whether attacking or transferring is determined by the ownership of the receiving node. But the action of sending flow is the same for the owner of the from\_node regardless of attacking or transferring. It also looks identical along the edge.  
* Flow: Energy going from one node to another along an edge/bridge  
* Energy: The stuff that grows over time on a node. Each players energy displays as that players color.  
* Ownership: When a node has your colored energy on it, you OWN that node. You can control the flow of edges stemming from a node you own.

**Ability Catalogue**   
Bridge allows you to bridge to another node. You can only bridge to unwalled nodes. Bridge is uni-directional. Bridges cannot cross other existing bridges.

D-Bridge, like bridge, can connect to other unwalled nodes as long as it doesn't overlap existing bridges. However, it creates a bi-directional connection, working identically to already existing d-bridges on the map. Be careful with this, if you D-bridge to a larger opponents node the 

Wall lets you create a gray wall on an unwalled node of yours. This will stop opponents from bridging to it. However note that it will come down at the 5 minute, walls down mark. Remember walls do not affect flow. Walls affect 

Nuke allows you to remove a node (and all the bridges attached to it)l, as long as it's a neighbor to your node AND isn't currently attacking you.

Poisoned nodes temporarily shrink rather than growing. The poison will spread with, and backwards through, currently flowing bridges. It can also spread between different players. Placement rules for poison are identical to Nuke, on a neighboring node so long as it isn’t currently attacking (flowing into) you. Poison lasts for a limited time from its initial placement. Afterwards all poisoned nodes immediately lose the effect.

Cannon is placed on any node the player owns. Afterwards it can choose a target node, and shoot energy to it, so long as the path does not cross over any bridges. The cannon is a reusable ability. Once it is placed, it is then separately shot from, and this repeated secondary action costs no elixir. Cannon also has a synergy with other attack-esque abilities, currently including nuke and poison. By selecting your placed cannon, then one of those aforementioned abilities, and then a target, you can use that ability on any node the cannon can shoot, rather than using the cannon to send energy.

Over grow affects all of your nodes at once. For a limited time they lose their growth cap, and can expand to any size.

Rage affects all your edges at once. For a limited time they flow at 3 times the rate. When a new node is captured during rage, its raging timer for all edges extending from it is reset. In other words this means that while the length of a rage is limited, it can extend far beyond that time if you effectively capture more nodes, and slowly progress through the map.

|  | Cost | Type (Purpose) | Sub-Type | Placement |
| :---- | :---- | :---- | :---- | :---- |
| **Wall** | 2 | Defense | Single\-Buff | Node |
| **Over-Grow** | 2 | Powerup | Group\-Buff |  — |
| **Freeze** | 3 | Defense | Single\-Strike | Edge |
| **D-Bridge** | 3 | Expansion | Bridge | Node \-\> Node |
| **Poison** | 4  | Attack | Single\-Strike | Node |
| **Bridge** | 5 | Expansion | Bridge | Node \-\> Node |
| **Rage** | 5 | Powerup | Group\-Buff | — |
| **Cannon** | 6 | Expansion | Structure | Node |
| **Nuke** | 7 | Attack / Defense | Single\-Strike | Node |
|  |  |  |  |  |
|  |  |  |  |  |

