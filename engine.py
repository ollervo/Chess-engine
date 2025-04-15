import board
import numpy as np
import random

class engine:
    def __init__(self):
        pass
    
    def opposite_color(self,color):
        if color == "w":
            return "b"
        elif color == "b":
            return "w"
        else:
            return None

    def calculate_ply(self,brd,color):
        moves = brd.all_moves(color)
        dir = {}
        for piece in moves:
            for i in moves[piece]:
                newboard = brd.move_new(piece[0],piece[1],i[0],i[1])
                dir[(piece,i)] = newboard
        return dir
    
    def calculate_move(self,brd,color):
        first = self.calculate_ply(brd,color)
        dir = {}
        for move,bord in first.items():
            lastmoves = self.calculate_ply(bord,self.opposite_color(color))
            for i,j in lastmoves.items():
                dir[(move,i)] = j
        return dir

    def calculate_next_move_by_history(self,history,color):
        dir = {}
        for hist,brd in history.items():
            moves = self.calculate_move(brd,color)
            for i,j in moves.items():
                key = hist + i
                dir[key] = j
        return dir

    def calculate_next_n_moves(self,brd,color,n):
        history = self.calculate_move(brd,color)
        for i in range(n-1):
            newhist = self.calculate_next_move_by_history(history,color)
            history = newhist
        return history
    
    def evaluate(self,brd,color):
        positions = self.calculate_move(brd,color)
        hist = positions.keys()
        move1 = brd.all_moves(color)
        moves = []
        for move in move1:
            for i in move1[move]:
                moves.append((move,i))
        best = [[-999,""],[-999,""],[-999,""]]
        for move in moves:
            worst = 999
            for i in hist:
                if i[0] == move:
                    material = positions[i].material_difference(color) + positions[i].center_control(color) + positions[i].minor_quality(color) + positions[i].is_castled(color) + positions[i].no_f3(color) + positions[i].rook_moving_fix(color) + positions[i].pawns_up_when_no_queens(color) + positions[i].attack_undefended_things(color)
                    if positions[i].move_is_capture(i[1]):
                        row,col = i[1][1]
                        if positions[i].isAttackedSquare(row,col,self.opposite_color(color)) and not positions[i].isAttackedSquare(row,col,color):
                            material = material + positions[i].brd[row][col].value
                    if material <= worst:
                        worst = material
            if worst > best[0][0]: #min-max
                best[0][0] = worst
                best[0][1] = move
            elif worst > best[1][0]:
                best[1][0] = worst
                best[1][1] = move
            elif worst > best[2][0]:
                best[2][0] = worst  
                best[2][1] = move
        print(best)
        bestest = []
        if best[0][0] == -999:
            return None
        rand = random.random()
        for i in best:
            if i[0] == best[0][0]:
                bestest.append(i)
        space = np.linspace(0,1,len(bestest)+1)
        if len(bestest) == 1:
            return bestest[0]
        for j in range(1, len(bestest)+1):
            if rand <= space[j]:
                return bestest[j-1]
    def evaluate_after_one_move(self,brd,color):
        positions = self.calculate_move(brd,color)
        hist = positions.keys()
        move1 = brd.all_moves(color)
        moves = []
        for move in move1:
            for i in move1[move]:
                moves.append((move,i))
        best = [[-999,""],[-999,""],[-999,""]]
        for move in moves:
            worst = 999
            for i in hist:
                if i[0] == move:
                    material = positions[i].material_difference(color) + positions[i].center_control(color) + positions[i].minor_quality(color) + positions[i].is_castled(color)
                    if material <= worst:
                        worst = material
            if worst > best[0][0]: #min-max
                best[0][0] = worst
                best[0][1] = move
            elif worst > best[1][0]:
                best[1][0] = worst
                best[1][1] = move
            elif worst > best[2][0]:
                best[2][0] = worst  
                best[2][1] = move
        bestest = []
        if best[0][0] == -999:
            return None
        rand = random.random()
        for i in best:
            if i[0] == best[0][0]:
                bestest.append(i)
        space = np.linspace(0,1,len(bestest)+1)
        if len(bestest) == 1:
            return bestest[0]
        for j in range(1, len(bestest)+1):
            if rand <= space[j]:
                return bestest[j-1]
    def calculate_next_ply_for_captures(self,brd,color):
        moves = brd.all_moves(color)
        dir = {}
        for piece in moves:
            for i in moves[piece]:
                newboard = brd.move_new(piece[0],piece[1],i[0],i[1])
                dir[(piece,i)] = newboard
        return dir

                