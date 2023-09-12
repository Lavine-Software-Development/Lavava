# Lavava
Sup yall

# Setup
The game is for 2 to 4 players
Each player must pull main and install requirements.txt

Choose one player to run the server. This player needs to check the local ip address on their computer.
Go to the 'constants.py' file on each computer and change the 'NETWORK' value to the ip of the player running server

The player running server should run server.py
Each player should then run client.py. This must be after server.py is running

One player types HOST and chooses how many players should play, and they will be given a 6 digit code
The other players type JOIN, and then type in the code.

# Play
The goal is to be the only player with their colored nodes on the board
Click a node to start growing from there. This will cost you 300 money each time (Wallet show in the top left)
Note the edges pointing outwards from that node turn lightly of that color
Once the node grows big enough it'll "pop" and new nodes will stem from its outward growing edges

Click an edge pointing outwards from a node you own 
The edge will turn on, and the node will shrink, as the node on the opposing side grows. (You're transferring energy)
Two-way edges are denoted with circles connected to one green triangle
Right click two-way edges to swap their direction. (This can only be done in certain circumstances you'll pick up on)

Edge Building --- Costs 500 money
Tap 'A' on the keyboard (do not hold)
Click a node you want to start from (click the mouse, do not hold down) (must be a node you own)
Click any other node (you do not need to own it)
This will build an edge. Note edges cannot be built if they intersect other edges

# FAQ
How does attacking work?
Turn on an edge pointing into an opponents node. It'll make it shrink rather than grow.
If it gets small enough the colors will swap. Node captured!

The board is too small, or doesn't fit on my screen?
Change 'HEIGHT' and 'WIDTH' in 'constants'py'
This should be consistent for each player but may work even if not

What are the numbers at the top in the middle?
The total nodes each player has

How do I start a new game?
Every player but one should be killed (have no nodes) or forfeit (press 'X')
The remaining player presses 'R' and voila (may be glitchy)

Difference between lightly colored and darkly colored edges?
Lightly colored just means it's on but can't flow for 1 of 2 reasons:
- The from_node is too small
- The to_node is full (full nodes have a black outer ring. They cannot grow or intake energy)
Clicking an edge turns it on or off. Flow can only happen when on

Number below wallet?
Rate of wealth increase. Logarithmically related to total nodes a player owns
This will likely change as its too snowbally

Got ideas?
Reach out pal I'd love to hear it

