from player import DefaultPlayer
from constants import COLOR_DICT


class PlayerManager:
    def __init__(self, player_count, gs):
        self.gs = gs
        self.player_dict = {
            i: DefaultPlayer(COLOR_DICT[i], i) for i in range(player_count)
        }
        self.player_points = {i: 0 for i in range(player_count)}
        self.remaining = {i for i in range(player_count)}
        self.victor = None
        self.timer = 60

    def start_json(self):
        # for each player, return their id and color
        return {
                player: self.player_dict[player].color for player in self.player_dict
        }

    def reset(self):
        for player in self.player_dict.values():
            player.default_values()
        self.timer = 60
        self.victor = None
        self.remaining = {i for i in range(len(self.player_dict))}

    def update(self):
        for player in self.player_dict.values():
            if not player.eliminated:
                player.update()
                if player.count == 0:
                    self.eliminate(player.id)

    def eliminate(self, player):
        self.remaining.remove(player)
        self.player_dict[player].eliminate()

    def check_over(self):
        if len(self.remaining) == 1:
            self.win_and_end(self.player_dict[list(self.remaining)[0]])
        else:
            self.check_capital_win()

    def check_capital_win(self):
        winner = None
        for player in self.player_dict.values():
            if player.check_capital_win():
                winner = player
                break
        if winner:
            for player in self.remaining.copy():
                if player != winner.id:
                    self.eliminate(player)
            self.win_and_end(winner)

    def win_and_end(self, player):
        self.victor = player
        self.victor.win()
        self.display_ranks()

    def display_ranks(self):
        sorted_by_score = sorted(
            self.player_dict.values(), key=lambda p: p.points, reverse=True
        )
        print("New Scores")
        print("-----------------")
        for player in sorted_by_score:
            player.display()
        print()

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 0.1

            if self.timer > 3 and self.opening_moves == len(self.remaining):
                self.timer = 3
            return True

        self.gs.next()
        return False
    
    def chosen(self, player, data):
        self.player_dict[player].chosen(data)

    @property
    def opening_moves(self):
        return sum([player.count for player in self.player_dict.values()])
    

class SoloPlayerManager(PlayerManager):

    def __init__(self, gs):
        super().__init__(1, gs)

    def check_over(self):
        self.check_capital_win()
