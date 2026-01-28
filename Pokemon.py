class Pokemon:
    def __init__(self, name, type, hp, attack, defense, moves):
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense

        # Initialize moves dict to 0
        self.moves = {move: 0 for move in moves}
    
    # Determine available moves
    def avail_moves(self):
        avail_moves = []

        for move, use in self.moves.items():
            if use == 1:
                avail_moves.append(move)
        
        return avail_moves
    
    # Set move to used (1)
    def use_move(self, move):
        self.moves[move] = 1

        if all(use == 1 for use in self.moves.values()):
            self.reset_moves

    # Reset all the moves
    def reset_moves(self):
        for m in self.moves:
            self.moves[m] = 0

    # Calculates and returns hp after damage is taken
    def take_damage(self, damage):
        self.hp -= damage
        return self.hp

class Move:
    def __init__(self, type, category, contest, pp, power, accuracy):
        self.type = type
        self.category = category
        self.contest = contest
        self.pp = pp
        self.power = power
        self.accuracy = accuracy

