from node import Node 
from edge import Edge

nodes = []
captured = []

def clicked():
    pass

while True:
    for cap in captured:
        cap.grow()

    if capture := clicked():
        captured.append(capture)


# This is a demonstration of clicking. First node can be selected, others only work if they're neighbor has
# been selected. \/
player = Player(BLUE)
owned = []

for spot in nodes:
    if spot.click(player):
        owned.append(spot)

print(len(owned))


        # p.draw.circle(screen, BLACK, (position[0],position[1]), 20, 0)
for spot in owned:
    spot.grow()