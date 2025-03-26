import random
import numpy as np
from platform import machine

from transitions import Machine, State


class Rally(object):
    states = ["serve", "end", "reception", "setting", "attack","defense"]
    ball_action_states = ["fail", "bad","good", "perfect"]
   # success_ball_action_states = [ "bad","good", "perfect"]

    def __init__(self, serving_team, receiving_team):
        self.serving_team=serving_team
        self.receiving_team=receiving_team
        self.machine = Machine(model=self, states=Rally.states, initial="serve")
        self.machine.add_transition("fail", "*", "end")
        self.machine.add_transition("success", "serve", "reception")
        self.machine.add_transition("success", "reception","setting")
        self.machine.add_transition("success", "setting", "attack")
        self.machine.add_transition("success", "attack", "defense")
        self.machine.add_transition("success", "defense","setting")

    def play_rally(self):
        #  stronger = random.choices([self.serving_team, self.receiving_team], weights=[self.serving_team.sideout_efficiency, self.receiving_team.sideout_efficiency], k=1)[0]
       # print(f"skills: {self.receiving_team.skill_data['serve']}")
        serve_value = self.generate_ball_action_quality(self.serving_team.skill_data['serve'])
        if serve_value == 'fail':
            self.machine.fail()
            return self.receiving_team
        #ELSE:
        self.machine.success()
        receive_value = self.generate_ball_action_quality(self.receiving_team.skill_data['receive'])
        if receive_value == 'fail':
            self.machine.fail()
            return self.serving_team
        print(f"Serve: {serve_value}, Receive: {receive_value}")
        reception_weights = [self.receiving_team.skill_data['receive']["fail"], self.serving_team.skill_data['serve']["perfect"] + self.receiving_team.skill_data['receive']["bad"], self.serving_team.skill_data['serve']["good"] + self.receiving_team.skill_data['receive']["good"], self.serving_team.skill_data['serve']["bad"] + self.receiving_team.skill_data['receive']["perfect"]]
        reception_value = self.generate_ball_action_quality(reception_weights)
        if reception_value == 'fail':
            self.machine.fail()
            return self.serving_team
        return self.serving_team

    def generate_ball_action_quality(self, weights):
        quality = random.choices(Rally.ball_action_states, weights=[weights["fail"],weights["bad"],weights["good"],weights["perfect"], ], k=1)[0]
        return quality

    def server_wins(self):
        return self.serving_team

    def receiver_wins(self):
        return self.receiving_team

    def ace(self):
        return self.serving_team

    def serve_fail(self):
        return self.receiving_team
