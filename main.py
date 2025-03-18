import random
from match import Match
from match import Team
from match import Player
# Import other game components as needed

def main():
    # Initialize game components
    # For example, create teams, players, etc.
    team1 = Team("Team A", 70)
    team2 = Team("Team B", 70)

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
    match.end_match()

if __name__ == "__main__":
    main()