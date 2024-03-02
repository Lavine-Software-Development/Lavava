class Tracker:
    def __init__(self):
        self.tracked_id_states = dict()
        self.mines = set()
        self.capital_owners = dict()

    def node(self, node):
        if node.id in self.tracked_id_states:
            if node.state_name == self.tracked_id_states[node.id]:
                self.update(node)
            elif node.state_name == 'default':
                self.remove(node)
            else:
                print("Should Not Occur. Should only SWITCH states to default, not to other states.")
        else:
            self.add(node)

    def remove(self, node):
        del self.tracked_id_states[node.id]
        if node.state_name == 'capital':
            self.capital_owners[node.id].capital_handover(False)
            del self.capital_owners[node.id]
        elif node.state_name == 'mine':
            self.mines.discard(node.id)
            node.owner.change_tick(node.node_state.bonus)
        else:
            print("Should Not Occur. Should only REMOVE Capital or Mine in Tracker")

    def add(self, node):
        self.tracked_id_states[node.id] = node.state_name
        if node.state_name == 'capital':
            self.capital_owners[node.id] = node.owner
        elif node.state_name == 'mine':
            self.mines.add(node.id)
        else:
            print("Should Not Occur. Should only ADD Capital or Mine in Tracker")

    def update(self, node):
        if node.state_name == 'capital':
            self.capital_owners[node.id].capital_handover(False)
            node.owner.capital_handover(True)
            self.capital_owners[node.id] = node.owner
        else:
            print("Should Not Occur. Should only UPDATE Capital in Tracker")

