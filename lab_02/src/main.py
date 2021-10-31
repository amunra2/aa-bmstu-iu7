# Libs
from time import process_time
from random import randint
import matplotlib.pyplot as plt 

from algorythms import standart_alg, vinograd_alg, optimized_vinograd_alg


# Text
MSG = "\n\n      Меню \n\n \
    1. Станадартное умножение матриц \n \
    2. Алгоритм Винограда \n \
    3. Опитимизированный алгоритм Винограда \n \
    4. Все алгоритмы вместе \n \
    5. Замерить время \n \
    0. Выход \n\n \
    \
    Выбор: \
    "

# Define
EXIT = 0
STD_ALG = 1
VIN_ALG = 2
OPT_VIN_ALG = 3
ALL_ALG = 4
TEST =  5

ODD = 1
EVEN = 2

TIMES = 100
TO_MILISECONDS = 1000


# Functions

def input_matrix():

    try:
        row = int(input("\nВведите количество строк: \t"))
        col = int(input("Введите количество столбцов: \t"))

        if ((row < 1) or (col < 1)):
            print("Ошибка: Должно быть больше 1")
            return []

    except:
        print("Ошибка: Введено не число")
        return []

    print("\nВведите матрицу по строчно (в одной строке - все числа для данной строки матрицы): ")
    matrix = []

    for _ in range(row):
        tmp_arr = list(int(i) for i in input().split())

        if (len(tmp_arr) != col):
            print("Ошибка: Количество чисел не соответствует количеству столбцов матрицы")
            return []

        matrix.append(tmp_arr)

    return matrix
        

def output_matrix(matrix, msg):

    print(msg + '\n')

    row = len(matrix)
    col = len(matrix[0])

    for i in range(row):
        for j in range(col):

            print("%-3d" %(matrix[i][j]), end = '')

        print()



def input_data():
    mat_a = input_matrix()
    mat_b = input_matrix()

    return mat_a, mat_b


def get_rand_matrix(size):
    
    matrix = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            matrix[i][j] = randint(0, 50)

    return matrix


def get_process_time(func, size):
    
    time_res = 0

    for _ in range(TIMES):
        mat_a = get_rand_matrix(size)
        mat_b = get_rand_matrix(size)

        time_start = process_time()
        func(mat_a, mat_b)
        time_end = process_time()

        time_res += (time_end - time_start)


    return time_res / TIMES


def graph_lev_rec_and_cache(time_lev_rec, time_lev_cache):

    sizes = [0, 1, 2, 3, 4, 5, 6, 7, 8 , 9]

    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(sizes, time_lev_rec, label = "Левенштейн (рекурсия)")
    plot.plot(sizes, time_lev_cache, label="Левенштейн (рекурсия + кеш)")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Длина")
    
    plt.show()


def test_algos():

    is_size = int(input("\nТестировать на: 1 - нечетных размерах матриц, 2 - четных: "))

    if ((is_size > 2) or (is_size < 1)):
        print("Ошибка: Неверно выбрана опция заполнения матриц")
        return

    even_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    odd_sizes = [11, 21, 31, 41, 51, 61, 71, 81, 91, 101]

    time_std_alg = []
    time_vin_alg = []
    time_opt_vin_alg = []

    for_test = even_sizes
    graph_text = "\nЧетные размеры матриц"

    if (is_size == EVEN):
        for_test = even_sizes
        graph_text = "\nЧетные размеры матриц"
    elif (is_size == ODD):
        for_test = odd_sizes
        graph_text = "\nНечетные размеры матриц"

    print()

    for num in for_test:

        print("Progress:\t", num, " len")

        time_std_alg.append(get_process_time(standart_alg, num))
        time_vin_alg.append(get_process_time(vinograd_alg, num))
        time_opt_vin_alg.append(get_process_time(optimized_vinograd_alg, num))

    print("\n\nЗамер времени для алгоритмов: \n")

    ind = 0

    for num in for_test:
        print(" %4d & %.4f & %.4f & %.4f \\\\ \n \\hline" %(num, \
            time_std_alg[ind] * TO_MILISECONDS, \
            time_vin_alg[ind] * TO_MILISECONDS, \
            time_opt_vin_alg[ind] * TO_MILISECONDS))

        ind += 1

    # Graph


    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(for_test, time_vin_alg, label = "Стандартный алгоритм")
    plot.plot(for_test, time_std_alg, label="Алгоритм Винограда")
    plot.plot(for_test, time_opt_vin_alg, label="Оптимизированный алгоритм Винограда")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики" + graph_text)
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Размер")
    
    plt.show()




def main():
    option = -1

    while (option != EXIT):
        option = int(input(MSG))

        if (option == STD_ALG):

            mat_a, mat_b = input_data()

            res = standart_alg(mat_a, mat_b)

            output_matrix(res, "\n\nРезультат:")

        elif (option == VIN_ALG):

            mat_a, mat_b = input_data()

            res = vinograd_alg(mat_a, mat_b)

            output_matrix(res, "\n\nРезультат:")

        elif (option == OPT_VIN_ALG):
            
            mat_a, mat_b = input_data()

            res = optimized_vinograd_alg(mat_a, mat_b)

            output_matrix(res, "\n\nРезультат:")

        elif (option == ALL_ALG):

            mat_a, mat_b = input_data()

            res_std = standart_alg(mat_a, mat_b)
            res_vin = vinograd_alg(mat_a, mat_b)
            res_opt = optimized_vinograd_alg(mat_a, mat_b)

            output_matrix(res_std, "\n\nРезультат стандартаного алгоритма:")
            output_matrix(res_vin, "\n\nРезультат алгоритма Винограда:")
            output_matrix(res_opt, "\n\nРезультат оптимизированного алгоритма Винограда:")

        elif (option == TEST):
            
            test_algos()

        else:
            print("\nПовторите ввод\n")


if __name__ == "__main__":
    main()
