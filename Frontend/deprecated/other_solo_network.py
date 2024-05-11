class SoloNetwork:
    def __init__(self, setup, update, data):
        self.setup_callback = setup
        self.update_callback = update

        self.running = True
        self.data = data

        self.get_user_input_and_board()

    def get_user_input_and_board(self):
        while self.running:
            self.get_user_input_for_game()
            if self.receive_board():
                threading.Thread(target=self.listen).start()
                break

    # def get_user_input_for_game(self):
    #     self.game_type = int(self.data[0])

    # def receive_board(self):
    #     self.board_generator_value = int(random.randint(0, 10000))
    #     return True

    # def send(self, data):
    #     self.action_callback(*data[:2], data[2:])

    # def listen(self):
    #     time.sleep(1)
    #     while self.running:
    #         self.action_callback(0, 0, 0)
    #         time.sleep(0.1)
