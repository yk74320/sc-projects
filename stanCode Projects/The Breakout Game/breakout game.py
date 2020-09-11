from graphic import Graphics
from campy.gui.events.timer import pause

FRAME_RATE = 1000/60

def main():
    all_score = []
    g = Graphics(700)
    g.intro()
    g.game_start = False
    while not g.game_start:
        pause(100)
    g.window.clear()
    g.loading()
    pause(1000)
    g.window.clear()
    game_round = 0
    g.game_start = True
    while g.game_start:
        g.game_start = False
        game_round += 1
        g.object_show()
        while g.life_check() == 0:
            pause(FRAME_RATE)
            if g.game_start:
                g.boundary_bump()
                g.ball_bump()
                g.gift_bump()
                g.object_move()
            else:
                g.ball_reset()
        g.window.clear()
        if g.life_check() == 1:
            g.lose()
        else:
            g.win()
        all_score += [g.score]
        g.final_score()
        if not g.game_start:
            break
        g.window.clear()
        g.full_reset()
    g.window.clear()
    g.high_score(all_score)


if __name__ == "__main__":
    main()