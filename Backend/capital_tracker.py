class CapitalTracker:
    def __init__(self):
        self.tracked_id_states = dict()
        self.capital_owners = dict()

    def node(self, node):
        if node.id in self.tracked_id_states:
            if node.state_name == 'capital':
                self.update(node)               
            else:
                self.remove(node)
                print("None capital node is removed")
        else:
            if node.state_name == 'capital':
                self.add(node)
                
    def remove(self, node):
        del self.tracked_id_states[node.id]
        self.capital_owners[node.id].capital_handover(False)
        del self.capital_owners[node.id]

    def add(self, node):
        self.tracked_id_states[node.id] = node.state_name
        self.capital_owners[node.id] = node.owner

    def update(self, node):
        if self.capital_owners[node.id]:
            self.capital_owners[node.id].capital_handover(False)
        if node.owner:
            node.owner.capital_handover(True)
        self.capital_owners[node.id] = node.owner

    def reset(self):
        self.tracked_id_states.clear()
        self.capital_owners.clear()

