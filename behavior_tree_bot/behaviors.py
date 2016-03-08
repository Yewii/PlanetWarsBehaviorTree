import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 5

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return


def spread_to_weakest_neutral_planet(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 2

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

def send_aid_to_invaded_planet(state):

    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    try:
        my_planet = next(my_planets)
        #target_planet = next(target_planets)
        while my_planet:

            if any(fleet.destination_planet == my_planet.ID for fleet in state.enemy_fleets()):
                if not any(fleet.destination_planet == my_planet.ID for fleet in state.my_fleets()):
                    for fleet in state.enemy_fleets():
                        if fleet.destination_planet == my_planet.ID:
                            if (my_planet.num_ships + (fleet.turns_remaining * my_planet.growth_rate)
                                    + (strongest_planet.num_ships/15+2) + 5 >= fleet.num_ships +
                                    (state.distance(strongest_planet.ID, my_planet.ID)-fleet.turns_remaining)
                                    * my_planet.growth_rate):
                                issue_order(state, strongest_planet.ID, my_planet.ID, strongest_planet.num_ships / 15 + 2)
                my_planet = next(my_planets)
                    #target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return


def multi_attack(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse = True))

    enemy_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        target_planet = next(target_planets)
        while True:
            cluster = []
            i = 0
            my_ships = 0

            while i < 6:
                cluster.append(next(my_planets))
                my_ships += cluster[0].num_ships/5 + 2
                i += 1

            dist = 0
            furthest_planet = None
            for planet in cluster:
                temp = state.distance(target_planet.ID, planet.ID)
                if temp > dist:
                    furthest_planet = planet
                    dist = temp

            required_ships = target_planet.num_ships + \
                state.distance(furthest_planet.ID, target_planet.ID) * target_planet.growth_rate + 2
            if my_ships > required_ships:
                for planet in cluster:
                    issue_order(state, planet.ID, target_planet.ID, (planet.num_ships/4 + 2))
                    return
            else:
               return
    except StopIteration:
        return


def multi_spread(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse = True))
    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    try:
        neutral_planet = next(target_planets)
        while True:
            cluster = []
            i = 0
            my_ships = 0

            while i < 10:
                cluster.append(next(my_planets))
                my_ships += cluster[0].num_ships/8 + 2
                i += 1
            required_neutral = neutral_planet.num_ships
            if my_ships > required_neutral:
                for planet in cluster:
                    issue_order(state, planet.ID, neutral_planet.ID, (planet.num_ships/8 + 2))
                    return
            else:
                return
    except StopIteration:
        return

def strong_attack(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 5

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

def barrage(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse = True))

    enemy_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    if len(state.enemy_planets()) > 3:
        return
    try:
        target_planet = next(target_planets)
        while True:
            cluster = []
            i = 0
            my_ships = 0

            while i < 9:
                cluster.append(next(my_planets))
                i += 1
            for planet in cluster:
                issue_order(state, planet.ID, target_planet.ID, planet.num_ships/2)
            target_planet = next(target_planets)
    except StopIteration:
        return

def pinpoint(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse = True))

    enemy_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    if len(state.enemy_fleets()) == 0:
        return
    enemy_fleet = state.enemy_fleets()
    target_planet = None
    target_size = 0
    for fleet in enemy_fleet:
        if state.planet[fleet.source_planet].num_ships > target_size:
            target_planet = state.planet[fleet.source_planet]
            target_size = target_planet.num_ships

    ID = enemy_fleet[0].source_planet
    target_planet = state.planets[ID]

    try:
        while True:
            cluster = []
            i = 0
            my_ships = 0

            while i < 6:
                cluster.append(next(my_planets))
                my_ships += cluster[0].num_ships/5 + 2
                i += 1

            dist = 0
            furthest_planet = None
            for planet in cluster:
                temp = state.distance(target_planet.ID, planet.ID)
                if temp > dist:
                    furthest_planet = planet
                    dist = temp

            required_ships = target_planet.num_ships + \
                state.distance(furthest_planet.ID, target_planet.ID) * target_planet.growth_rate + 2
            if my_ships > required_ships:
                for planet in cluster:
                    issue_order(state, planet.ID, target_planet.ID, (planet.num_ships/4 + 2))
                    return
            else:
               return
    except StopIteration:
        return