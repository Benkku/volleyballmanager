from transitions import Machine


class Match:
    states = ['not_started', 'in_progress', 'finished']

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.sets_team1 = 0
        self.sets_team2 = 0
        self.current_state = 'not_started'
        self.machine = Machine(model=self, states=Match.states, initial='not_started')
        self.machine.add_transition(trigger='start_match', source='not_started', dest='in_progress')
        self.machine.add_transition(trigger='end_match', source='in_progress', dest='finished')

    def set_scored(self, team):
        if team == self.team1:
            self.sets_team1 += 1
        elif team == self.team2:
            self.sets_team2 += 1
        else:
            raise ValueError("Invalid team")
        if self.sets_team1 == 3 or self.sets_team2 == 3:
            self.current_state = 'finished'

    def display_score(self):
        print(f"Sets: {self.team1}: {self.sets_team1} - {self.team2}: {self.sets_team2}")


class Set:
    states = ['not_started', 'in_progress', 'finished']

    def __init__(self, team1, team2):
        self.score_team1 = 0
        self.score_team2 = 0
        self.current_state = 'not_started'
        self.machine = Machine(model=self, states=Match.states, initial='not_started')
        self.machine.add_transition(trigger='start_set', source='not_started', dest='in_progress')
        self.machine.add_transition(trigger='end_set', source='in_progress', dest='finished')

    def point_scored(self, team):
        if team == self.team1:
            self.score_team1 += 1
        elif team == self.team2:
            self.score_team2 += 1
        else:
            raise ValueError("Invalid team")
        if self.score_team1 == 25 or self.score_team2 == 25:
            self.current_state = 'finished'

