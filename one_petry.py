from colorfight import Colorfight
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

from petry_ai import ai_petry

game = Colorfight()
game.connect(room = 'final')
game.register(username = 'PetryAI', password = '00000000')

if not game.me:
    game.connect(room = 'final')
    game.register(username = 'PetryAI', password = '00000000')
    
    # This is the game loop
while True:
    game.update_turn()


    params = [1, -18.53341319688236, -0.8219475924979506, 2.2963243078751745, -2.12995591256858, -5.172858499022022, 16.968696086066522, -1.4114154156601832, -1.0770153231601682, -12.082107075648503, -2.1421765673156354, 18.795280713849472, 14.66617744870164, -0.39348099194405034, 4.819134378406117, 17.67588494142681, -31.470563592117514]
    cmd_list = ai_petry(game, params)
    
    result = game.send_cmd(cmd_list)
    print(result)

