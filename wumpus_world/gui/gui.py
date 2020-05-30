from math import ceil

import pygame
from wumpus_world.gui.gui_logic import GuiLogic, Field, Action
from wumpus_world.main import qlearning, run


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
BOX_SIZE = WINDOW_WIDTH/4
WHITE = (255,255,255)
BLACK = (0,0,0)
BUTTON_X = 250
BUTTON_Y = 630
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

class Gui(GuiLogic):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Wumpus world')
        self.background_img = pygame.image.load("images/background.jpg").convert()
        self.agent_img = pygame.image.load("images/agent.png").convert_alpha()
        self.wumpus_img = pygame.image.load("images/wumpus.png").convert_alpha()
        self.gold_img = pygame.image.load("images/gold.png").convert_alpha()
        self.pit_img = pygame.image.load("images/pit.jpg").convert()
        self.display.fill(WHITE)
        self.clock = pygame.time.Clock()

    def draw_board(self):
        for x in range(4):
            for y in range(4):
                self.display.blit(self.background_img, (x * BOX_SIZE, y * BOX_SIZE))
                if self.board_state[x][y] == Field.AGENT:
                    self.display.blit(self.agent_img, (x * BOX_SIZE, y * BOX_SIZE))
                elif self.board_state[x][y] == Field.PIT:
                    self.display.blit(self.pit_img, (x * BOX_SIZE, y * BOX_SIZE))
                elif self.board_state[x][y] == Field.WUMPUS:
                    self.display.blit(self.wumpus_img, (x * BOX_SIZE, y * BOX_SIZE))
                elif self.board_state[x][y] == Field.GOLD:
                    self.display.blit(self.gold_img, (x * BOX_SIZE, y * BOX_SIZE))
        for x in range(1,4):
            pygame.draw.line(self.display, BLACK, (x*BOX_SIZE, 0), (x*BOX_SIZE, WINDOW_WIDTH))
        for y in range(1,4):
            pygame.draw.line(self.display, BLACK, (0, y*BOX_SIZE), (WINDOW_WIDTH, y*BOX_SIZE))
        pygame.display.update()

    def create_button(self, message, x, y, w, h, color):
        def text_objects(text, font):
            textSurface = font.render(text, True, BLACK)
            return textSurface, textSurface.get_rect()


        pygame.draw.rect(self.display, color, (x, y, w, h))
        smallText = pygame.font.SysFont("Arial",20)
        textSurf, textRect = text_objects(message, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.display.blit(textSurf, textRect)

    def reset(self):
        self.learned = False
        self.finished = False
        self.step_number = 0
        self.reset_board()

    def run(self):
        running = True
        self.reset()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x_click, y_click = event.pos
                        if y_click < 600:
                            x_click = ceil(x_click/BOX_SIZE) - 1
                            y_click = ceil(y_click/BOX_SIZE) - 1
                            if not self.learned:
                                self.update_field(x_click, y_click)
                        else:
                            if BUTTON_X < x_click < BUTTON_X + BUTTON_WIDTH and \
                               BUTTON_Y < y_click < BUTTON_Y + BUTTON_HEIGHT:
                                if not self.learned:
                                    self.reward_array = self.convert_to_reward_array()
                                    self.Q = qlearning(self.reward_array)
                                    self.learned = True
                                    self.step_list = run(self.reward_array, self.Q)
                                elif not self.finished:
                                    if self.step_number < len(self.step_list):
                                        agent_x, agent_y = self.step_list[self.step_number][0], \
                                                           self.step_list[self.step_number][1]
                                        self.update_agent(agent_x, agent_y)
                                        self.step_number += 1
                                    else:
                                        self.finished = True
                                else:
                                    self.reset()

            self.draw_board()
            if not self.learned:
                self.create_button("Learn", BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, (0,255, 0))
            elif not self.finished:
                self.create_button("Step", BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, (128, 255, 0))
            else:
                self.create_button("Reset", BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, (255, 0, 0))
            pygame.display.update()
            self.clock.tick(10)

if __name__ == "__main__":
    Gui().run()