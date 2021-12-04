# Libs
from time import process_time
from random import randint, random
from typing import TYPE_CHECKING
import matplotlib.pyplot as plt 

import itertools as it
import numpy as np
from os import system

from algorythms import full_combinations, ant_algorythm



# Text
MSG = "\n\n      Словари \n\n \
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

# Type
LATEX = 0
CSV = 1
NORMAL = 2

TIMES = 100
TO_MILISECONDS = 1000




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
    option = int(input("\nДобавить новый файл? (1 - да, 2 - нет): "))

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


def parse_full_combinations():

    matrix = read_matrix()
    size = len(matrix)

    result = full_combinations(matrix, size)

    print("\n\nМинимальная сумма пути = ", result[0], 
            "\nПуть: ", result[1])


def read_koefs():
    alpha = float(input("\n\nВведите коэффициент alpha: " ))
    beta = 1 - alpha
    k_evaporation = float(input("Введите коэффициент evaporation: " ))
    days = int(input("Введите кол-во дней: " ))
    
    return alpha, beta, k_evaporation, days


def parse_ant_alg():

    matrix = read_matrix()
    size = len(matrix)

    alpha, beta, k_evaporation, days = read_koefs()

    result = ant_algorythm(matrix, size, alpha, beta, k_evaporation, days)

    print("\n\nМинимальная сумма пути = ", result[0], 
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

    # For Latex
    f_latex = open("latex_table.txt", "w")

    for i in range(len(sizes_arr)):
        f_latex.write("%4d & %10.6f & %10.6f \\\\ \\hline\n" %(sizes_arr[i], time_full_combs[i], time_ant[i]))

    f_latex.close()
    
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


def parametrization(type = CSV):
    alpha_arr = [num / 10 for num in range(1, 10)]
    k_eva_arr = [num / 10 for num in range(1, 9)]
    days_arr = [1, 3, 5, 10, 50, 100, 300, 500]

    size = 9

    matrix1 = read_file_matrix("mat9_lowdif.csv")
    matrix2 = read_file_matrix("mat9_highdif.csv")

    optimal1 = full_combinations(matrix1, size)
    optimal2 = full_combinations(matrix2, size)

    file1 = open("parametrization_class1.txt", "w")
    file2 = open("parametrization_class2.txt", "w")

    count = 0
    count_all = len(alpha_arr) * len(k_eva_arr)

    print()

    for alpha in alpha_arr:
        beta = 1 - alpha

        for k_eva in k_eva_arr:
            count += 1

            for days in days_arr:
                res1 = ant_algorythm(matrix1, size, alpha, beta, k_eva, days)
                res2 = ant_algorythm(matrix2, size, alpha, beta, k_eva, days)

                if (type == LATEX):
                    sep = " & "
                    ender = " \\\\"
                elif (type == CSV):
                    sep = ", "
                    ender = ""
                else:
                    sep = " | " 
                    ender = ""

                str1 = "%4.1f%s%4.1f%s%4d%s%5d%s%5d%s\n" \
                    % (alpha, sep, k_eva, sep, days, sep, optimal1[0], sep, res1[0] - optimal1[0], ender)

                str2 = "%4.1f%s%4.1f%s%4d%s%5d%s%5d%s\n" \
                    % (alpha, sep, k_eva, sep, days, sep, optimal2[0], sep, res2[0] - optimal2[0], ender)

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
            parametrization(type = CSV)

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
