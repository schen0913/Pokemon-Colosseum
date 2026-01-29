import csv
import ast
import random
import math
from Pokemon import Pokemon, Move

# Type Matchup Table
TYPE_MATCHUP = {
    "Normal":     {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1},
    "Fire":       {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 1, "Grass": 2},
    "Water":      {"Normal": 1, "Fire": 2, "Water": 0.5, "Electric": 1, "Grass": 0.5},
    "Electric":   {"Normal": 1, "Fire": 1, "Water": 2, "Electric": 0.5, "Grass": 0.5},
    "Grass":      {"Normal": 1, "Fire": 0.5, "Water": 2, "Electric": 1, "Grass": 0.5}
}

# Load csvfile into a dictionary of move objects
def load_moves(filename):
    moves = {}

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader) # Skips header

        for row in reader:
            name, mtype, category, contest, pp, power, accuracy = row

            if accuracy == 'None':
                accuracy = None
            else:
                accuracy = int(accuracy)

            moves[name] = Move(name, mtype, category, contest, int(pp), int(power), accuracy)
        
    return moves    

# Load csvfile into a list of Pokemon objects
def load_pokedex(filename, move_dict):
    pokedex = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader) # Skips header

        for row in reader:
            name, ptype, hp, attack, defense, height, weight, moves = row
            
            # Convert moves into a list of move objects
            move_names = ast.literal_eval(moves)
            move_objs = []
            for m in move_names:
                move_objs.append(move_dict[m])

            pokedex.append(Pokemon(name, ptype, int(hp), int(attack), int(defense), int(height), int(weight), move_objs))

    return pokedex

# Get and return selected move from user
def choose_move(pokemon):
    avail_moves = pokemon.moves
    num_moves = len(pokemon.moves)
    selected = False
    move = None

    while not selected:
        print(f"\nChoose the move for {pokemon.name}:")

        # Print moves menu
        for i, move in enumerate(avail_moves, start=1):
            label = " (N/A)" if pokemon.moves[move] == 1 else ""
            print(f"{i}. {move.name}{label}")

        choice = input(f"Enter your move choice (1-{num_moves}): ")
        
        if not choice.isdigit():
            print("Invalid choice. Try again.")
            continue

        choice = int(choice) - 1
        if 0 <= choice < num_moves:
            move = list(pokemon.moves.keys())[choice]
            if pokemon.moves[move] == 0:
                selected = True
            else:
                print("Move is unavailable. Moves will reset once all have been used. Try again.")
        else:
            print("Invalid choice. Try again.")
    
    return move

# Calculate and return damage
def calc_damage(move, attacker, defender):
    stab = 1.5 if move.type == attacker.type else 1
    type_eff = TYPE_MATCHUP.get(move.type, {}).get(defender.type, 1)
    rand = random.uniform(0.5, 1)

    damage = move.power * (attacker.attack / defender.defense) * stab * type_eff * rand
    
    return math.ceil(damage)


def main():
    print("Welcome to Pokemon Colosseum!\n")
    player_name = input("Enter Player Name: ")

    # Load all csv files
    moves_dict = load_moves("moves-data.csv")
    pokedex = load_pokedex("pokemon-data.csv", moves_dict)

    # Create random pokemon teams
    random_pokemon = random.sample(pokedex, 6)
    team_rocket = random_pokemon[:3]
    team_player = random_pokemon[3:]

    # Print teams
    print("\nTeam Rocket enters with", ", ".join(p.name for p in team_rocket))
    print(f"Team {player_name} enters with", ", ".join(p.name for p in team_player))
    
    print("\nLet the battle begin!\n")

    # Select team to start
    turn = random.choice(['Rocket', player_name])
    print(f"Coin toss goes to ----- Team {turn} to start the attack!")

    # Battle while both teams still have Pokemon
    while team_rocket and team_player:
        
        # Identify attacker, defender, and move to be used
        if turn == player_name:
            attack_team = team_player
            attacker = attack_team[0]
            defend_team = team_rocket
            defender = defend_team[0]
            move = choose_move(attacker)
        else:
            attack_team = team_rocket
            attacker = attack_team[0]
            defend_team = team_player
            defender = defend_team[0]
            move = random.choice(attacker.avail_moves())

        attacker.use_move(move)
        damage = calc_damage(move, attacker, defender)
        defender.take_damage(damage)

        print(f"\nTeam {turn}'s {attacker.name} cast '{move.name}' to {defender.name}:")
        print(f"Damage to {defender.name} is {damage} points.")

        turn = 'Rocket' if turn == player_name else player_name

        if defender.hp <= 0:
            print(f"{defender.name} faints back to poke ball and {attacker.name} has {attacker.hp} HP\n")
            defend_team.pop(0)
            if defend_team:
                print(f"Next for Team {turn}, {defend_team[0].name} enters battle!")
        else:
            print(f"{defender.name} has {defender.hp} HP and {attacker.name} has {attacker.hp} HP")
    
    # Declare winning team
    if team_player:
        print(f"All of Team Rocket's Pokemon fainted. Team {player_name} prevails and restores peace!")
    else:
        print(f"All of Team {player_name}'s Pokemon fainted. Team Rocket wins....")               

if __name__ == "__main__":
    main()
