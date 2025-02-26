from transitions import Machine


class Match:
    states = ['not_started', 'in_progress', 'finished']

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.set_in_progress = 1
        self.set1 = Set(21)
        self.set2 = Set(21)
        self.set3 = Set(15)
        self.sets_team1 = 0
        self.sets_team2 = 0
        self.current_state = 'not_started'
        self.machine = Machine(model=self, states=Match.states, initial='not_started')
        self.machine.add_transition(trigger='start_match', source='not_started', dest='in_progress')
        self.machine.add_transition(trigger='end_match', source='in_progress', dest='finished')

    def point_scored(self, team):
        if self.set_in_progress == 1:
            self.set1.point_scored(team)
        elif self.set_in_progress == 2:
            self.set2.point_scored(team)
        elif self.set_in_progress == 3:
            self.set3.point_scored(team)

    def set_scored(self, team):
        if team == self.team1:
            self.sets_team1 += 1
        elif team == self.team2:
            self.sets_team2 += 1
        else:
            raise ValueError("Invalid team")
        if self.sets_team1 == 2 or self.sets_team2 == 2:
            self.current_state = 'finished'

    def display_sets(self):
        print(f"Sets: {self.team1}: {self.sets_team1} - {self.team2}: {self.sets_team2}")

    def display_scores(self):
        print(f"Set1: {self.team1}: {self.set1.score_team1} - {self.team2}: {self.set1.score_team2}")
        print(f"Set2: {self.team1}: {self.set2.score_team1} - {self.team2}: {self.set2.score_team2}")
        print(f"Set3: {self.team1}: {self.set3.score_team1} - {self.team2}: {self.set3.score_team2}")


class Set:
    states = ['not_started', 'in_progress', 'finished']

    def __init__(self, max_score):
        self.max_score = max_score
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
        if self.score_team1 == self.max_score and self.score_team2 < self.max_score-1:
            self.current_state = 'finished'
        if self.score_team2 == self.max_score or self.score_team1 < self.max_score-1:
            self.current_state = 'finished'

    def display_score(self):
        print(f"Points: {self.team1}: {self.score_team1} - {self.team2}: {self.score_team2}")


