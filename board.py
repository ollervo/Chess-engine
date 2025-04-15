#Chess
import os
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import engine

#os.chdir("C:/Users/Administrator/Desktop/python/chess")
# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 80  # Pixels per square
#Class for the board
class board:
    def __init__(self,board_FEN):
        if type(board_FEN) is str:
            self.brd = FEN_to_board(board_FEN)
        elif type(board_FEN) is list:
            self.brd = board_FEN.copy()
        else:
            self.brd = FEN_to_board(initial_board_FEN)
        self.enpassant = None
        #Castling rights w O-O-O,w O-O, b O-O-O, b O-O
        self.castle = [True,True,True,True]

    def get_piece(self,row,col):
        if (row in range(8) and (col in range(8))):
            return self.brd[row][col]
        else:
            return -1

    def get_piece_color(self,row,col):
        if self.isPiece(row,col):
            return self.brd[row][col].color
        else:
            return None

    def set_piece(self,row,col,piece):
        if (row in range(8) and (col in range(8))):
            self.brd[row][col] = piece
    def isEmpty(self,row,col):
        return self.get_piece(row,col)==""
    def isEnemy(self,row,col,color):
        if color == "w" or color == "b":
            return self.isPiece(row,col) and (color != self.get_piece_color(row,col))
        else:
            return False
    def isPiece(self,row,col):
        return self.get_piece(row,col)!="" and self.get_piece(row,col)!=-1
    def isPieceCol(self,row,col,color):
        if self.isPiece(row,col):
            return self.brd[row][col].color == color
        else:
            return False
    def isWhitePiece(self,row,col):
        return self.isPiece(row,col) and self.get_piece(row,col).color == "w"
    def isBlackPiece(self,row,col):
        return self.isPiece(row,col) and self.get_piece(row,col).color == "b"
    
    def all_moves(self,color):
        dir = {}
        for i in range(8):
            for j in range(8):
                if self.isPieceCol(i,j,color):
                    dir[(i,j)] = self.legal_moves(i,j)
        return dir
    
        
    def can_move(self,row,col,color):
        if color == "w":
            return self.isEmpty(row,col) or self.isBlackPiece(row,col)
        else:
            return self.isEmpty(row,col) or self.isWhitePiece(row,col)

    def move(self,old_row,old_col,row,col):
        piece = self.get_piece(old_row,old_col)
        enpas = self.enpassant
        self.enpassant = None
        if type(piece) is pawn:
            if ((old_row,row) == (1,3)) or ((old_row,row) == (6,4)): #Prime en passant when a pawn moves two squares
                change = row-old_row
                self.enpassant = (int(old_row + change/2),old_col)
            if row == 0 or row == 7: #Queening
                self.set_piece(row,col,queen(piece.color))
                self.set_piece(old_row,old_col,"")
            elif (row,col) == enpas: #En passant
                if piece.color == "w":
                    self.set_piece(row,col,piece)
                    self.set_piece(old_row,old_col,"")
                    self.set_piece(row+1,col,"")
                else:
                    self.set_piece(row,col,piece)
                    self.set_piece(old_row,old_col,"")
                    self.set_piece(row-1,col,"")
            else:
                self.set_piece(row,col,piece)
                self.set_piece(old_row,old_col,"")
        elif type(piece) is king: #Castling
            if old_col==4 and (col == 6 or col == 2):
                if col == 2:
                    self.set_piece(row,col,piece)
                    self.set_piece(old_row,old_col,"")
                    self.set_piece(row,3,rook(piece.color))
                    self.set_piece(old_row,0,"")
                else:
                    self.set_piece(row,col,piece)
                    self.set_piece(old_row,old_col,"")
                    self.set_piece(row,5,rook(piece.color))
                    self.set_piece(old_row,7,"")
            else:
                self.set_piece(row,col,piece)
                self.set_piece(old_row,old_col,"")
            if piece.color == "w":
                self.castle[0] = False
                self.castle[1] = False
            else:
                self.castle[2] = False
                self.castle[3] = False
        elif type(piece) is rook:
            self.set_piece(row,col,piece)
            self.set_piece(old_row,old_col,"")
            if piece.color == "w":
                if (old_row,old_col) == (7,7):
                    self.castle[0] = False
                elif (old_row,old_col) == (7,0):
                    self.castle[1] = False
            else:
                if (old_row,old_col) == (0,7):
                    self.castle[2] = False
                elif (old_row,old_col) == (0,0):
                    self.castle[3] = False
        else: #Move normally
            self.set_piece(row,col,piece)
            self.set_piece(old_row,old_col,"")
    
    def move_new(self,old_row,old_col,row,col):
        piece = self.get_piece(old_row,old_col)
        enpas = self.enpassant
        
        newboard = []
        for i in range(8):
            x = []
            for j in range(8):
                x.append(self.brd[i][j])
            newboard.append(x)
        

        cast = self.castle.copy()
        if type(piece) is pawn:
            if ((old_row,row) == (1,3)) or ((old_row,row) == (6,4)): #Prime en passant when a pawn moves two squares
                change = row-old_row
                enpas = (int(old_row + change/2),old_col)
            if row == 0 or row == 7: #Queening
                newboard[row][col] = queen(piece.color)
                newboard[old_row][old_col] = ""
            elif (row,col) == enpas: #En passant
                if piece.color == "w":
                    newboard[row][col] = piece
                    newboard[old_row][old_col] = ""
                    newboard[row+1][col] = ""
                else:
                    newboard[row][col] = piece
                    newboard[old_row][old_col] = ""
                    newboard[row-1][col] = ""
            else:
                newboard[row][col] = piece
                newboard[old_row][old_col] = ""
        elif type(piece) is king: #Castling
            if old_col==4 and (col == 6 or col == 2):
                if col == 2:
                    newboard[row][col] = piece
                    newboard[old_row][old_col] = ""
                    newboard[row][3] = rook(piece.color)
                    newboard[old_row][0] = ""
                else:
                    newboard[row][col] = piece
                    newboard[old_row][old_col] = ""
                    newboard[row][5] = rook(piece.color)
                    newboard[old_row][7] = ""
            else:
                newboard[row][col] = piece
                newboard[old_row][old_col] = ""
            if piece.color == "w":
                cast[0] = False
                cast[1] = False
            else:
                cast[2] = False
                cast[3] = False
        elif type(piece) is rook:
            newboard[row][col] = piece
            newboard[old_row][old_col] = ""
            if piece.color == "w":
                if (old_row,old_col) == (7,7):
                    cast[0] = False
                elif (old_row,old_col) == (7,0):
                    cast[1] = False
            else:
                if (old_row,old_col) == (0,7):
                    cast[2] = False
                elif (old_row,old_col) == (0,0):
                    cast[3] = False
        else: #Move normally
            newboard[row][col] = piece
            newboard[old_row][old_col] = ""
        newboardret = board(newboard)
        newboardret.castle = cast
        newboardret.enpassant = enpas
        return newboardret

    def material_count(self,color):
        material = 0
        for i in range(8):
            for j in range(8):
                if self.isPieceCol(i,j,color):
                    material += self.brd[i][j].value
        return material
    
    def opposite_color(self,color):
        if color == "w":
            return "b"
        elif color == "b":
            return "w"
        else:
            return None

    def center_control(self,color):
        control = 0
        opp = self.opposite_color(color)
        for i in range(3,5):
            for j in range(3,5):
                if self.isAttackedSquare(i,j,opp):
                    control += 1
                if self.square_is_attacked_by_pawn(i,j,opp):
                    control += 1
        return control/4
    
    def is_not_pawn(self,row,col,color):
        if self.isPieceCol(row,col,color):
            return type(self.brd[row][col]) is not pawn
        else:
            return True

    def no_f3(self,color):
        ans = 0
        if color == "w":
            if self.is_not_pawn(6,5,color):
                ans = ans - 2
            if self.is_not_pawn(6,4,color):
                ans += 2
            if self.is_not_pawn(6,3,color):
                ans += 2
        else:
            if self.is_not_pawn(1,5,color):
                ans = ans - 2
            if self.is_not_pawn(1,4,color):
                ans += 2
            if self.is_not_pawn(1,3,color):
                ans += 2
        return ans
    
    def is_castled(self,color):
        ans = 0
        if color == "w":
            if type(self.brd[7][6]) is king or type(self.brd[7][2]) is king:
                ans = 2
        else: 
            if type(self.brd[0][6]) is king or type(self.brd[0][2]) is king:
                ans = 2
        return ans
    
    def move_is_capture(self,move):
        row = move[1][0]
        col = move[1][1]
        return self.isPiece(row,col)

    def number_of_all_pieces(self):
        count = 0
        for i in range(8):
            for j in range(8):
                if self.isPiece(i,j):
                    count += 1
        return count
    
    def no_queens(self,color):
        ans = True
        for i in range(8):
            for j in range(8):
                if self.isPieceCol(i,j,color):
                    if type(self.brd[i][j]) is queen:
                        ans = False
        return ans
    
    def pawns_up_when_no_queens(self,color):
        if not self.no_queens(color):
            return 0
        pawncount = 0
        count = 0
        for i in range(1,6):
            for j in range(8):
                if self.isPieceCol(i,j,color):
                    if type(self.brd[i][j]) is pawn:
                        pawncount += 1
                        if color == "w":
                            count += 6-i
                        else:
                            count += i - 1
        return count/(pawncount*5)

    def number_of_pieces(self,color):
        counter = 0
        for i in range(8):
            for j in range(8):
                if self.isPieceCol(i,j,color):
                    counter += 1
        return counter

    def attack_undefended_things(self,color):
        if self.number_of_pieces(color) > 8:
            return 0
        count = 0
        opp = self.opposite_color(color)
        for i in range(8):
            for j in range(8):
                if self.isPieceCol(i,j,opp):
                    if self.isAttacked(i,j) and not self.isAttackedSquare(i,j,color):
                        count += self.brd[i][j].value/2
        return count


    def rook_moving_fix(self,color):
        pieces = self.number_of_pieces(color)
        ans = 0
        if color == "w":
            if not (self.isWhitePiece(7,0) and type(self.brd[7][0]) is rook):
                ans = -pieces/32
        else:
            if not (self.isBlackPiece(0,0) and type(self.brd[0][0]) is rook):
                ans = -pieces/32
        return ans

    def minor_quality(self,color):
        count = 0
        if color == "w":
            for i in range(8):
                if self.isPieceCol(7,i,color):
                    if (type(self.brd[7][i]) is bishop) or (type(self.brd[7][i]) is knight):
                        count = count - 1
        else:
            for i in range(8):
                if self.isPieceCol(0,i,color):
                    if (type(self.brd[0][i]) is bishop) or (type(self.brd[0][i]) is knight):
                        count = count - 1
        return count
    
    def material_difference(self,color):
        diff = self.material_count("w")-self.material_count("b")
        if color == "w":
            return diff
        else:
            return -diff

    def isKing(self,row,col,color):
        piece = self.get_piece(row,col)
        if self.isPiece(row,col):
            return piece.color == color and type(piece) == king
        return False
    
    def isChecked(self,color): #Check if color is in check?
        for i in range(8):
            for j in range(8):
                if self.isKing(i,j,color):
                    return self.isAttacked(i,j)
        return False
    
    def check_move(self,old_row,old_col,row,col): #Checks if move is legal by checking if the resulting position is legal. (own king not in check)
        if not self.isPiece(old_row,old_col):
            return False
        old = self.get_piece(old_row,old_col)
        new = self.get_piece(row,col)
        color = old.color
        ans = False
        if type(old) is pawn:
            if (row,col) == self.enpassant: #En passant
                if color == "w":
                    self.set_piece(row,col,old)
                    self.set_piece(old_row,old_col,"")
                    self.set_piece(row+1,col,"")
                    ans = self.isChecked(color)
                    self.set_piece(row,col,new)
                    self.set_piece(old_row,old_col,old)
                    self.set_piece(row+1,col,pawn("b"))
                else:
                    self.set_piece(row,col,old)
                    self.set_piece(old_row,old_col,"")
                    self.set_piece(row-1,col,"")
                    ans = self.isChecked(color)
                    self.set_piece(row,col,new)
                    self.set_piece(old_row,old_col,old)
                    self.set_piece(row+1,col,pawn("w"))
            else:
                self.set_piece(row,col,old)
                self.set_piece(old_row,old_col,"")
                ans = self.isChecked(color)
                self.set_piece(row,col,new)
                self.set_piece(old_row,old_col,old)
        else: #Move normally
            self.set_piece(row,col,old)
            self.set_piece(old_row,old_col,"")
            ans = self.isChecked(color)
            self.set_piece(row,col,new)
            self.set_piece(old_row,old_col,old)
        return ans
    

    def legal_moves(self,row,col):
        moves = self.moves(row,col)
        if not moves:
            return []
        legal_moves = []
        for move in moves:
            if not self.check_move(row,col,move[0],move[1]):
                legal_moves.append(move)
        return legal_moves
    def isAttacked(self,row,col):
        if self.isPiece(row,col):
            return self.isAttackedSquare(row,col,self.get_piece_color(row,col))
        else:
            return False
    def isAttackedSquare(self,row,col,color):
        if color is None:
            return False
        for i in self.rook_moves(row,col,color):
            if self.isEnemy(i[0],i[1],color) and type(self.get_piece(i[0],i[1]))==rook:
                return True
        for i in self.bishop_moves(row,col,color):
            if self.isEnemy(i[0],i[1],color) and type(self.get_piece(i[0],i[1]))==bishop:
                return True
        for i in self.queen_moves(row,col,color):
            if self.isEnemy(i[0],i[1],color) and type(self.get_piece(i[0],i[1]))==queen:
                return True
        for i in self.knight_moves(row,col,color):
            if self.isEnemy(i[0],i[1],color) and type(self.get_piece(i[0],i[1]))==knight:
                return True
        moves = []
        for i in range(-1,2):
            for j in range(-1,2):
                if self.can_move(row+i,col+j,color) and (i != 0 or j != 0):
                    moves.append((row+i,col+j))       
        for i in moves:
            if self.isEnemy(i[0],i[1],color) and type(self.get_piece(i[0],i[1]))==king:
                return True

        if color == "w":
            if (self.isBlackPiece(row-1,col+1) and type(self.get_piece(row-1,col+1))==pawn) or (self.isBlackPiece(row-1,col-1) and type(self.get_piece(row-1,col-1))==pawn):
                return True
        else:
            if (self.isWhitePiece(row+1,col+1) and type(self.get_piece(row+1,col+1))==pawn) or (self.isWhitePiece(row+1,col-1) and type(self.get_piece(row+1,col-1))==pawn):
                return True
        return False
    
    def square_is_attacked_by_pawn(self,row,col,color):
        if color is None:
            return False
        if color == "w":
            if (self.isBlackPiece(row-1,col+1) and type(self.get_piece(row-1,col+1))==pawn) or (self.isBlackPiece(row-1,col-1) and type(self.get_piece(row-1,col-1))==pawn):
                return True
        else:
            if (self.isWhitePiece(row+1,col+1) and type(self.get_piece(row+1,col+1))==pawn) or (self.isWhitePiece(row+1,col-1) and type(self.get_piece(row+1,col-1))==pawn):
                return True
        return False
    def pawn_moves(self,row,col,color):
        moves = []
        if color == "b":
            if self.isEmpty(row+1,col):
                moves.append((row+1,col))
                if row == 1 and self.isEmpty(row+2,col):
                    moves.append((row+2,col))
            if self.isWhitePiece(row+1,col+1) or (row+1,col+1) == self.enpassant:
                moves.append((row+1,col+1))
            if self.isWhitePiece(row+1,col-1) or (row+1,col-1) == self.enpassant:
                moves.append((row+1,col-1))
        else:
            if self.isEmpty(row-1,col):
                moves.append((row-1,col))
                if row == 6 and self.isEmpty(row-2,col):
                    moves.append((row-2,col))
            if self.isBlackPiece(row-1,col+1) or (row-1,col+1) == self.enpassant:
                moves.append((row-1,col+1))
            if self.isBlackPiece(row-1,col-1) or (row-1,col-1) == self.enpassant:
                moves.append((row-1,col-1))
        return moves
    def king_moves(self,row,col,color):
        moves = []
        piece = self.get_piece(row,col)
        for i in range(-1,2):
            for j in range(-1,2):
                if self.can_move(row+i,col+j,color) and (i != 0 or j != 0):
                    moves.append((row+i,col+j))
        if type(piece) is king:
            if piece.color == "w":
                if self.castle[0] and self.isEmpty(7,5) and self.isEmpty(7,6) and not self.isAttackedSquare(7,6,"w") and not self.isAttackedSquare(7,5,"w") and not self.isAttackedSquare(7,4,"w"):
                    moves.append((7,6))
                if self.castle[1] and self.isEmpty(7,1) and self.isEmpty(7,2) and self.isEmpty(7,3) and not self.isAttackedSquare(7,2,"w") and not self.isAttackedSquare(7,3,"w") and not self.isAttackedSquare(7,4,"w"):
                    moves.append((7,2))
            else:
                if self.castle[2] and self.isEmpty(0,5) and self.isEmpty(0,6) and not self.isAttackedSquare(0,6,"b") and not self.isAttackedSquare(0,5,"b") and not self.isAttackedSquare(0,4,"b"):
                    moves.append((0,6))
                if self.castle[3] and self.isEmpty(0,1) and self.isEmpty(0,2)  and self.isEmpty(0,3) and (not self.isAttackedSquare(0,2,"b")) and not self.isAttackedSquare(0,3,"b") and not self.isAttackedSquare(0,4,"b"):
                    moves.append((0,2))
        return moves
        
    def rook_moves(self,row,col,color):
        moves = []
        for i in range(1,9):
            if self.isEmpty(row+i,col):
                moves.append((row+i,col))
            elif self.isEnemy(row+i,col,color):
                moves.append((row+i,col))
                break
            else:
                break
        for i in range(1,9):
            if self.isEmpty(row-i,col):
                moves.append((row-i,col))
            elif self.isEnemy(row-i,col,color):
                moves.append((row-i,col))
                break
            else:
                break
        for i in range(1,9):
            if self.isEmpty(row,col+i):
                moves.append((row,col+i))
            elif self.isEnemy(row,col+i,color):
                moves.append((row,col+i))
                break
            else:
                break
        for i in range(1,9):
            if self.isEmpty(row,col-i):
                moves.append((row,col-i))
            elif self.isEnemy(row,col-i,color):
                moves.append((row,col-i))
                break
            else:
                break
        return moves

    def bishop_moves(self,row,col,color):
        moves = []
        for i in range(1,9):
            if self.isEmpty(row+i,col+i):
                moves.append((row+i,col+i))
            elif self.isEnemy(row+i,col+i,color):
                moves.append((row+i,col+i))
                break
            else:
                break
        for i in range(1,9):
            if self.isEmpty(row-i,col-i):
                moves.append((row-i,col-i))
            elif self.isEnemy(row-i,col-i,color):
                moves.append((row-i,col-i))
                break
            else:
                break
        for i in range(1,9):
            if self.isEmpty(row-i,col+i):
                moves.append((row-i,col+i))
            elif self.isEnemy(row-i,col+i,color):
                moves.append((row-i,col+i))
                break
            else:
                break
        for i in range(1,9):
            if self.isEmpty(row+i,col-i):
                moves.append((row+i,col-i))
            elif self.isEnemy(row+i,col-i,color):
                moves.append((row+i,col-i))
                break
            else:
                break
        return moves

    def queen_moves(self,row,col,color):
        b = self.bishop_moves(row,col,color)
        r = self.rook_moves(row,col,color)
        return r+b
    
    def knight_moves(self,row,col,color):
        moves = []    
        for i in [1,-1]:
            for j in [2,-2]:
                if self.can_move(row+i,col+j,color):
                    moves.append((row+i,col+j))
                if self.can_move(row+j,col+i,color):
                    moves.append((row+j,col+i))
        return moves
    
    def moves(self,row,col):
        if not self.isPiece(row,col):
            return []
        piece = self.get_piece(row,col)
        color = self.get_piece_color(row,col)
        if type(piece) == pawn:
            return self.pawn_moves(row,col,color)
        if type(piece) == rook:
            return self.rook_moves(row,col,color)
        if type(piece) == bishop:
            return self.bishop_moves(row,col,color)
        if type(piece) == queen:
            return self.queen_moves(row,col,color)
        if type(piece) == king:
            return self.king_moves(row,col,color)
        if type(piece) == knight:
            return self.knight_moves(row,col,color)
        
