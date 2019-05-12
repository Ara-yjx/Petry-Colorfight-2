from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

from ai1 import ai1
from petry_ai import ai_petry


gamers = []
for gamer_id in range(8):
    
    # register
    game = Colorfight()
    game.connect(room = 'public')
    game.register(username = 'AI_' + str(gamer_id), password = '00000000')
    
    # param

    param = [1]
    for i in range(14):
        param.append(random.random() * 100 - 50)
    with open("param.txt","a") as f:
        f.write(str(gamer_id))
        f.write(' ')
        f.write(str(param))
        f.write('\n')
        f.close()

    game.param = param
    gamers.append(game)

while True:
    for game in gamers:
        game.update_turn()

        cmd_list = ai_petry(game, game.param)
        
        result = game.send_cmd(cmd_list)
        print(result)

