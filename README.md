# Lavava
Sup yall

# Main Idea
This game is a real-time variation of the classic board game Risk, with some other twists. It's built around graph theory, and so rather than countries there are nodes, and instead of borders between countries (determining who can attack who), there are edges connecting nodes. The real time aspect is distinctly demonstrated in two ways. Firstly, rather than placing your troops at the beginning of each turn in select territories (as you would in Risk), each territory you own naturally grows at a constant rate, without any action. The game-term for this naturally growing resource is *energy*, shown visually through each nodes' size. Secondly, attacking, and additionally the reallocating of energy happens in real time all over the map: Each edge is directional, and can be turned on or off (this state being determined by the owner of the "from-node"). A turned on edge connecting two teammate nodes ("teammate nodes" as in that they are the same color (have the same owner)) will transfer energy from one node to the other in the direction it points. A turned on edge connecting two opposing nodes will remove energy at an equal rate from both nodes. If the attacked node (the node the edge points toward) loses all its energy before the atacking ndoe, then ownership of the attacked node transfers to the attacker (it takes on the attacking nodes color. This mechanic is identical to Risk). Nodes continue growing and energy continually transfers along edges throughout the game until only one player still having nodes of their color remains.

The main other twist is abilities! Each player is given 20 credits at the beginning of the game to select a set of abilities from the ability menu. Each ability has a cost (in credits) as well as a reload time to limit immediate repeated usage in-game. At the bottom is a description of each ability.

# Phases and Ending
The game is broken up into 3 main phases. First, start selection. Each player chooses one starting spot. Then there is the main part, as described in detail above. If no one wins in that time, the end-game phase begins. The end-game phase is still being experimented with but currently two things happen: 
- Growth stops. Nodes naturally stay at their current energy.
- Free attacking. Attacking an opponents node costs you no energy
The goal of these changes is too stop progression, and allow the current winner to snowball. If still no player has won after the timer for end-game phase completes, then the winner is determined by which player owns the most nodes.

# Structures
There are currently 3 kinds of structures: Capitals, Cannons, and Pumps. 3 capitals start on the board, whereas the other two structures can only come from being placed by a player using an ability. Structures follow a set of rules:
- Do not grow, unlike the rest of nodes
- When captured by an opponent, lose their structure. (The 3 starting capitals on the map are an exception to this rule)
- Cannot be nuked.

# Other tidbits of information 
- The board is randomly generated, and has approximately 60 nodes and 80 edges.
- Nodes can be *full*. At this point they no longer naturally gain energy. This means you shouldn't let nodes be full unless neccessary.
- Many of the edges are in fact dynamic, meaning they can change the direction they point in. When between teammate nodes, the owner can swap their direction. When between opponent nodes they automatically point in favor of (away from) the larger node. However if both nodes are full, both players can turn it on and it will swap in their favor.
- Players start by choosing one random start point. Everything else comes from natural energy growth, transferring, and abilities.
- The map starts with 3 capital states, these can be captured and afford the owning player certain capabilties. Capitals are just one of multiple other 'states' nodes can be in (usually as a result of abilities, as explored further below)
- The main win condition requires removing all other players from the map, but this can be tedious and so they can forfeit at any point once they're confident they've lost. However a secondary win condition exists in owning 3 full capitals.
- Every other node is randomly determined to be a port-node. Port-nodes affect certain interactions with specific abilities.

# Ability Breakdown
1 Credit
- Spawn: Choose an an unowned node anywhere and claim it. Identical to choosing a node to start the game.
- Freeze: Make a dynamic-edge directional. Effectively stops an opponent from attacking you through that edge, while still keeping it open for your use from the other side. Will flip a contested as edge in your advantage, so long as it is not flowing.
- Burn: Make a port node into a standard node (remove its ports).
- Mini-Bridge: Make a new *two-way* edge between two *port-nodes* so long as it doesn't overlap any other edge. *Does not* Remove ports from nodes its placed on. Has a limited range.
- Zombie: Make a node you own into an unowned wall (Zombie State). It automatically is set to 200 energy, but all energy transferred into it is halved (affectively requires 400 energy to be recaptured by a player).

2 Credits
- Bridge: Make a new edge between two *port-nodes* so long as it doesn't overlap any other edge. Removes ports from nodes its placed on.
- Capital: Turn any full node you own into a capital. It then immediately shrinks entirely. Flow into them so can become *full*. Capitals act as a win condition, among all the other advantages of structures. Also, allow for using Nuke within the capitals range: determined by its size and a multiplier. Also, capitals cannot be placed directly beside eachother.
- Rage: All nodes you own transfer energy at 3.5 times the rate. Meant for a rush-esque play.
- Poison: Choose an edge directly extending from a node you own. A *poison* is then sent to the opposing node. That poison then recurisvely spreads along all edges that are on. A poisoned node shrinks (loses energy) at the rate a normal node grows. This happens for 20 seconds.

3 Credits
- Nuke: Deletes a node, and all its connecting edges from the map. To use Nuke, the node selected must be within a certain perimeter outside a capital (starting or placed) the said player controls. You cannot Nuke structures.
- Pump: Placed on any node you own. Once full, a pump can be drained (clicked) and it then allows the player to replenish an ability of their choice. One can either get two more 1-credit abilities, or one singular 2-credit ability. You cannot replenish 3-credit+ abilities. Also, pumps take in 150% of the energy flowed into them, both from its owner, and by attackers.

4 Credits
- Cannon: Placed on any port-node you own. That node can then shoot its energy to another node so long as its shot path doesn't overlap any other edge. Can be used to capture unclaimed nodes, transfer energy to a teammate node in need, or to attack a node far away. 

# FAQ

Difference between lightly colored and darkly colored edges?
Lightly colored just means it's on but can't flow for 1 of 2 reasons:
- The from_node is too small
- The to_node is full (full nodes have a black outer ring. They cannot grow or intake energy)
Clicking an edge turns it on or off. Flow can only happen when on

# Got ideas?
Reach out pal I'd love to hear it. Still lots of ideas in progess.


