import copy
import random
import socket
import sys
import threading
import time

import pygame
from constants_tic import *
import numpy as np

# PYGAME STARTUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic tac toe")
screen.fill(BG_Colour)
font = pygame.font.Font(None, 36)


class Board():
    def __init__(self):
        self.pause = None
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.mark_sqrs = 0
        #self.pauses()

    def final_state(self, show=False):

        # vertical win
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = (0, 255, 0) if self.squares[0][col] == 2 else (0, 255, 0)
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    ePos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, ePos, LINE_WIDTH)
                    if self.squares[0][col] == 1.0:
                        player_text = "X's Wins"
                        text = font.render(player_text, True, (255, 255, 255))
                        text_rect = text.get_rect()
                        text_rect.center = (WIDTH // 2, HEIGHT - 20)
                        pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                        screen.blit(text, text_rect)
                        self.pauses()
                    elif self.squares[0][col] == 2.0:
                        player_text = "0's Wins"
                        text = font.render(player_text, True, (255, 255, 255))
                        text_rect = text.get_rect()
                        text_rect.center = (WIDTH // 2, HEIGHT - 20)
                        pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                        screen.blit(text, text_rect)
                        self.pauses()

                return self.squares[0][col]

        # horizontal win
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = (0, 255, 0) if self.squares[row][0] == 2 else (0, 255, 0)
                    iPos = (20, row * SQSIZE + SQSIZE // 2)

                    ePos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, ePos, LINE_WIDTH)
                    if self.squares[row][0] == 1.0:
                        player_text = "X's Wins"
                        text = font.render(player_text, True, (255, 255, 255))
                        text_rect = text.get_rect()
                        text_rect.center = (WIDTH // 2, HEIGHT - 20)
                        pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                        screen.blit(text, text_rect)
                        self.pauses()
                    if self.squares[row][0] == 2.0:
                        player_text = "0's Wins"
                        text = font.render(player_text, True, (255, 255, 255))
                        text_rect = text.get_rect()
                        text_rect.center = (WIDTH // 2, HEIGHT - 20)
                        pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                        screen.blit(text, text_rect)
                        self.pauses()
                return self.squares[row][0]

        # diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = (0, 255, 0) if self.squares[1][1] == 2 else (0, 255, 0)
                iPos = (20, 20)

                ePos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, ePos, LINE_WIDTH)
                if self.squares[1][1] == 1.0:
                    player_text = "X's Wins"
                    text = font.render(player_text, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.center = (WIDTH // 2, HEIGHT - 20)
                    pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                    screen.blit(text, text_rect)
                    self.pauses()

                elif self.squares[1][1] == 2.0:
                    player_text = "0's Wins"
                    text = font.render(player_text, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.center = (WIDTH // 2, HEIGHT - 20)
                    pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                    screen.blit(text, text_rect)
                    self.pauses()
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = (0, 255, 0) if self.squares[1][1] == 2 else (0, 255, 0)
                iPos = (20, HEIGHT - 20)

                ePos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, ePos, LINE_WIDTH)
                if self.squares[1][1] == 1.0:
                    player_text = "X's Wins"
                    text = font.render(player_text, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.center = (WIDTH // 2, HEIGHT - 20)
                    pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                    screen.blit(text, text_rect)
                    self.pauses()

                elif self.squares[1][1] == 2.0:
                    player_text = "0's Wins"
                    text = font.render(player_text, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.center = (WIDTH // 2, HEIGHT - 20)
                    pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
                    screen.blit(text, text_rect)
                    self.pauses()
            return self.squares[1][1]

        # NO win
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.mark_sqrs += 1

    def get_empty_squares(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sq(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def empty_sq(self, row, col):
        #print(self.squares)
        return self.squares[row][col] == 0

    def isfull(self):
        if self.mark_sqrs == 9:
            player_text = "TIE"
            text = font.render(player_text, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT - 20)
            pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
            screen.blit(text, text_rect)
            self.pauses()
            return True
        else:
            return False

    def isempty(self):
        return self.mark_sqrs == 0

    def pauses(self):
        self.pause = True

    def un_pause(self):
        self.pause = False


class AI():
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_squares()
        print(empty_sqrs)
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]

    def minimax(self, board, maximing):
        # terminal case
        case = board.final_state()
        # player 1 wins

        if case == 1:
            return 1, None

        # player 2 wins

        if case == 2:
            return -1, None

        # draw

        elif board.isfull():
            return 0, None

        if maximing:
            max_eval = -1000
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximing:
            min_eval = 1000
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def evals(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
        else:
            eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square {move} with an eval of {eval}')

        return move


class Game:
    def __init__(self):
        self.player1_draw = None
        self.client = None
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.runing = True
        self.show_lines()
        self.draw_player_turn()

    def draw_player_turn(self):
        if self.gamemode != "multiplayer":
            player_text = "X's Turn" if self.player == 1 else "O's Turn"
            text = font.render(player_text, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT - 20)
            pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
            screen.blit(text, text_rect)

    def make_move(self, row, col):
        if not self.board.pause:
            self.board.mark_square(row, col, self.player)
            self.draw_fig(row, col)
            if self.gamemode == 'multiplayer':
                self.client.send(str(row).encode())
                self.client.send(str(col).encode())
            self.next_turn()

    def show_lines(self):
        screen.fill(BG_Colour)
        # vertical
        pygame.draw.line(screen, LINS, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINS, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINS, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINS, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def next_turn(self):
        if self.gamemode !=  'multiplayer':
            self.player = self.player % 2 + 1
            self.draw_player_turn()

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # decending line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLUR, start_desc, end_desc, CROSS_WIDTH)

            # acending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLUR, start_asc, end_asc, CROSS_WIDTH)
        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLUR, center, RADIUS, CIRC_WIDTH)

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def reset(self):
        self.__init__()

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def multi_turn(self, end=False):
        if not end:
            player_text = "Your turn"
            text = font.render(player_text, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT - 20)
            pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
            screen.blit(text, text_rect)
        else:
            player_text = "Opponent Turn"
            text = font.render(player_text, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT - 20)
            pygame.draw.rect(screen, BG_Colour, (0, HEIGHT - 40, WIDTH, 40))
            screen.blit(text, text_rect)

    def multiplayer(self):
        self.gamemode = 'multiplayer'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('192.168.1.2', 5240))

        # Send the nickname to the server
        nick = input("Enter your name: ")
        self.client.send(nick.encode('utf-16'))

        # Receive the name of the match from the server
        name = self.client.recv(1024).decode('utf-16')

        print(name)

        x_or_o = self.client.recv(1024).decode('utf-16')
        print(x_or_o)

        if x_or_o == 'X':
            self.board.pauses()
            self.player = 1

        else:
            self.board.pauses()
            self.player = 2
        self.player1_draw = False

        while True:
            my_turn = self.client.recv(1024).decode('utf-16')
            print(my_turn)
            if my_turn == '1' and self.player == 1:
                if self.player1_draw is not True:
                    self.board.un_pause()
                    self.multi_turn()
                    print(str(self.player) + "1")
                    print('ok')
                    self.player1_draw = True
                    ack = self.client.recv(1024).decode('utf-16')
                    print(ack)
                    self.multi_turn(end=True)
                    self.board.pauses()
                else:
                    self.board.un_pause()
                    self.multi_turn()
                    print(str(self.player) + "1u")
                    time.sleep(0.5)
                    row2 = self.client.recv(1024).decode('utf-16')
                    time.sleep(0.5)
                    col2 = self.client.recv(1024).decode('utf-16')

                    print("Values of a and b are:")
                    print(row2, col2, type(row2), type(col2))
                    row2, col2 = int(row2), int(col2)
                    self.player = 2
                    if self.board.empty_sq(row2, col2):
                        self.draw_fig(row=row2, col=col2)
                        self.board.mark_square(row2, col2, self.player)
                    self.player = 1
                    ack = self.client.recv(1024).decode('utf-16')
                    print(ack)
                    self.multi_turn(end=True)
                    self.board.final_state(show=True)
                    self.board.pauses()
                    
            elif my_turn == '2' and self.player == 2:
                print('success')
                self.board.un_pause()
                self.multi_turn()
                print(str(self.player) + "2")
                row1 = self.client.recv(1024).decode('utf-16')
                col1 = self.client.recv(1024).decode('utf-16')
                self.player = 1
                if self.board.empty_sq(int(row1), int(col1)):
                    self.draw_fig(row=int(row1), col=int(col1))
                    self.board.mark_square(int(row1), int(col1), self.player)
                self.player = 2
                ack = self.client.recv(1024).decode('utf-16')
                print(ack)
                self.multi_turn(end=True)
                self.board.final_state(show=True)
                self.board.pauses()


def main():
    game = Game()
    board = game.board
    ai = game.ai
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_gamemode()

                elif event.key == pygame.K_0:
                    ai.level = 0

                elif event.key == pygame.K_1:
                    ai.level = 1

                elif event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                elif event.key == pygame.K_m:
                    multiplayer_thread = threading.Thread(target=game.multiplayer)
                    multiplayer_thread.start()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sq(row, col) and game.runing:
                    game.make_move(row, col)

                    if game.isover():
                        game.runing = False

        if game.gamemode == 'ai' and game.player == ai.player and game.runing and game.gamemode != 'multiplayer':
            pygame.display.update()

            row, col = ai.evals(main_board=board)
            game.make_move(row, col)

            if game.isover():
                game.runing = False

            if game.gamemode == 'multiplayer':
                break

        pygame.display.update()


if __name__ == '__main__':
    main()
