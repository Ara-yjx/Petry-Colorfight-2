from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

# Create a Colorfight Instance. This will be the object that you interact
# with.
gamers = []
for gamer_id in range(8):
    
    game = Colorfight()
    game.connect(room = 'public')
    game.register(username = 'AI_' + gamer_id, password = '00000000')
    gamers.append(game)

    # This is the game loop
while True:

    for game in gamers:
        game.update_turn()

        cmd_list = []
        my_attack_list = []

        if game.me == None:
            continue

        me = game.me
        my_energy = me.energy

        for cell in game.me.cells.values():
            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                # Get the MapCell object of that position
                c = game.game_map[pos]
                
                # Attack if the cost is less than what I have, and the owner
                # is not mine, and I have not attacked it in this round already
                # We also try to keep our cell number under 100 to avoid tax
                if c.attack_cost < my_energy and c.owner != game.uid \
                        and c.position not in my_attack_list:
                    # Add the attack command in the command list
                    # Subtract the attack cost manually so I can keep track
                    # of the energy I have.
                    # Add the position to the attack list so I won't attack
                    # the same cell
                    cmd_list.append(game.attack(pos, c.attack_cost))
                    print("We are attacking ({}, {}) with {} energy".format(pos.x, pos.y, c.attack_cost))
                    my_energy -= c.attack_cost
                    my_attack_list.append(c.position)

            # If we can upgrade the building, upgrade it.
            # Notice can_update only checks for upper bound. You need to check
            # tech_level by yourself. 
            if cell.building.can_upgrade and \
                    (cell.building.is_home or cell.building.level < me.tech_level) and \
                    cell.building.upgrade_gold < me.gold and \
                    cell.building.upgrade_energy < my_energy:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgraded ({}, {})".format(cell.position.x, cell.position.y))
                me.gold   -= cell.building.upgrade_gold
                my_energy -= cell.building.upgrade_energy
                
            # Build a random building if we have enough gold
            if cell.owner == me.uid and cell.building.is_empty and me.gold >= 100:
                building = random.choice([BLD_FORTRESS, BLD_GOLD_MINE, BLD_ENERGY_WELL])
                cmd_list.append(game.build(cell.position, building))
                print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
                me.gold -= 100

        
        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)
