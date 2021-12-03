import itertools as it
import numpy as np
from random import random

MIN_PHEROMONE = 0.01


def full_combinations(matrix, size):
    places = np.arange(size)
    places_combs = list()

    for combination in it.permutations(places):
        comb_arr = list(combination)

        places_combs.append(comb_arr)

    min_dist = float("inf")

    for i in range(len(places_combs)):
        places_combs[i].append(places_combs[i][0])

        cur_dist = 0

        for j in range(size):
            start_city = places_combs[i][j]
            end_city = places_combs[i][j + 1]

            cur_dist += matrix[start_city][end_city]

        if (cur_dist < min_dist):
            min_dist = cur_dist

            best_way = places_combs[i]

    return min_dist, best_way


# Ant algorythm
def calc_q(matrix, size):
    
    q = 0
    count = 0

    for i in range(size):
        for j in range(size):
            if (i != j):
                q += matrix[i][j]
                count += 1

    return q / count


def get_pheromones(size):

    min_phero = 1
    pheromones = [[min_phero for i in range(size)] for j in range(size)]

    return pheromones


def get_visibility(matrix, size):

    visibility = [[(1.0 / matrix[i][j] if (i != j) else 0) for j in range(size)] for i in range(size)]

    return visibility


def get_visited_places(route, ants):

    visited = [list() for _ in range(ants)]

    for ant in range(ants):
        visited[ant].append(route[ant])

    return visited


def calc_length(matrix, route):
    length = 0

    for way_len in range(1, len(route)):
        length += matrix[route[way_len - 1], route[way_len]]

    return length


def update_pheromones(matrix, places, visited, pheromones, q, k_evaporation):
    ants = places

    for i in range(places):
        for j in range(places):
            delta_pheromones = 0

            for ant in range(ants):
                length = calc_length(matrix, visited[ant])
                delta_pheromones += q / length

            pheromones[i][j] *= (1 - k_evaporation)
            pheromones[i][j] += delta_pheromones

            if (pheromones[i][j] < MIN_PHEROMONE):
                pheromones[i][j] = MIN_PHEROMONE

    return pheromones


def find_posibilyties(pheromones, visibility, visited, places, ant, alpha, beta):
    pk = [0] * places

    for place in range(places):
        if place not in visited[ant]:
            ant_place = visited[ant][-1]

            # Используется формула
            pk[place] = pow(pheromones[ant_place][place], alpha) * \
                pow(visibility[ant_place][place], beta)
        
        else:
            pk[place] = 0

    sum_pk = sum(pk)

    for place in range(places):
        pk[place] /= sum_pk  

    return pk


# Следующий город
#  0         pk[0]  pk[1]    pk[2]       pk[2]  1
#  |----------|------|--------|---x--------|----|
def choose_next_place_by_posibility(pk):
    posibility = random()
    choice = 0
    chosen_place = 0

    while ((choice < posibility) and (chosen_place < len(pk))):
        choice += pk[chosen_place]
        chosen_place += 1

    return chosen_place



def ant_algorythm(matrix, places, alpha, beta, k_evaporation, days):
    q = calc_q(matrix, places)

    best_way = []
    min_length = float("inf")

    pheromones = get_pheromones(places)
    visibility = get_visibility(matrix, places)

    ants = places

    for day in range(days):
        route = np.arange(places)

        visited = get_visited_places(route, ants)

        for ant in range(ants):
            while (len(visited[ant]) != ants):
                pk = find_posibilyties(pheromones, visibility, visited, places, ant, alpha, beta)  

                chosen_place = choose_next_place_by_posibility(pk)

                visited[ant].append(chosen_place - 1)
        
            visited[ant].append(visited[ant][0])

            # Длина текущего маршрута
            cur_length = calc_length(matrix, visited[ant]) 

            if (cur_length < min_length):
                min_length = cur_length
                best_way = visited[ant]

        # Обновить значения
        pheromones = update_pheromones(matrix, places, visited, pheromones, q, k_evaporation)

    return min_length, best_way