#Create classes for pieces
class pawn:
    def __init__(self,color):
        self.color = color
        if self.color == "w":
            self.img = "P.png"
            self.id = "P"
        else:
            self.img = "pp.png"
            self.id = "p"
        self.value = 1


class king:
    def __init__(self,color):
        self.color = color
        if self.color == "w":
            self.img = "K.png"
            self.id = "K"
        else:
            self.img = "kk.png"
            self.id = "k"
        self.value = 0

class queen:
    def __init__(self,color):
        self.color = color
        if self.color == "w":
            self.img = "Q.png"
            self.id = "Q"
        else:
            self.img = "qq.png"
            self.id = "q" 
        self.value = 8
     
class rook:
    def __init__(self,color):
        self.color = color
        if self.color == "w":
            self.img = "R.png"
            self.id = "R"
        else:
            self.img = "rr.png"
            self.id = "r"
        self.value = 5
 
class bishop:
    def __init__(self,color):
        self.color = color
        if self.color == "w":
            self.img = "B.png"
            self.id = "B"
        else:
            self.img = "bb.png"
            self.id = "b"
        self.value = 3

class knight:
    def __init__(self,color):
        self.color = color
        if self.color == "w":
            self.img = "N.png"
            self.id = "N"
        else:
            self.img = "nn.png"
            self.id = "n"
        self.value = 3

