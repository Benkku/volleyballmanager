import random
from transitions import Machine, State


class Match:
    states = ['not_started', 'in_progress', 'finished']

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.set_in_progress = 1
        self.set1 = Set(21, team1, team2)
        self.set2 = Set(21, team1, team2)
        self.set3 = Set(15, team1, team2)
        self.sets_team1 = 0
        self.sets_team2 = 0
        self.current_state = 'not_started'
        self.machine = Machine(model=self, states=Match.states, initial='not_started')
        self.machine.add_transition(trigger='start_match', source='not_started', dest='in_progress')
        self.machine.add_transition(trigger='end_match', source='in_progress', dest='finished')

    def play_point_action(self, serving_team, receiving_team):
       # winner = random.choices([self.team1, self.team2], weights=[self.team1.sideout_efficiency, self.team2.sideout_efficiency], k=1)[0]
        rally= Rally(serving_team, receiving_team)
        winner=rally
        self.point_scored(winner)
        return winner

    def point_scored(self, team):
        if self.set_in_progress == 1:
            self.set1.point_scored(team)
            if self.set1.current_state == 'set_finished':
                self.set_scored(team)
                self.set_in_progress = 2
        elif self.set_in_progress == 2:
            self.set2.point_scored(team)
            if self.set2.current_state == 'set_finished':
                self.set_scored(team)
                print(f" Team1: {self.sets_team1} - Team2: {self.sets_team2}")
        elif self.set_in_progress == 3:
            if self.set3.current_state == 'set_finished':
                self.set_scored(team)
            else:
                self.set3.point_scored(team)

    def set_scored(self, team):
        if team == self.team1:
            self.sets_team1 += 1
        elif team == self.team2:
            self.sets_team2 += 1
        else:
            raise ValueError("Invalid team")
        if ((self.sets_team1 == 2) or (self.sets_team2 == 2)):
            print(f"sets_team1 == 2: {self.sets_team1 == 2} - sets_team2 == 2: {self.sets_team2 == 2}")
            self.current_state = 'finished'
        else:
            self.set_in_progress += 1
        print(f"Set scored: Team1: {self.sets_team1} - Team2: {self.sets_team2}")

    def display_sets(self):
        print(f"Sets: Team1: {self.sets_team1} - Team2: {self.sets_team2}")

    def display_scores(self):
        print(f"Set1: Team1: {self.set1.score_team1} - Team2: {self.set1.score_team2}")
        print(f"Set2: Team1: {self.set2.score_team1} - Team2: {self.set2.score_team2}")
        print(f"Set3: Team1: {self.set3.score_team1} - Team2: {self.set3.score_team2}")

class Set:
    states = ['set_not_started', 'set_in_progress', 'set_finished']

    def __init__(self, max_score, team1, team2):
        self.max_score = max_score
        self.team1 = team1
        self.team2 = team2
        self.score_team1 = 0
        self.score_team2 = 0
        self.current_state = 'set_not_started'
        self.machine = Machine(model=self, states=Match.states, initial='not_started')
        self.machine.add_transition(trigger='start_set', source='not_started', dest='in_progress')
        self.machine.add_transition(trigger='end_set', source='in_progress', dest='finished')

    def point_scored(self, team):
        self.current_state = 'set_in_progress'
        if team == self.team1:
            self.score_team1 += 1
        elif team == self.team2:
            self.score_team2 += 1
        else:
            raise ValueError("Invalid team")
        if ((self.score_team1 >= self.max_score) and (self.score_team2 < (self.score_team1-1))):
            self.current_state = 'set_finished'
            print(f"Set finished: Team1: {self.score_team1} - Team2: {self.score_team2}")
            print(f"Max: {self.max_score}")
        if ((self.score_team2 >= self.max_score) and (self.score_team1 < (self.score_team2-1))):
            self.current_state = 'set_finished'
            print(f"Set finished: Team1: {self.score_team1} - Team2: {self.score_team2}")
            print(f"Max: {self.max_score}")

    def display_score(self):
        print(f"Points: {self.team1}: {self.score_team1} - {self.team2}: {self.score_team2}")

class Team:

    def __init__(self, name, sideout_efficiency):
        self.name = name
        self.sideout_efficiency = sideout_efficiency
        self.player1 = Player("Pekka", sideout_efficiency)
        self.player2 = Player("Kimmo", sideout_efficiency)

class Player:

    def __init__(self, name, sideout_efficiency):
        self.sideout_efficiency = sideout_efficiency
        self.name = name

class Rally(object):
    states = ["serve", "end"]
    ball_action_states = ["failure", "bad","good", "perfect"]

    def __init__(self, serving_team, receiving_team):
        self.serving_team=serving_team
        self.receiving_team=receiving_team
        self.machine = Machine(model=self, states=Rally.states, initial="serve")
        self.machine.add_transition("ace", "serve", "end", after="server_wins")
        self.machine.add_transition("serve_fail", "serve", "end", after="receiver_wins")

    def play_rally(self):
        stronger = random.choices([self.serving_team, self.receiving_team], weights=[self.serving_team.sideout_efficiency, self.receiving_team.sideout_efficiency], k=1)[0]
        if stronger == self.serving_team:
            self.ace()
        else:
            self.serve_fail()

    def server_wins(self):
        return self.serving_team

    def receiver_wins(self):
        return self.receiving_team