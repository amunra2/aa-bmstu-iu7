# Libs
from time import process_time
from random import randint, random
import matplotlib.pyplot as plt 

import itertools as it

import numpy as np

from os import system

from numpy.lib.function_base import append
from numpy.matrixlib import matrix



# Text
MSG = "\n\n      Задача коммивояжера \n\n \
    1. Полный перебор \n \
    2. Муравьиный алгоритм \n \
    3. Все алгоритмы \n\n \
    4. Параметризация \n \
    5. Замерить время \n\n \
    6. Обновить данные \n \
    7. Распечатать матрицу \n\n \
    0. Выход \n\n \
    \
    Выбор: \
    "

# Define
EXIT = 0
ALL_COMB = 1
ANT_ALG = 2
ALG_ALL = 3
PARAMETRIC = 4
TEST =  5
UPDATE_DATA = 6
SHOW_DATA = 7

ODD = 1
EVEN = 2

TIMES = 100
TO_MILISECONDS = 1000

MIN_PHEROMONE = 0.01


# Functions

def generate_matrix(size, rand_start, rand_end):

    matrix = np.zeros((size, size), dtype = int)

    for i in range(size):
        for j in range(size):

            if (i == j):
                num = 0
            else:
                num = randint(rand_start, rand_end)

            matrix[i][j] = num
            matrix[j][i] = num

    return matrix


def generate_matrix_file(file_name, size, rand_start, rand_end):

    matrix = generate_matrix(size, rand_start, rand_end)

    file = open("data/" + file_name, "w")

    for i in range(size):

        string = ""

        for j in range(size):

            string += str(matrix[i][j])
            string += " "

        string += "\n"

        file.write(string)

    file.close()

    return "\nSuccess: %s generated\n" % (file_name)


def read_file_matrix(file_name):

    file = open("data/" + file_name, "r")
    size = len(file.readline().split()) # определение размера матрицы
    file.seek(0)

    matrix = np.zeros((size, size), dtype = int)
    
    i = 0

    for line in file.readlines():
        j = 0

        for num in line.split():
            matrix[i][j] = int(num)
            j += 1

        i += 1

    file.close()

    return matrix


def list_files():
    system("ls \data > files.txt") # linux works

    f_files = open("files.txt", "r")

    files = f_files.read().split()

    f_files.close()


    print("\n\nДоступные файлы: ", len(files), " штук", )

    for i in range(len(files)):
        print("%d. %s" % (i + 1, files[i]))

    return files


def update_file():
    option = int(input("Добавить новый файл? (1 - да, 2 - нет): "))

    if (option == 1):
        file_name = input("\nВведите имя файла: ")

        size = int(input("\nВведите размер матрицы: "))

        rand_start = int(input("\nВведите начальное число рандома: "))
        rand_end = int(input("\nВведите конечное число рандома: "))

        print(generate_matrix_file(file_name, size, rand_start, rand_end))

    elif (option == 2):
        files = list_files()

        num_file = int(input("\nВыберите файл: ")) - 1

        size = int(input("\nВведите размер матрицы: "))

        rand_start = int(input("\nВведите начальное число рандома: "))
        rand_end = int(input("\nВведите конечное число рандома: "))

        print(generate_matrix_file(files[num_file], size, rand_start, rand_end))

    else:
        print("\nОшибка: Неверно выбран пункт")
            

    print("\n\nУспешно обновлен список файлов\n")


def print_matrix():
    files = list_files()

    num_file = int(input("\nВыберите файл: ")) - 1

    matrix = read_file_matrix(files[num_file])

    print("\n")

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):

            print("%4d" % (matrix[i][j]), end = "")

        print()


def read_matrix():
    files = list_files()

    num_file = int(input("\nВыберите файл: ")) - 1

    matrix = read_file_matrix(files[num_file])

    return matrix


def full_combinations(matrix, size):
    cities = np.arange(size)
    cities_combs = list()

    for combination in it.permutations(cities):
        comb_arr = list(combination)

        cities_combs.append(comb_arr)

    min_dist = float("inf")

    for i in range(len(cities_combs)):
        cities_combs[i].append(cities_combs[i][0])

        cur_dist = 0

        for j in range(size):
            start_city = cities_combs[i][j]
            end_city = cities_combs[i][j + 1]

            cur_dist += matrix[start_city][end_city]

        if (cur_dist < min_dist):
            min_dist = cur_dist

            best_way = cities_combs[i]

    return min_dist, best_way
    

def parse_full_combinations():

    matrix = read_matrix()
    size = len(matrix)

    result = full_combinations(matrix, size)

    print("\n\nМинимальная сумма пути = ", result[0], 
            "\nПуть: ", result[1])


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
                pk = [0] * places

                for place in range(places):
                    if place not in visited[ant]:
                        ant_place = visited[ant][-1]

                        pk[place] = pow(pheromones[ant_place][place], alpha) * \
                            pow(visibility[ant_place][place], beta)
                    
                    else:
                        pk[place] = 0

                sum_pk = sum(pk)

                for place in range(places):
                    pk[place] /= sum_pk    

                # Следующий город

                #  0         pk[0]  pk[1]    pk[2]       pk[2]  1
                #  |----------|------|--------|---x--------|----|
                posibility = random()
                choice = 0
                chosen_place = 0

                while ((choice < posibility) and (chosen_place < len(pk))):
                    choice += pk[chosen_place]
                    chosen_place += 1

                visited[ant].append(chosen_place - 1)
        
            visited[ant].append(visited[ant][0])

            # Длина текущего маршрута
            cur_length = calc_length(matrix, visited[ant]) 

            if (cur_length < min_length):
                min_length = cur_length
                best_way = visited[ant]

        # Обновить значения
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

    return min_length, best_way


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
        # shuffle(curr_route)

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


