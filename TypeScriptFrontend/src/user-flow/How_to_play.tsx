import "../../styles/style.css";
import React from "react";

const HowToPlay: React.FC = () => {
    return (
        <div className="scrollable-container">
            <h1>How To Play</h1>
            <div className="space">
                <h2>Main Idea</h2>
            </div>
            <div className="space">
                This game is a real-time variation of the classic board game
                Risk, with some other twists. It's built around graph theory,
                and so rather than countries there are nodes, and instead of
                borders between countries (determining who can attack who),
                there are edges connecting nodes. The real time aspect is
                distinctly demonstrated in two ways. Firstly, rather than
                placing your troops at the beginning of each turn in select
                territories (as you would in Risk), each territory you own
                naturally grows at a constant rate, without any action. The
                game-term for this naturally growing resource is energy, shown
                visually through each nodes' size. Secondly, attacking, and
                additionally the reallocating of energy happens in real time all
                over the map: Each edge is directional, and can be turned on or
                off (this state being determined by the owner of the
                "from-node"). A turned on edge connecting two teammate nodes
                ("teammate nodes" as in that they are the same color (have the
                same owner)) will transfer energy from one node to the other in
                the direction it points. A turned on edge connecting two
                opposing nodes will remove energy at an equal rate from both
                nodes. If the attacked node (the node the edge points toward)
                loses all its energy before the atacking ndoe, then ownership of
                the attacked node transfers to the attacker (it takes on the
                attacking nodes color. This mechanic is identical to Risk).
                Nodes continue growing and energy continually transfers along
                edges throughout the game until only one player still having
                nodes of their color remains.
            </div>
            <div className="space">
                The main other twist is abilities! Each player is given 15
                credits at the beginning of the game to select a set of
                abilities from the ability menu. Each ability has a cost (in
                credits) as well as a reload time to limit immediate repeated
                usage in-game. At the bottom is a description of each ability.
            </div>
            <div className="space">
                <h2>Phases and Ending</h2>
            </div>
            <div className="space">
                The game is broken up into 3 main phases. First, start
                selection. Each player chooses one starting spot. Then there is
                the main part, as described in detail above. If no one wins in
                that time, the end-game phase begins. The end-game phase is
                still being experimented with but currently two things happen:
                <ul>
                    <li>
                        Growth stops. Nodes naturally stay at their current
                        energy.
                    </li>
                    <li>
                        Free attacking. Attacking an opponents node costs you no
                        energy The goal of these changes is too stop
                        progression, and allow the current winner to snowball.
                        If still no player has won after the timer for end-game
                        phase completes, then the winner is determined by which
                        player owns the most nodes.
                    </li>
                </ul>
            </div>
            <div className="space">
                <h2>Other Tidbits of Information</h2>
            </div>
            <div className="space">
                <ul>
                    <li>
                        The board is randomly generated, and has approximately
                        60 nodes and 80 edges.
                    </li>
                    <li>
                        Nodes can be full. At that point they no longer
                        naturally gain energy. This means you shouldn't let
                        nodes be full unless neccessary.
                    </li>
                    <li>
                        Many of the edges are in fact dynamic, meaning they can
                        change the direction they point in. When between
                        teammate nodes, the owner can swap their direction. When
                        between opponent nodes they automatically point in favor
                        of (away from) the larger node. However if both nodes
                        are full, both players can turn it on and it will swap
                        in their favor.
                    </li>
                    <li>
                        Players start by choosing one random start point.
                        Everything else comes from natural energy growth and
                        transferring, and abilities.
                    </li>
                    <li>
                        The map starts with 3 capital states, these can be
                        captured and afford the owning player certain
                        capabilties. Capitals are just one of multiple other
                        'states' nodes can be in (usually as a result of
                        abilities, as explored further below)
                    </li>
                    <li>
                        The main win condition requires removing all other
                        players from the map, but this can be tedious and so
                        they can forfeit at any point once they're confident
                        they've lost. However a secondary win condition exists
                        in owning 3 full capitals.
                    </li>
                    <li>
                        Every other node is randomly determined to be a
                        port-node. Port-nodes affect certain interactions with
                        specific abilities.
                    </li>
                </ul>
            </div>
            <div className="space">
                <h2>Ability Breakdown</h2>
            </div>
            <div className="space">
                <h4>1 credit</h4>
                <ul>
                    <li>
                        Spawn: Choose an an unowned node anywhere and claim it.
                        Identical to choosing a node to start the game.
                    </li>
                    <li>
                        Freeze: Make a dynamic-edge directional. Effectively
                        stops an opponent from attacking you through that edge,
                        while still keeping it open for your use from the other
                        side.
                    </li>
                    <li>
                        Burn: Make a port node into a standard node (remove its
                        ports).
                    </li>
                    <li>
                        Zombie: Make a node you own into an unowned wall (Zombie
                        State). It automatically is set to 200 energy, but all
                        energy transferred into it is halved (affectively
                        requires 400 energy to be recaptured by a player).
                    </li>
                </ul>
                <h4>2 credits</h4>
                <ul>
                    <li>
                        Bridge: The quintessential ability. Make a new edge
                        between two port-nodes so long as it doesn't overlap any
                        other edge.
                    </li>
                    <li>
                        D-Bridge: Just a dynamic edge. Has its pros and cons.
                    </li>
                    <li>
                        Rage: All nodes you own transfer energy at 2.5 times the
                        rate. Meant for a rush-esque play.
                    </li>
                    <li>
                        Poison: Choose an edge directly extending from a node
                        you own. A poison is then sent to the opposing node.
                        That poison then recurisvely spreads along all edges
                        that are on. A poisoned node shrinks (loses energy) at
                        the rate a normal node grows. This happens for 20
                        seconds.
                    </li>
                </ul>
                <h4>3 credits</h4>
                <ul>
                    <li>
                        Nuke: Deletes a node, and all its connecting edges from
                        the map. To use Nuke, the node selected must be within a
                        certain perimeter outside a capital the said player
                        controls.
                    </li>
                    <li>
                        Capital: Turn any full node you own into a capital. It
                        then immediately shrinks entirely, and then ceases to
                        grow naturally, instead relying on transferred in
                        energy. Capitals have a few usages. They cannot be
                        poisoned or nuked, enable using Nukes (as explained
                        above), be built to with a bridge, and most importantly
                        act as a win condition. If a capital is ever captured,
                        it returns to a normal node.
                    </li>
                    <li>
                        Cannon: Placed on any node you own. That node can then
                        shoot its energy anywhere onto the map. Can be used to
                        capture unclaimed nodes, transfer energy to a teammate
                        node in need, or to attack a node far away. If a cannon
                        is ever captured, unlike capital, the capturing player
                        now has access to the cannon.
                    </li>
                    <li>Pump: Placed on any node you own. Pump nodes stop naturally 
                        growing similar to capitals. Transferring into them is also 
                        halved, similar to Zombie. Once full, a pump can be drained 
                        (clicked) and it then allows the player to replenish an ability 
                        of their choice. One can either get two more 1-credit abilities, 
                        or one singular 2-credit ability. You cannot replenish 3-credit 
                        abilities.</li>
                </ul>
            </div>
            <div className="space">
                <h1>FAQ</h1>
                Difference between lightly colored and darkly colored edges?
                Lightly colored just means it's on but can't flow for 1 of 2
                reasons:
                <ul>
                    <li>The from_node is too small</li>
                    <li>
                        The to_node is full (full nodes have a black outer ring.
                        They cannot grow or intake energy) Clicking an edge
                        turns it on or off. Flow can only happen when on
                    </li>
                </ul>
            </div>
            <div className="space">
                <h1>Got Ideas?</h1>
                Reach out pal I'd love to hear it. Still lots of ideas in
                progess.
            </div>
        </div>
    );
};

export default HowToPlay;
