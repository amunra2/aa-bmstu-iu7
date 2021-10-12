# Libs
from time import process_time
from random import randint
import matplotlib.pyplot as plt 
from copy import deepcopy

from sorts import insertion_sort, shaker_sort, gnomme_sort


# Text
MSG = "\n\n      Меню \n\n \
    1. Сортировка вставками \n \
    2. Сортировка перемешиванием \n \
    3. Гномья сортировка \n \
    4. Замеры времени \n \
    0. Выход \n\n \
    \
    Выбор: \
    "

# Define
EXIT = 0
INSERTION = 1
SHAKER = 2
GNOMME = 3
TEST = 4

TIMES = 1000
TO_MILISECONDS = 1000

INPUT_KEYBOARD = 1
INPUT_FILE = 0
INPUT_TYPE = 0

FILE = "arr25.csv"


# Functions

def input_arr_keyboard():
    arr = list()

    nums = 0

    print("Введите массив поэлементно в одной строке (окончание - Enter): ")

    nums = input().split()

    for i in range(len(nums)):
        try:
            arr.append(int(nums[i]))
        except:
            print("Ошибка: введено не число")

    return arr


def input_arr_file():
    f = open(FILE, "r")

    arr = list()

    for line in f:
        try:
            arr.append(int(line))
        except:
            print("Ошибка: введено не число")

    return arr


def input_arr():

    if (INPUT_TYPE):
        arr = input_arr_keyboard()
    else:
        arr = input_arr_file()

    return arr


def get_arr_sorted(size):
    arr = list()

    for i in range(size):
        arr.append(i)

    return arr


def get_arr_down_sorted(size):
    arr = list()

    for i in range(size):
        arr.append(size - i)

    return arr


def get_arr_random(size):
    arr = list()

    for _ in range(size):
        arr.append(randint(0, 100))

    return arr


def get_arr_by_type(option, size):

    #size = int(input("Введите количество элементов в массиве: "))
    #option = int(input("Введите тип массива: "))

    type = "Не определено"

    if (option == 0):

        arr = get_arr_sorted(size)
        type = "Отсортированный "


    elif (option == 1):

        arr = get_arr_down_sorted(size)
        type = "Отсортированный в обратном порядке "

    elif (option == 2):

        arr = get_arr_random(size)
        type = "Случайный "

    return arr, type


def get_sort():

    option = int(input("Введите номер сортировки: "))

    if (option == 0):

        func = insertion_sort

    elif (option == 1):

        func = shaker_sort

    elif (option == 2):

        func = gnomme_sort

    return func


def get_process_time(func, arr):
    
    time_res = 0

    for _ in range(TIMES):
        arr_tmp = deepcopy(arr)

        time_start = process_time()
        func(arr_tmp, len(arr_tmp))
        time_end = process_time()

        time_res += (time_end - time_start)


    return time_res / TIMES


def test_sort():
    time_shaker = []
    time_gnomme = []
    time_insertion = []

    option = int(input("\nВведите тип массива \n(0 - отсортированный, 1 - отсортированный в обратном порядке, 2 - случайный): "))

    # Arr

    # sizes = [10, 50, 100, 200, 300, 400, 500]
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    for num in sizes:
        arr, type = get_arr_by_type(option, num)

        time_shaker.append(get_process_time(shaker_sort, arr))
        time_gnomme.append(get_process_time(gnomme_sort, arr))
        time_insertion.append(get_process_time(insertion_sort, arr))

    print("\n\n" + type + "массив: \n")

    ind = 0

    # for num in sizes:
    #     print("Размер = %4d : перемешиванием = %.4f, вставками = %.4f, гномья = %.4f" %(num, \
    #         time_shaker[ind] * TO_MINCROSECONDS, \
    #         time_insertion[ind] * TO_MINCROSECONDS, \
    #         time_gnomme[ind] * TO_MINCROSECONDS))

    #     ind += 1


    for num in sizes:
        print(" %4d & %.4f & %.4f & %.4f \\\\ \n \\hline" %(num, \
            time_shaker[ind] * TO_MILISECONDS, \
            time_insertion[ind] * TO_MILISECONDS, \
            time_gnomme[ind] * TO_MILISECONDS))

        ind += 1

    # Graph

    fig1 = plt.figure(figsize=(10, 7))
    plot = fig1.add_subplot()
    plot.plot(sizes, time_shaker, label = "Сортировка Шейкер")
    plot.plot(sizes, time_insertion, label="Сортировка вставками")
    plot.plot(sizes, time_gnomme, label="Гномья сортировка")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики алгоритмов сортировок\n" + type + "массив")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Длина")
    
    plt.show()


def main():
    option = -1

    while (option != EXIT):
        option = int(input(MSG))

        if (option == INSERTION):

            arr = input_arr()
            print(insertion_sort(arr, len(arr)))

        elif (option == SHAKER):

            arr = input_arr()
            print(shaker_sort(arr, len(arr)))

        elif (option == GNOMME):
            
            arr = input_arr()
            print(gnomme_sort(arr, len(arr)))

        elif (option == TEST):

            test_sort()
            #print("\nIt's coming soon...")


if __name__ == "__main__":
    main()
