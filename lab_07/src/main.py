# Libs
from time import process_time
from random import randint, random
from typing import TYPE_CHECKING
import matplotlib.pyplot as plt 
from copy import deepcopy

import numba

import itertools as it
import numpy as np
from os import system

from algorythms import full_combinations, ant_algorythm



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

NAME = 0
INFO = 1
RATING = 0
COUNTRY = 1
CLUB = 2

FIRST_LETTER = 0


# Functions

class Dictionary(object):

    data_dict = dict()


    def __init__(self, filename):
        self.load_csv(filename)
    

    def load_csv(self, filename):
        # CSV file must have in first column Key
        # Other columns will become Value as list

        file = open(filename, "r")

        data = []

        for line in file.readlines():
            tmp = line.split(",")
            tmp[len(tmp) - 1] = tmp[len(tmp) - 1][:-1] # delete \n at the end of last field
            data.append(tmp)

        file.close()

        parsed_data = []

        for record in data: # delete not unique name
            if record[NAME] not in [result[NAME] for result in parsed_data]:
                parsed_data.append(record)

        for i in range(len(parsed_data)):
            key = parsed_data[i][NAME]
            value = [parsed_data[i][ind] for ind in range(1, len(parsed_data[i]))]

            self.data_dict[key] = value


    def print_record(self, record): # For footballers only
        print("Name: %s\nRating: %s, Country: %s, Club: %s\n" \
                    %(record[NAME], record[INFO][RATING], record[INFO][COUNTRY], record[INFO][CLUB]))


    def print_dict(self):
        if (len(self.data_dict) == 0):
            print("\nОшибка: Словарь пуст\n")
            return

        all_records = self.data_dict.items()

        for record in all_records:
            self.print_record(record)


    def full_search(self, key, output = True):
        count = 0 # count of comparsions

        keys = self.data_dict.keys()

        for elem in keys:
            count += 1

            if (elem == key):
                if (output):
                    record = [key, self.data_dict[key]]
                    print("\nРезультат поиска:\n")
                            
                    self.print_record(record)
                    
                return count

        return -1


    def parse_full_search(self, key, output = True):
        count = self.full_search(key, output)
        
        if (output):
            print("Полный перебор:\nКоличество сравнений: ", count if (count != -1) else "Не найдено")

        return count
    

    def sort_dict(self, to_sort_dict):
        keys = list(to_sort_dict.keys())
        keys.sort()

        tmp_dict = dict()

        for key in keys:
            tmp_dict[key] = to_sort_dict[key]

        return tmp_dict

    
    def parse_binary_search(self, key, output = True):

        sorted_dict = self.sort_dict(self.data_dict)

        count = self.binary_search(key, sorted_dict, output)

        if (output):
            print("Бинарный поиск:\nКоличество сравнений: ", count if (count != -1) else "Не найдено")

        return count


    def binary_search(self, key, sorted_dict, output = True):
        count = 0 # count of comparsions

        keys = list(sorted_dict.keys())

        left = 0 
        right = len(keys)

        while (left <= right):
            count += 1
            middle = (left + right) // 2
            elem = keys[middle]

            if (elem == key):
                if (output):
                    record = [key, sorted_dict[key]]
                    print("\nРезультат поиска:\n")     
                    self.print_record(record)
                    
                return count

            if (elem < key):
                left = middle + 1
            else:
                right = middle - 1

        return -1


    def sort_value(self, diction):
        sorted_dict = dict()

        # sorted by value dict items
        items = list(diction.items())
        items.sort(key = lambda k: k[1], reverse = True)

        for elem in items:
            sorted_dict[elem[0]] = elem[1]

        return sorted_dict


    def make_segments(self):
        temp_dict = {i: 0 for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

        for key in self.data_dict:
            temp_dict[key[FIRST_LETTER]] += 1

        temp_dict = self.sort_value(temp_dict)

        segmented_dict = {i: dict() for i in temp_dict}

        for key in self.data_dict:
            segmented_dict[key[0]].update({key: self.data_dict[key]})

        return segmented_dict

    
    def segment_search(self, key, segmented_dict, output = True):
        count = 0

        for key_letter in segmented_dict:
            count += 1

            if (key[FIRST_LETTER] == key_letter):
                count_search = 0

                for elem in segmented_dict[key_letter]:
                    count_search += 1

                    if (elem == key):
                        if (output):
                            record = [key, segmented_dict[key_letter][key]]
                            print("\nРезультат поиска:\n")     
                            self.print_record(record)

                        return count_search + count

                return -1


    def parse_segment_search(self, key, output = True):

        segmented_dict = self.make_segments()

        count = self.segment_search(key, segmented_dict, output)

        if (output):
            print("Поиск сегментами:\nКоличество сравнений: ", count if (count != -1) else "Не найдено")

        return count


    def parse_all(self, key):
        self.parse_full_search(key)
        self.parse_binary_search(key)
        self.parse_segment_search(key)


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
