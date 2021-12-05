# Libs
from time import process_time
import matplotlib.pyplot as plt 
from copy import deepcopy


from dictionary import Dictionary



# Text
MSG = "\n\n      Словари \n\n \
    1. Полный перебор \n \
    2. Бинарный поиск \n \
    3. Поиск сегментами \n\n \
    4. Все алгоритмы \n \
    5. Замерить время \n \
    6. Проанализировать кол-во сравнений \n\n \
    7. Распечатать словарь \n\n \
    0. Выход \n\n \
    \
    Выбор: \
    "

# Define
EXIT = 0
FULL_COMB_SEARCH = 1
BIN_SEARCH = 2
SEGM_SEARCH = 3
ALL_SEARCH = 4
TEST_TIME =  5
TEST_COMPARSIONS = 6
SHOW_DATA = 7

# Type
LATEX = 0
CSV = 1
NORMAL = 2

TIMES = 30
TO_MILISECONDS = 1000


# Functions
def time_mes(dictionary, key, alg):
    time_res = 0

    for i in range(TIMES):

        if (alg == FULL_COMB_SEARCH):
            start = process_time()
            dictionary.full_search(key, output = False)
        elif (alg == BIN_SEARCH):
            sorted_dict = dictionary.sort_dict(dictionary.data_dict)
            start = process_time()
            dictionary.binary_search(key, sorted_dict, output = False)
        elif (alg == SEGM_SEARCH):
            segmented_dict = dictionary.make_segments()
            start = process_time()
            dictionary.segment_search(key, segmented_dict, output = False)

        end = process_time()

        time_res += (end - start)

    return time_res / TIMES


def time_test(dictionary_obj):

    data_dict = dictionary_obj.data_dict

    ind_keys = [ind for ind in range(len(data_dict))]

    keys = list(data_dict.keys())

    full_search_time = []
    bin_search_time = []
    segm_search_time = []

    percentage = 0
    all_percentage = len(data_dict)
    print()

    for key in keys:
        percentage += 1

        full_search_time.append(time_mes(dictionary_obj, key, FULL_COMB_SEARCH))
        bin_search_time.append(time_mes(dictionary_obj, key, BIN_SEARCH))
        segm_search_time.append(time_mes(dictionary_obj, key, SEGM_SEARCH))

        if (percentage % 50 == 0):
            print("Progress: %5.2f%s (key = %s)" %((percentage / all_percentage) * 100, "%", key))


    # Graph
    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(ind_keys, full_search_time, label = "Поиск полным перебором")
    plot.plot(ind_keys, bin_search_time, label="Бинарный поиск")
    plot.plot(ind_keys, segm_search_time, label="Поиск сегментами")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Индекс ключа")
    
    plt.show()


def sort_comparsions(arr_comp):
    comp_sorted = deepcopy(arr_comp)

    for i in range(len(comp_sorted) - 1):
        for j in range(len(comp_sorted) - i - 1):
            if (comp_sorted[j] < comp_sorted[j + 1]):
                comp_sorted[j], comp_sorted[j + 1] = comp_sorted[j + 1], comp_sorted[j]

    return comp_sorted


def comparsion_test(dictionary_obj):

    alg = int(input("\nВыберите алгоритм: \
                \n\t1. Полный перебор \
                \n\t2. Бинарный поиск \
                \n\t3. Поиск сегментами \
                \n\nВыбор: "))

    alg_text = "Не определено"
    
    if (alg == FULL_COMB_SEARCH):
        alg_text = "Полный перебор"
    elif (alg == BIN_SEARCH):
        alg_text = "Бинарный поиск"
    elif (alg == SEGM_SEARCH):
        alg_text = "Поиск сегментами"
    else:
        print("\nОшибка: Неверно выбран алгоритм\n")
        return

    data_dict = dictionary_obj.data_dict

    ind_keys = [ind for ind in range(len(data_dict))]


    keys = list(data_dict.keys())

    search_comparsions = []

    percentage = 0
    all_percentage = len(data_dict)
    print()

    for key in keys:
        percentage += 1

        if (alg == FULL_COMB_SEARCH):
            search_comparsions.append(dictionary_obj.parse_full_search(key, output = False))
        elif (alg == BIN_SEARCH):
            search_comparsions.append(dictionary_obj.parse_binary_search(key, output = False))
        elif (alg == SEGM_SEARCH):
            search_comparsions.append(dictionary_obj.parse_segment_search(key, output = False))

        if (percentage % 50 == 0):
            print("Progress: %5.2f%s (key = %s)" %((percentage / all_percentage) * 100, "%", key))


    comp_sorted = sort_comparsions( search_comparsions)

    # Graph
    fig, ax = plt.subplots(2, 1, figsize = (10, 10))

    ax[0].bar(ind_keys, search_comparsions, alpha = 0.5)
    ax[0].set(title = alg_text)
    ax[1].bar(ind_keys, comp_sorted, alpha = 0.5)
    ax[1].set(title = alg_text + " (отсоритрованный)")

    for i in range(0, 2):
        ax[i].set_xlabel("Индекс ключа")
        ax[i].set_ylabel("Количество сравнений")
        ax[i].grid()
    
    plt.show()


def main():
    option = -1

    dictionary = Dictionary("data/fifa_players.csv")

    while (option != EXIT):
        option = int(input(MSG))

        if (option == FULL_COMB_SEARCH):

            key = input("\nВведите фамилию футболиста: ")

            dictionary.parse_full_search(key)

        elif (option == BIN_SEARCH):

            key = input("\nВведите фамилию футболиста: ")

            dictionary.parse_binary_search(key)

        elif (option == SEGM_SEARCH):

            key = input("\nВведите фамилию футболиста: ")

            dictionary.parse_segment_search(key)

        elif (option == ALL_SEARCH):

            key = input("\nВведите фамилию футболиста: ")

            dictionary.parse_all(key)

        elif (option == TEST_TIME):

            time_test(dictionary)

        elif (option == TEST_COMPARSIONS):

            comparsion_test(dictionary)

        elif (option == SHOW_DATA):

            dictionary.print_dict()

        else:
            print("\nПовторите ввод\n")


if __name__ == "__main__":
    main()
