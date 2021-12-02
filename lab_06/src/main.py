# Libs
from time import process_time
from random import randint, random
import matplotlib.pyplot as plt 

import numpy as np

from os import system



# Text
MSG = "\n\n      Задача коммивояжера \n\n \
    1. Полный перебор \n \
    2. Мураьиный алгоритм \n \
    3. Замерить время \n \
    0. Выход \n\n \
    \
    Выбор: \
    "

# Define
EXIT = 0
ALL_COMB = 1
ANT_ALG = 2
TEST =  3

ODD = 1
EVEN = 2

TIMES = 100
TO_MILISECONDS = 1000


# Functions

def generate_matrix(size):

    matrix = np.zeros((size, size), dtype = int)

    for i in range(size):
        for j in range(size):

            if (i == j):
                num = 0
            else:
                num = randint(1, 10)

            matrix[i][j] = num
            matrix[j][i] = num

    return matrix


def generate_matrix_file(file_name, size):

    matrix = generate_matrix(size)

    file = open(file_name, "w")

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

    file = open(file_name, "r")
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


def read_data():
    system("ls \data > files.txt")

    f_files = open("files.txt", "r")

    files = f_files.read().split()

    f_files.close()


    print("\n\nДоступные файлы: ", len(files), " штук", )

    for i in range(len(files)):
        print("%d. %s" % (i + 1, files[i]))

    num_file = int(input("\nВыберите файл: ")) - 1




        








def main():
    option = -1

    while (option != EXIT):
        option = int(input(MSG))

        if (option == ALL_COMB):
            read_data()

        elif (option == ANT_ALG):
            read_file_matrix("data/mat5.csv")

        elif (option == TEST):
            pass

        else:
            print("\nПовторите ввод\n")


if __name__ == "__main__":
    main()
