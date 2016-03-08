#!/usr/bin/env python
#

"""
// The do_turn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist.
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    reinforcements = Sequence(name='Send Reinforcements')
    invaded_check = Check(invaded_maybe)
    send_backup = Action(send_aid_to_invaded_planet)
    reinforcements.child_nodes = [invaded_check, send_backup]

    multi_plan = Sequence(name='Multi Attack')
    have_planets = Check(min_planets)
    multi_action = Action(multi_attack)

    multi_plan.child_nodes = [largest_fleet_check, have_planets, multi_action]

    mul_spread = Sequence(name='Multi Spread')
    have_planets = Check(min_planets)
    is_neutral = Check(if_neutral_planet_available)
    multi_spread_action = Action(multi_spread)

    mul_spread.child_nodes = [have_planets, is_neutral, multi_spread_action]

    strong_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    strongest_attack = Action(strong_attack)
    strong_plan.child_nodes = [largest_fleet_check, strongest_attack]

    finish_plan = Sequence(name='Finish Plan')
    largest_fleet_check = Check(have_largest_fleet)
    have_planets = Check(min_planets)
    finish_action = Action(barrage)
    finish_plan.child_nodes = [largest_fleet_check, have_planets, finish_action]

    pinpoint_plan = Sequence(name='Pinpoint')
    largest_fleet_check = Check(have_largest_fleet)
    have_planets = Check(min_planets)
    pinpoint_action = Action(pinpoint)
    pinpoint_plan.child_nodes = [largest_fleet_check, have_planets, pinpoint_action]

    root.child_nodes = [offensive_plan, spread_sequence, reinforcements, mul_spread, multi_plan, finish_plan, attack.copy()]

    logging.info('\n' + root.tree_to_string())
    return root


if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                behavior_tree.execute(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
