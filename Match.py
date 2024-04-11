from transitions import Machine


class Match:
    states = ['not_started', 'in_progress', 'finished']

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.score_team1 = 0
        self.score_team2 = 0
        self.current_state = 'not_started'
        self.machine = Machine(model=self, states=Match.states, initial='not_started')
        self.machine.add_transition(trigger='start_match', source='not_started', dest='in_progress')
        self.machine.add_transition(trigger='end_match', source='in_progress', dest='finished')

    def point_scored(self, team):
        if team == self.team1:
            self.score_team1 += 1
        elif team == self.team2:
            self.score_team2 += 1
        else:
            raise ValueError("Invalid team")

    def display_score(self):
        print(f"Score: {self.team1}: {self.score_team1} - {self.team2}: {self.score_team2}")