def read_koefs():
    alpha = float(input("\n\nВведите коэффициент alpha: " ))
    beta = float(input("\nВведите коэффициент beta: " ))
    k_evaporation = float(input("\nВведите коэффициент evaporation: " ))
    days = int(input("\nВведите кол-во дней: " ))
    
    return alpha, beta, k_evaporation, days


def parse_ant_alg():

    matrix = read_matrix()
    size = len(matrix)

    alpha, beta, k_evaporation, days = read_koefs()

    result = ant_algorythm(matrix, size, alpha, beta, k_evaporation, days)

    print("\n\n1. Минимальная сумма пути = ", result[0], 
            "\nПуть: ", result[1])

    result = ant_search(matrix, size, alpha, beta, k_evaporation, days)

    print("\n\n2. Минимальная сумма пути = ", result[0], 
            "\nПуть: ", result[1])


def parse_all():

    matrix = read_matrix()
    size = len(matrix)

    alpha, beta, k_evaporation, days = read_koefs()

    result = full_combinations(matrix, size)

    print("\n\nАлгоритм полного перебора \
            \n\tМинимальная длина пути = ", result[0], 
            "\n\tПуть: ", result[1])

    result = ant_algorythm(matrix, size, alpha, beta, k_evaporation, days)

    print("\n\nМуравьиный алгоритм \
            \n\tМинимальная длина пути = ", result[0], 
            "\n\tПуть: ", result[1])



def time_test():

    size_start = int(input("\n\nВведите начальный размер матрицы: "))
    size_end = int(input("Введите конечный размер матрицы: "))

    time_full_combs = []
    time_ant = []

    sizes_arr = [i for i in range(size_start, size_end + 1)]

    count = 0
    print()

    # Time
    for size in sizes_arr:
        count += 1

        matrix = generate_matrix(size, 1, 2)

        # Full combinations
        start = process_time()
        full_combinations(matrix, size)
        end = process_time()

        time_full_combs.append(end - start)

        # Ant algorythm
        start = process_time()
        ant_algorythm(matrix, size, 0.5, 0.5, 0.5, 250)
        end = process_time()

        time_ant.append(end - start)

        print("Progress: %3d%s" %((count / len(sizes_arr)) * 100, "%"))

    # Table
    print("\n %s | %s | %s" %("Размер", "Время полного перебора", "Время муравьиного алгоритма"))
    print("-" * (8 + 1 + 24 + 1 + 29))

    for i in range(len(sizes_arr)):
        print(" %6d | %22.6f | %27.6f" %(sizes_arr[i], time_full_combs[i], time_ant[i]))

    # Graph
    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(sizes_arr, time_full_combs, label = "Полный перебор")
    plot.plot(sizes_arr, time_ant, label="Муравьиный алгоритм")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Размер матрицы")
    
    plt.show()


def parametrization():
    alpha_arr = [num / 10 for num in range(1, 10)]
    k_eva_arr = [num / 10 for num in range(1, 9)]
    days_arr = [10, 50, 100, 200, 300, 400, 500]

    size = 9

    matrix1 = generate_matrix(size, 1, 2)
    matrix2 = generate_matrix(size, 1000, 9999)

    optimal1 = full_combinations(matrix1, size)
    optimal2 = full_combinations(matrix2, size)

    file1 = open("parametrization_class1.txt", "w")
    file2 = open("parametrization_class2.txt", "w")

    count = 0
    count_all = len(alpha_arr) * len(k_eva_arr)

    for alpha in alpha_arr:
        beta = 1 - alpha

        for k_eva in k_eva_arr:
            count += 1

            for days in days_arr:
                res1 = ant_algorythm(matrix1, size, alpha, beta, k_eva, days)
                res2 = ant_algorythm(matrix2, size, alpha, beta, k_eva, days)

                sep = "|"
                ender = ""

                str1 = "%3.1f %s %3.1f %s %3.1d %s %5d %s %5d %s\n" \
                    % (alpha, sep, k_eva, sep, days, sep, optimal1[0], sep, res1[0] - optimal1[0], ender)

                str2 = "%3.1f %s %3.1f %s %3.1d %s %5d %s %5d %s\n" \
                    % (alpha, sep, k_eva, sep, days, sep, optimal1[0], sep, res2[0] - optimal2[0], ender)

                file1.write(str1)
                file2.write(str2)

            print("Progress: %3d%s" %((count / count_all) * 100, "%"))
            
    file1.close()
    file2.close()



def main():
    option = -1

    while (option != EXIT):
        option = int(input(MSG))

        if (option == ALL_COMB):
            parse_full_combinations()
        elif (option == ANT_ALG):
            parse_ant_alg()

        elif (option == ALG_ALL):
            parse_all()

        elif (option == PARAMETRIC):
            parametrization()

        elif (option == TEST):
            time_test()

        elif (option == UPDATE_DATA):
            update_file()

        elif (option == SHOW_DATA):
            print_matrix()

        else:
            print("\nПовторите ввод\n")


if __name__ == "__main__":
    main()
