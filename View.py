import pygame as pg

from EventManager import *
from Model import GameEngine
import Const


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.background.fill(Const.BACKGROUND_COLOR)

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pass

    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to start ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_play(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw players
        for player in self.model.players:
            center = list(map(int, player.position))
            pg.draw.circle(self.screen, Const.PLAYER_COLOR[player.player_id], center, Const.PLAYER_RADIUS)
            if player.state == 'attack':
                pg.draw.circle(self.screen, pg.Color('white'), center, Const.PLAYER_RADIUS, width = 5)

        # show game timer
        font = pg.font.Font(None, 24)
        text_surface = font.render(f"Timer: {int(self.model.timer/Const.FPS) + 1}", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 8, Const.ARENA_SIZE[1] / 16)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        # show state-exchange time left
        font = pg.font.Font(None, 24)
        text_surface = font.render(f"Exchange time left: {int(self.model.timer/Const.FPS) % Const.ATTACK_EXCHANGE_SEC + 1}", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 16)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))
        
        # show player states
        font = pg.font.Font(None, 24)
        text_surface = font.render(f"Attacker: Player {self.model.attacker}", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 8 * 7, Const.ARENA_SIZE[1] / 16)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_stop(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # show STOP
        font = pg.font.Font(None, 72)
        text_surface = font.render("STOP", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        font = pg.font.Font(None, 48)
        text_surface = font.render("Press [space] to continue ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 8 * 5)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        # show game timer
        font = pg.font.Font(None, 24)
        text_surface = font.render(f"Timer: {int(self.model.timer/Const.FPS) + 1}", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 8, Const.ARENA_SIZE[1] / 16)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_endgame(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # show winner
        font = pg.font.Font(None, 72)
        try:
            if self.model.winner_id == -1:
                raise 
            winner = f'Player {self.model.winner_id}'
            text_surface = font.render(f"{winner} wins!", 1, Const.PLAYER_COLOR[self.model.winner_id])
        except:
            text_surface = font.render("No one wins...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()
