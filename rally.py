import random
from transitions import Machine, State


class Rally(object):
    states = ["serve", "end"]
    ball_action_states = ["fail", "bad","good", "perfect"]

    def __init__(self, serving_team, receiving_team):
        self.serving_team=serving_team
        self.receiving_team=receiving_team
        self.machine = Machine(model=self, states=Rally.states, initial="serve")
        self.machine.add_transition("ace", "serve", "end", after="server_wins")
        self.machine.add_transition("serve_fail", "serve", "end", after="receiver_wins")

    def play_rally(self):
      #  stronger = random.choices([self.serving_team, self.receiving_team], weights=[self.serving_team.sideout_efficiency, self.receiving_team.sideout_efficiency], k=1)[0]
       # print(f"skills: {self.receiving_team.skill_data['serve']}")
        serve_value = self.generate_ball_action_quality(self.receiving_team.skill_data['serve'])
        receive_value = self.generate_ball_action_quality(self.receiving_team.skill_data['receive'])
        print(f"Serve: {serve_value}, Receive: {receive_value}")
      # if stronger == self.serving_team:
        #    self.ace()
        return self.serving_team

    def generate_ball_action_quality(self, serve_weights):
        quality = random.choices(Rally.ball_action_states, weights=[serve_weights["fail"],serve_weights["bad"],serve_weights["good"],serve_weights["perfect"], ], k=1)[0]
        return quality

    def server_wins(self):
        return self.serving_team

    def receiver_wins(self):
        return self.receiving_team

    def ace(self):
        return self.serving_team

    def serve_fail(self):
        return self.receiving_team
