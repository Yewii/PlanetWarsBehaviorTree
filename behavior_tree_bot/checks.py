
def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def invaded_maybe(state):
    
    try:
        my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
        my_planet = next(my_planets)

        while my_planet:
            if any(fleet.destination_planet == my_planet.ID for fleet in state.enemy_fleets()):
                return True
            my_planet = next(my_planets)
    
    except StopIteration:
        return False

def min_planets(state):
    sum = 0
    for planet in state.my_planets():
        sum += 1
    return sum > 10

def finish_state(state):
    return len(state.enemy_planets()) <= 3



