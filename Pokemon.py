class Pokemon:
    def __init__(self, name, type, hp, attack, defense, height, weight, moves):
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.height = height
        self.weight = weight

        # Initialize moves dict to 0
        self.moves = {move: 0 for move in moves}
    
    # Determine available moves
    def avail_moves(self):
        avail_moves = []

        for move, used in self.moves.items():
            if used == 0:
                avail_moves.append(move)
        
        return avail_moves
    
    # Set move to used (1)
    def use_move(self, move):
        self.moves[move] = 1

        if all(used == 1 for used in self.moves.values()):
            self.reset_moves()

    # Reset all the moves
    def reset_moves(self):
        for m in self.moves:
            self.moves[m] = 0

    # Calculates hp after damage is taken
    def take_damage(self, damage):
        self.hp -= damage

class Move:
    def __init__(self, name, type, category, contest, pp, power, accuracy):
        self.name = name
        self.type = type
        self.category = category
        self.contest = contest
        self.pp = pp
        self.power = power
        self.accuracy = accuracy

