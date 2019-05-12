from colorfight import Colorfight
import random
import math
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS
from colorfight.constants import GAME_WIDTH, GAME_HEIGHT


def ai_petry(game, param):
    # debug: 10 steps

    options = []
    cmd_list = []

    """
    # Resolve param
    _base_atk = param[0]
    _cost = param[1]
    _natural_gold = param[2]
    _natural_energy = param[3]
    _centerity = param[4]
    _close_friend = param[5]
    _far_friend = param[6]
    _close_enemy = param[7] # not now
    _far_enemy = param[8] # not now
    """


    me = game.me
    gw = GAME_WIDTH
    gh = GAME_HEIGHT


    # home
    for cell in game.me.cells.values():
        if cell.building.is_home:
            game.home_cell = cell
            break

    cmd_list += first(game)

    for cell_w in range(gw):
        for cell_h in range(gh):
            cell = game.game_map[cell_w, cell_h]

            # Features
            cell.centerity = abs(cell.position.x - gw/2) + abs(cell.position.y - gh/2)
            cell.close_friend = 0
            cell.far_friend = 0
            # dcx + dcy <= 3
            for dcx in range(-3, 4):
                cx = cell_w + dcx
                for dcy in range(-abs(dcx), abs(dcx)):
                    cy = cell_h + dcy
                    if 0 <= cx < gw and 0 <= cy < gh and game.game_map[cx, cy].owner == game.me.uid:
                        cell.far_friend += 1
                    # elif: far_enemy
            for adjacent in cell.position.get_surrounding_cardinals():
                if game.game_map[adjacent].owner == game.me.uid:
                    cell.close_friend += 1

            # If unoccupied or enemy's, atk
            if cell.owner != me.uid:
                if cell.close_friend > 0: # if acjacent to me
                    reward = atk_reward(cell, game, param)
                    cost = (cell.attack_cost, 0)
                    cmd_list.append((game.attack(cell.position, cell.attack_cost), reward, cost))
                    # print(cmd_list[-1])

            # If mine, build
            else:
                cmd, reward, cost = build_reward(cell, game, param)
                if(cmd):
                    cmd_list.append((cmd, reward, cost))


    # prioritize cmd
    cmd_list = sorted(cmd_list, key=lambda x: x[1]) # sort by reward
    cmd = []
    for i in cmd_list:
        cmd.append(i[0])
    # print(cmd)
    return cmd




def atk_reward(c, game, param):
    # Resolve param
    _base_atk = param[0] # fixed: 1
    _cost = param[1]
    _natural_gold = param[2]
    _natural_energy = param[3]
    _centerity = param[4]
    _close_friend = param[5]
    _far_friend = param[6]
    _atk_priority = param[7]
    _atk_time = param[8]

    reward = (_base_atk + \
    c.attack_cost * _cost + \
    c.natural_gold * _natural_gold + \
    c.natural_energy * _natural_energy + \
    c.centerity * _centerity + \
    c.close_friend * _close_friend + \
    c.far_friend * _far_friend) \
    * shift_atan(game.turn, _atk_time) * _atk_priority
    
    return reward
    


def build_reward(c, game, param):

    _build_gold = param[9]
    _build_energy = param[10]
    _build_close_friend = param[11]
    _build_far_friend = param[12]
    _build_time = param[13]
    _build_priority = param[14]

    # If no building
    if(c.building.name == 'empty'):
        gold_reward = c.natural_gold * _build_gold
        energy_reward = c.natural_energy * _build_energy
        # fortress_reward = _build_fortress
        # Don't build fortress
        if gold_reward > energy_reward: 
            cmd = game.build(c.position, BLD_GOLD_MINE)
            build_reward = gold_reward
            cost = (100, 0)
        else:
            cmd = game.build(c.position, BLD_ENERGY_WELL)
            build_reward = energy_reward
            cost = (100, 0)

    elif(c.building.name == 'home'):
        return None, 0, 0

    # Upgrade
    else:
        build_reward = 1
        cmd = game.upgrade(c.position)
        cost = (c.building.upgrade_energy, c.building.upgrade_gold)

    reward = build_reward * ( \
    c.close_friend * _build_close_friend + \
    c.far_friend * _build_far_friend) * \
    shift_atan(game.turn, _build_time) * _build_priority

    
    return cmd, reward, cost


def first(game):
    cmd_list = []
    if game.turn > 100 and game.home_cell.building.can_upgrade:
        cmd_list.append((game.upgrade(game.home_cell.position), math.inf, \
        game.home_cell.building.upgrade_energy, game.home_cell.building.upgrade_gold))
    
    """
    for dcx in range(-3, 4):
        cx = game.home_cell.position.x + dcx
        for dcy in range(-abs(dcx), abs(dcx)):
            cy = game.home_cell.position.y + dcy
            # Enemy!
            if 0 <= cx < GAME_WIDTH and 0 <= cy < GAME_HEIGHT and game.game_map[cx, cy].owner != game.me.uid and game.game_map[cx, cy].owner != 0:
                pass
    """
    return cmd_list


def shift_atan(time, midpoint):
    return (math.pi / 2 + math.atan(time - midpoint)) 