# Chessboard setup

initial_board_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
KvsK_FEN = "8/8/3k4/8/3K4/8/8/8"

def FEN_to_board(FEN):
    board = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""]
    ]
    row = 0
    col = 0
    for char in FEN:
        if char == "r":
            board[row][col] = rook("b")
            col += 1
        elif char == "n":
            board[row][col] = knight("b")
            col += 1
        elif char == "b":
            board[row][col] = bishop("b")
            col += 1
        elif char == "q":
            board[row][col] = queen("b")
            col += 1
        elif char == "k":
            board[row][col] = king("b")
            col += 1
        elif char == "p":
            board[row][col] = pawn("b")
            col += 1
        elif char == "R":
            board[row][col] = rook("w")
            col += 1
        elif char == "N":
            board[row][col] = knight("w")
            col += 1
        elif char == "B":
            board[row][col] = bishop("w")
            col += 1
        elif char == "Q":
            board[row][col] = queen("w")
            col += 1
        elif char == "K":
            board[row][col] = king("w")
            col += 1
        elif char == "P":
            board[row][col] = pawn("w")
            col += 1
        elif char == "/":
            row += 1
            col = 0
        elif int(char) in range(1,9):
            col += int(char)
    return board


initial_board = board(initial_board_FEN)

#print(initial_board.all_moves("w"))
#for i,j in initial_board.all_moves("w"):
 #   print(i,j)


