import csv
import ast
import random
from Pokemon import Pokemon, Move

# Load moves from csvfile into a dictionary of move objects
def load_moves(filename):
    moves = {}

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader) # Skips header

        for row in reader:
            name, mtype, category, contest, pp, power, accuracy = row
            moves[name] = Move(mtype, category, contest, int(pp), int(power), int(accuracy))
        
        return moves    

def load_pokedex(file):
    pass

def main():
    print("Welcome to Pokemon Colosseum!")
    player_name = input("Enter Player Name: ")




if __name__ == "__main__":
    main()
