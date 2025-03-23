import random
from match import Match
from match import Team
from match import Player

def main():
    # Initialize game components
    # For example, create teams, players, etc.
    team1_serve = {'fail': 10, 'bad': 20, 'good': 50, 'perfect': 20}
    team1_receive = {'fail': 10, 'bad': 30, 'good': 30, 'perfect': 30}
    team1_skills = {'serve': team1_serve, 'receive': team1_receive}
    team2_serve = {'fail':15,'bad':10,'good':40,'perfect':35}
    team2_receive = {'fail':15,'bad':25,'good':40,'perfect':20}
    team2_skills = {'serve':team1_serve,'receive':team1_receive}

    team1 = Team("Team A", team1_skills)
    team2 = Team("Team B", team2_skills)

    # Create a match instance
    match = Match(team1, team2)
    serving_team = team1
#    serving_team = random.choices([team1, team2])

    # Main game loop
    points = 0
    while match.current_state != 'finished':

        points = points + 1
        print(f"Points: {points}")
        print(f"Serving: {serving_team.name}")
        if serving_team == team1:
            receiving_team = team2
        else:
            receiving_team = team1

        # Example: Simulate some points being scored
        serving_team = match.play_point_action(serving_team, receiving_team)
        print(f"Point winner: {serving_team.name}")

        # Display match score
        match.display_sets()
        match.display_scores()

        # Check if the match is over
        if (match.current_state == 'finished') or (points == 200):
            print("Match is over!")
            break

    # End the match

if __name__ == "__main__":
    main()