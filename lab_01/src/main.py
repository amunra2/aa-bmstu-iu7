# Libs
from time import process_time
from random import choice
import matplotlib.pyplot as plt 
import string

from algorythms import damerau_levenstein_recursive, levenstein_cache_matrix, levenstein_matrix, levenstein_recursive


# Text
MSG = "\n\n      Меню \n\n \
    1. Расстояние Левенштейна (рекурсивно) \n \
    2. Расстояние Левенштейна (матрица) \n \
    3. Расстояние Левенштейна (рекурсивно с кешем) \n \
    4. Росстояние Дамерау-Левенштейна (рекурсивно) \n \
    5. Замерить времени \n \
    0. Выход \n\n \
    \
    Выбор: \
    "

# Define
EXIT = 0
LEV_REC = 1
LEV_MAT = 2
LEV_REC_CACHE = 3
DAM_LEV_REC = 4
TEST =  5

TIMES = 100
TO_MILISECONDS = 1000


# Functions

def input_data():
    str1 = input("\nВведите 1-ую строку:\t")
    str2 = input("Введите 2-ую строку:\t")

    return str1, str2


def get_random_string(size):
    letters = string.ascii_lowercase

    return "".join(choice(letters) for _ in range(size))


def get_process_time(func, size):
    
    time_res = 0

    for _ in range(TIMES):
        str1 = get_random_string(size)
        str2 = get_random_string(size)

        time_start = process_time()
        func(str1, str2, output = False)
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


def graph_lev_and_dam_lev(time_lev_rec, time_dam_lev_rec):

    sizes = [0, 1, 2, 3, 4, 5, 6, 7, 8 , 9]

    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(sizes, time_lev_rec, label = "Левенштейн (рекурсия)")
    plot.plot(sizes, time_dam_lev_rec, label="Дамерау-Левенштейн (рекурсия)")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Длина")
    
    plt.show()


def graph_lev_mat_and_cache(time_lev_mat, time_lev_cache):

    sizes = [0, 1, 2, 3, 4, 5, 6, 7, 8 , 9]

    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(sizes, time_lev_mat, label = "Левенштейн (матричный)")
    plot.plot(sizes, time_lev_cache, label="Левенштейн (кеш)")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Длина")
    
    plt.show()


def test_algos():
    time_lev_rec = []
    time_lev_mat = []
    time_lev_cache = []
    time_dam_lev_rec = []

    for num in range(10):

        print("Progress:\t", num * 10, "%")

        time_lev_rec.append(get_process_time(levenstein_recursive, num))
        time_lev_mat.append(get_process_time(levenstein_matrix, num))
        time_lev_cache.append(get_process_time(levenstein_cache_matrix, num))
        time_dam_lev_rec.append(get_process_time(damerau_levenstein_recursive, num))

    print("\n\nЗамер времени для алгоритмов: \n")

    ind = 0

    for num in range(10):
        print(" %4d & %.4f & %.4f & %.4f & %.4f \\\\ \n \\hline" %(num, \
            time_lev_rec[ind] * TO_MILISECONDS, \
            time_lev_mat[ind] * TO_MILISECONDS, \
            time_lev_cache[ind] * TO_MILISECONDS, \
            time_dam_lev_rec[ind] * TO_MILISECONDS))

        ind += 1

    graph_lev_and_dam_lev(time_lev_rec, time_dam_lev_rec)
    graph_lev_mat_and_cache(time_lev_mat, time_lev_cache)
    graph_lev_rec_and_cache(time_lev_rec, time_lev_cache)


def main():
    option = -1

    while (option != EXIT):
        option = int(input(MSG))

        if (option == LEV_REC):

            str1, str2 = input_data()
            print("\nРезультат: ", levenstein_recursive(str1, str2))

        elif (option == LEV_MAT):

            str1, str2 = input_data()
            print("\nРезультат: ", levenstein_matrix(str1, str2))

        elif (option == LEV_REC_CACHE):
            
            str1, str2 = input_data()
            print("\nРезультат: ", levenstein_cache_matrix(str1, str2))

        elif (option == DAM_LEV_REC):

            str1, str2 = input_data()
            print("\nРезультат: ", damerau_levenstein_recursive(str1, str2))

        elif (option == TEST):
            
            test_algos()

        else:
            print("\nПовторите ввод\n")


if __name__ == "__main__":
    main()
