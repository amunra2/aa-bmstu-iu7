from copy import *
from random import *
import itertools
from time import process_time
from numpy import arange, linspace

matrix_1 = [[-1, 6, 5, 5, 6, 9, 6, 5, 6, 8],
            [6, -1, 7, 9, 5, 8, 8, 8, 7, 7],
            [5, 7, -1, 5, 5, 6, 6, 8, 6, 9],
            [5, 9, 5, -1, 5, 8, 9, 6, 7, 8],
            [6, 5, 5, 5, -1, 8, 5, 7, 9, 7],
            [9, 8, 6, 8, 8, -1, 9, 7, 8, 9],
            [6, 8, 6, 9, 5, 9, -1, 7, 7, 5],
            [5, 8, 8, 6, 7, 7, 7, -1, 8, 8],
            [6, 7, 6, 7, 9, 8, 7, 8, -1, 9],
            [8, 7, 9, 8, 7, 9, 5, 8, 9, -1]]

matrix_2 = [[-1, 7, 8, 5, 6, 9, 7, 6], 
            [7, -1, 8, 8, 7, 8, 7, 8], 
            [8, 8, -1, 6, 7, 8, 8, 9], 
            [5, 8, 6, -1, 9, 6, 8, 9],
            [6, 7, 7, 9, -1, 8, 7, 6], 
            [9, 8, 8, 6, 8, -1, 5, 8], 
            [7, 7, 8, 8, 7, 5, -1, 7], 
            [6, 8, 9, 9, 6, 8, 7, -1]]

matrix_3 = [[-1, 5, 8, 6, 8, 8, 6, 6, 6, 6], 
            [5, -1, 8, 5, 7, 7, 9, 9, 7, 7], 
            [8, 8, -1, 9, 6, 5, 7, 5, 5, 6], 
            [6, 5, 9, -1, 8, 5, 5, 6, 9, 9], 
            [8, 7, 6, 8, -1, 6, 7, 8, 6, 8],
            [8, 7, 5, 5, 6, -1, 9, 8, 6, 6], 
            [6, 9, 7, 5, 7, 9, -1, 6, 5, 7], 
            [6, 9, 5, 6, 8, 8, 6, -1, 9, 8], 
            [6, 7, 5, 9, 6, 6, 5, 9, -1, 9], 
            [6, 7, 6, 9, 8, 6, 7, 8, 9, -1]]


def calculate_q(matrix, cities):
    q = 0
    count = 0

    for i in range(cities):
        for j in range(cities):
            if i != j:
                q += matrix[i][j]
                count += 1
    
    return q / count


def calculate_lk(matrix, visited_cities):
    lk = 0

    for l in range(1, len(visited_cities)):
        i = visited_cities[l-1]
        j = visited_cities[l]
        lk += matrix[i][j]

    return lk


def ant_search(matrix, cities, alpha, beta, evaporation_coef, days_max):
    pheromones = [[1 for _ in range(cities)] for _ in range(cities)] # tau
    visibility = [[1.0 / matrix[i][j] for j in range(cities)] for i in range(cities)] # eta

    pheromone_min = 0.01
    ants = cities
    Q = calculate_q(matrix, cities)
    min_distance = float("inf")

    # Цикл по всем дням
    for day in range(days_max):
        # Задаем список городов для текущего дня
        curr_route = list(range(cities))
        shuffle(curr_route)

        # Создаем массив посещенных городов для муравьев
        visited_cities = [0] * ants
        
        # Расставляем муравьев по уникальным городам
        for i in range(ants):
            visited_cities[i] = []
            visited_cities[i].append(curr_route[i])

        # Цикл по всем муравьям
        for k in range(ants):
            # Построение маршрута для текущего муравья
            while len(visited_cities[k]) != ants:
                Pk = [0] * cities
                # Определение вероятность перехода муравья из текущего города в непосещенные города
                for city in range(cities):
                    if city not in visited_cities[k]:
                        ant_curr_city = visited_cities[k][-1]
                        Pk[city] = pow(pheromones[ant_curr_city][city], alpha) *\
                                   pow(visibility[ant_curr_city][city], beta)
                    else:
                        Pk[city] = 0

                sum_Pk = sum(Pk)

                for city in range(cities):
                    Pk[city] /= sum_Pk

                # Выбор следующего города
                coin = random()
                choice, i = 0, 0

                while choice < coin and (i < len(Pk)):
                    choice += Pk[i]
                    i += 1
                
                visited_cities[k].append(i - 1)
            
            visited_cities[k].append(visited_cities[k][0])

            # Подсчет длины текущего маршрута
            Lk = calculate_lk(matrix, visited_cities[k])

            if Lk < min_distance:
                min_distance = Lk
                best_route = visited_cities[k]
        
        # Цикл по всем ребрам графа для обновления следов феромона
        for i in range(cities):
            for j in range(cities):
                # Нахождение количества откладываемого феромона всеми муравьями
                delta_pheromones = 0

                for k in range(ants):
                    Lk = calculate_lk(matrix, visited_cities[k])
                    delta_pheromones += Q / Lk

                # Обновление следов феромонов
                pheromones[i][j] *= (1 - evaporation_coef)
                pheromones[i][j] += delta_pheromones

                if pheromones[i][j] < pheromone_min:
                    pheromones[i][j] = pheromone_min

    return min_distance, best_route


def full_search(matrix, cities):
    cities_array = list(range(cities))
    cities_permutations = list()

    for subset in itertools.permutations(cities_array):
        subset = list(subset)
        cities_permutations.append(subset)

    min_distance = float("inf")

    for i in range(len(cities_permutations)):
        cities_permutations[i].append(cities_permutations[i][0])
        cur_distance = 0
    
        for j in range(cities): 
            first_city = cities_permutations[i][j]
            second_city = cities_permutations[i][j + 1]
            cur_distance += matrix[first_city][second_city]

        if cur_distance < min_distance: 
            min_distance = cur_distance 
            best_route = cities_permutations[i]
    
    return min_distance, best_route


def time_analysis():
    file = open('time.txt', 'w')

    for alpha in range(0, 10):
        beta = 10 - alpha

        for evaporation in linspace(0.1, 0.9, 9):
            for days_max in range(10, 100, 10):
                start = process_time()
                ant_search(matrix_2, 8, alpha, beta, evaporation, days_max)
                end = process_time()
                string = "Alpha: " + str(alpha) + "| Beta: " + str(beta) + "| Rho: " + str(evaporation) \
                    + "| days: " + str(days_max) + "| Time: " + str(end - start) + "\n"

                file.write(string)

    file.close()


def main():
    time_analysis()

    print("Full search:")
    result = full_search(matrix_2, 8)
    print(result)

    print("Ant search:")
    result = ant_search(matrix_2, 8, 4, 6, 0.6, 20)
    print(result)

if __name__ == '__main__':
    main()