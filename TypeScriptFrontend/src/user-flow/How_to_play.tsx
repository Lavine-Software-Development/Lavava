import "../../styles/style.css";
import React from "react";
import { Link } from 'react-router-dom';

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
                and so rather than countries there are dots, and instead of
                borders between countries (determining who can attack who),
                there are lines connecting dots. The real-time aspect is
                distinctly demonstrated in two ways. Firstly, rather than
                placing your troops at the beginning of each turn in select
                territories (as you would in Risk), each territory you own
                naturally grows at a constant rate, without any action. The
                game-term for this naturally growing resource is energy, shown
                visually through each dots' size. Secondly, attacking and
                energy reallocation happen in real time all
                over the map: Each line is directional, and can be turned on or
                off (this state being determined by the owner of the
                "from-dot"). A flowing line connecting two teammate dots
                ("teammate dots" as in that they are the same color (have the
                same owner)) will transfer energy from one dot to the other in
                the direction the line points. A flowing line connecting two
                opposing dots will remove energy at an equal rate from both
                dots. If the attacked dot (the dot the line points toward)
                loses all its energy before the atacking ndoe, then ownership of
                the attacked dot transfers to the attacker (it takes on the
                attacking dots color). This mechanic is identical to Risk.
                Dots continue growing and energy continually transfers along
                lines throughout the game until only one player still having
                dots of their color remains... or until someone wins by another method....
            </div>
            <div className="space">
                The main other twist is abilities! Each player is given 20
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
                        Start Selection (Upto 60 seconds): Each player chooses any unowned node. 
                        As soon as every player has chosen, the second phase begins.
                    </li>
                    <li>
                        Main Play (Upto 300 seconds (5 minutes)): Abilities are now usable!  
                        Try to spread out, take over the board, and claim capitals! 
                    </li>
                    <li>
                        Overtime (Upto 60 seconds): Attacking now comes at no cost. Watch as your 
                        opponents node shrinks, and yours does not. The goal of this change is to stop
                        progression, and allow the current winner to snowball.
                    </li>
                </ul>
            </div>
            <div className="space">
                <h3>Winning the Game</h3>
            </div>
            <div className="space">
                When a player has no remaining nodes on the map, they are eliminated. Once only one 
                remaining player has nodes on the map, they have a win by domination. In this case, 
                the other players ranks are determiined by their order of elimination.
            </div>
            <div className="space">
                However, players can also win by controlling 3 full capitals at once. In this case,
                the other players rank are determined by total node count. Be careful of this rule. If 
                you see another player is on the brink of a capital-win, your capitals will do nothing. 
                Instead, at this point just focus on controlling more of the map.
            </div>
            <div className="space">
                <h2>Structures</h2>
            </div>
            <div className="space">
            There are currently 3 kinds of structures: Capitals, Cannons, and Pumps.
             3 capitals start on the board, whereas the other two structures can only come
            from being placed by a player using an ability. Structures follow a set of rules:
            <ul>
                    <li>
                        Do not grow, unlike the rest of dots
                    </li>
                    <li>
                        When captured by an opponent, lose their structure. (The 3 starting capitals on the map are an exception to this rule)
                    </li>
                    <li>
                        Cannot be nuked.
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
                        60 dots and 80 lines.
                    </li>
                    <li>
                        dots can be full. At that point they no longer
                        naturally gain energy. This means you shouldn't let
                        dots be full unless neccessary.
                    </li>
                    <li>
                        Many of the lines are in fact dynamic (or two-way), meaning they can
                        change the direction they point in. When between
                        teammate dots, the owner can swap their direction. When
                        between opponent dots they automatically point in favor
                        of (away from) the larger dot. However if both dots
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
                        capabilties.
                    </li>
                    <li>
                        The main win condition requires removing all other
                        players from the map, but this can be tedious and so
                        they can forfeit at any point once they're confident
                        they've lost. However a secondary win condition exists
                        in owning 3 full capitals.
                    </li>
                    <li>
                        2/3 dots are randomly determined to be port-dots. Port-dots affect certain interactions with specific abilities.
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
                        Spawn: Choose an an unowned dot anywhere and claim it.
                        Identical to choosing a dot to start the game.
                    </li>
                    <li>
                        Mini-Bridge: Make a new two-way line between two port-dots so long as it doesn't overlap any other line. Does not Remove ports from dots its placed on. Has a limited range.
                    </li>
                    <li>
                        Freeze: Make a dynamic (two-way) line directional (one-way). Effectively
                        stops an opponent from attacking you through that line,
                        while still keeping it open for your use from the other
                        side. Can also flip a contested line in your advantage, so long as it is not flowing.
                    </li>
                    <li>
                        Burn: Make a port dot into a standard dot (remove its
                        ports). The burning effect can along flowing outward line to other port dots.
                        Used effectively, this can remove many ports.
                    </li>
                </ul>
                <h4>2 credits</h4>
                <ul>
                    <li>
                        Bridge: Make a new line between two *port-dots* so long as it doesn't overlap any other line. Bridge removes ports from dots its placed on.
                    </li>
                    <li>
                        Rage: All dots you own transfer energy at 3.5 times the
                        rate. Meant for a rush-esque play.
                    </li>
                    <li>
                        Capital: Turn any full dot you own into a capital. It then immediately shrinks entirely. Flow into them so can become *full*. Capitals act as a win condition, among all the other advantages of structures. Also, allow for using Nuke within the capitals range: determined by its size and a multiplier. Also, capitals cannot be placed directly beside eachother.
                    </li>
                </ul>
                <h4>3 credits</h4>
                <ul>
                    <li>
                        Nuke: Deletes a dot, and all its connecting lines from the map. To use Nuke, the dot selected must be within a certain perimeter outside a capital (starting or placed) the said player controls. You cannot Nuke structures.
                    </li>
                    <li>
                        Pump: Placed on any dot you own. Once full, a pump can be drained (clicked) and it then allows the player to replenish an ability of their choice. One can either get two more 1-credit abilities, or one singular 2-credit ability. You cannot replenish 3-credit+ abilities. Also, pumps take in 150% of the energy flowed into them, both from its owner, and by attackers.
                    </li>
                </ul>
                <h4>4 credits</h4>
                <ul>
                    <li>
                        Cannon: Placed on any port-dot you own. That dot can then shoot its energy to another dot so long as its shot path doesn't overlap any other line. Can be used to capture unclaimed dots, transfer energy to a teammate dot in need, or to attack a dot far away. 
                    </li>
                </ul>
            </div>
            <div className="space">
                <h1>FAQ</h1>
                Difference between lightly colored and darkly colored lines?
                Lightly colored just means it's on but can't flow for 1 of 2
                reasons:
                <ul>
                    <li>The from_dot is too small</li>
                    <li>
                        The to_dot is full (full dots have a black outer ring.
                        They cannot grow or intake energy) Clicking an line
                        turns it on or off. Flow can only happen when on
                    </li>
                </ul>
            </div>
            <div className="space">
                <h1>Got Ideas?</h1>
                <Link to="/team">Reach out</Link> pal I'd love to hear it. Still lots of ideas in
                progress.
            </div>
        </div>
    );
};

export default HowToPlay;