pieces = {}
pieces2 = [pawn("w"), rook("w"), knight("w"),
    bishop("w"), queen("w"), king("w"),
    pawn("b"), rook("b"), knight("b"),
    bishop("b"), queen("b"), king("b")]


class ChessGUI:
    def __init__(self, root):
        self.chessAI = engine.engine()
        self.AIcolor = "b"
        self.root = root
        self.root.title("Interactive Chessboard")
        self.legal_moves = []
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
        self.canvas.pack()
        self.selected_square = None
        self.selected_piece = None
        self.board = board(initial_board_FEN) # Copy initial board setup
        self.turn = "w"
        self.load_images()
        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.on_square_click)

    def win_popup(self):
        pass

    def load_images(self):
        """ Load and resize piece images """
        for piece in pieces2:
            img = Image.open(piece.img).resize((SQUARE_SIZE, SQUARE_SIZE))
            pieces[piece.id] = ImageTk.PhotoImage(img)

    def draw_board(self):
        """ Draws the chessboard squares """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    col * SQUARE_SIZE, row * SQUARE_SIZE,
                    (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                    fill=color
                )

    def draw_pieces(self):
        """ Draws the pieces on the board """
        self.canvas.delete("piece")  # Clear previous pieces
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row,col)
                if piece:
                    self.canvas.create_image(
                        col * SQUARE_SIZE, row * SQUARE_SIZE,
                        anchor=tk.NW, image=pieces[piece.id], tags="piece"
                    )

    def on_square_click(self, event):
        """ Handles square selection and movement """
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        if self.selected_square:
            # Move piece
            if (row,col) in self.legal_moves: #Deselect by clicking a nonlegal move
                old_row,old_col = self.selected_square
                self.board.move(old_row,old_col,row,col)
                self.selected_square = None  # Deselect
                self.draw_board()
                self.draw_pieces()
                if self.turn == "w": #Change turn
                    self.turn = "b"
                else:
                    self.turn = "w"
                if self.turn == self.AIcolor:
                    blacksmove = self.chessAI.evaluate(self.board,self.AIcolor)
                    if blacksmove:
                        blacksmove = blacksmove[1]
                        self.board.move(blacksmove[0][0],blacksmove[0][1],blacksmove[1][0],blacksmove[1][1])
                        self.draw_board()
                        self.draw_pieces()
                        if self.turn == "w": #Change turn
                            self.turn = "b"
                        else:
                            self.turn = "w"
                    else:
                        print("You won! (Or it is stalemate)")
            else: #Deselect by clicking a nonlegal move
                self.selected_square = None
                self.draw_board()
                self.draw_pieces()
                
        else:
            # Select a piece to move
            
            if self.board.isPiece(row,col) and self.board.get_piece(row,col).color == self.turn:
                self.selected_square = (row, col)
                self.selected_piece = self.board.get_piece(row,col)
                self.legal_moves = self.board.legal_moves(row,col)
                self.highlight_square([(row, col)]+self.legal_moves)


    def highlight_square(self, squares):
        #Highlights square selected and all legal moves with the piece
        self.draw_board()
        for i in squares:
            self.canvas.create_rectangle(
                i[1] * SQUARE_SIZE, i[0] * SQUARE_SIZE,
                (i[1] + 1) * SQUARE_SIZE, (i[0] + 1) * SQUARE_SIZE,
                outline="red", width=4
            )
        self.draw_pieces()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()
