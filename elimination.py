import random
import time

def number_of_teams():
    team_count = input("Enter the number of teams: ")
    teams = []
    try:
        team_count = int(team_count)
        if team_count < 2:
            raise ValueError("Number of teams must be at least 2.")
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter a valid number.")
        return number_of_teams()
    for i in range(team_count):
        team_name = "Team " + str(i+1)
        teams.append(team_name)
    if len(teams) % 2 != 0:
        teams.append("Bye")  # Add a bye for odd number of teams
    return teams

def simulate(team1, team2):
    winner = random.choice ([team1, team2])
    return winner


def pair (teams):
    current_round = 1
    fixtures = {}
    current_teams = teams.copy()
    
    while len(current_teams) > 1 :
        round_name =  (f"Round {current_round}")
        print (round_name)
        fixtures[round_name] = {
            'round_teams':current_teams.copy(),
            'matches': []
        }
        next_round_teams = []
        random.shuffle(current_teams)
        print (f"Current teams are: {current_teams}")
        for i in range(0,len(current_teams), 2):
            if i+1 < len(current_teams):
                team1, team2 = current_teams[i], current_teams[i+1]
                winner = simulate(team1, team2)
                fixtures[round_name]['matches'].append(f"{team1} vs {team2} -> Winner: {winner}")
                next_round_teams.append(winner)
            else:
                next_round_teams.append(current_teams[i])
                fixtures[round_name]['matches'].append(f"{current_teams[i]} has a bye.")
        current_teams = next_round_teams
        current_round += 1
        print (f" Next round teams are: {next_round_teams}")
        print (current_teams)
        
    if current_teams:
        fixtures["Final"] = current_teams[0]
        return fixtures
    '''
     # Alternatively, store champion in the same dictionary structure
    if current_teams:
       fixtures["Champion"] = {
            'round_teams': current_teams.copy(),
            'matches': [],
            'winner': current_teams[0]
        }
         # and print like this:
        if round_name == "Champion":
        print(f"Trophy Winner: {round_data['winner']}")
'''


teams = number_of_teams()
print(f"Teams: {teams}")
tournament= pair(teams)
print(tournament)

for round, round_data in tournament.items():
    print(f"\n{round}:")
    
    if round == 'Final':
        print (f"Trophy Winner: {round_data}")
    else:    
        print (f"Teams in this round: {', '.join(round_data['round_teams'])}") #use join to remove the list brackets
        
        if isinstance(round_data, dict):
            for match in round_data['matches']:
                print(match)
                time.sleep(1)
    
'''
# former print style without round teams
for round_name, matches in tournament.items():
    
    
    print(f"{round_name}:")
    if isinstance(matches, list):
        for match in matches:
            print(match)
            time.sleep(1)
    else:
        print(f"Trophy Winner: {matches}")  

'''
        
            
            
        
