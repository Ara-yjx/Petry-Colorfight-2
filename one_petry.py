from colorfight import Colorfight
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

from petry_ai import ai_petry

game = Colorfight()
game.connect(room = 'public')
game.register(username = 'ONE', password = '00000000')

if not game.me:
    game.connect(room = 'public')
    game.register(username = 'ONE', password = '00000000')
    
    # This is the game loop
for i in range(10):
    game.update_turn()


    params = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cmd_list = ai_petry(game, params)
    
    result = game.send_cmd(cmd_list)
    print(result)

