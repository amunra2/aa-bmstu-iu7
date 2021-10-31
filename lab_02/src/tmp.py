from time import process_time

COMPARE_TYPE = 1
RUNS_NUM = 100

def input_matrix():

    try:
        n = int(input("\nВведите количество строк:\n"))

        if n < 1:
            print("\nОшибка: количество строк должно быть больше нуля\n")
            return []

        m = int(input("\nВведите количество столбцов:\n"))

        if m < 1:
            print("\nОшибка: количество столбцов меньше нуля\n")
            return [] 

    except:
        print("\nОшибка: должно быть число\n")
        return [] 

    print("\nВведите матрицу по числу через пробел:\n")
    matrix = []

    for i in range(n):
        try:
            array = list(int(i) for i in input().split())
        except:
            print("\nОшибка: должно быть число\n")
            return []

        if len(array) != m:
            print("\nОшибка: неверно введено количество чисел\n")
            return []
        else:
            matrix.append(array)
    return matrix

def output_matrix(matrix):

    n = len(matrix)
    m = len(matrix[0])
    print()

    for i in range (n):
        for j in range (m):
            print(matrix[i][j], end = ' ')
        print()

    print("\n")

def classic_alg(matrix_1, matrix_2):
    n = len(matrix_1)
    m = len(matrix_1[0])
    k = len(matrix_2[0])

    result_matrix_ = [[0] * k for _ in range(n)]

    for i in range(n):
        for j in range(k):
            for u in range(m):
                result_matrix_[i][j] += matrix_1[i][u] * matrix_2[u][j]

    return result_matrix_


def vinograd_alg(matrix_1, matrix_2):
    n = len(matrix_1)
    m = len(matrix_1[0])
    k = len(matrix_2[0])

    result_matrix_ = [[0] * k for _ in range(n)]
    row_factor = [0] * n

    for i in range(n):
        for j in range(0, m // 2, 1):
            row_factor[i] += matrix_1[i][2 * j] * matrix_1[i][2 * j + 1]

    column_factor = [0] * k

    for i in range(k):
        for j in range(0, m // 2, 1):
            column_factor[i] += matrix_2[2 * j][i] * matrix_2[2 * j + 1][i]

    for i in range(n):
        for j in range(k):
            result_matrix_[i][j] = -row_factor[i] - column_factor[j]
            for u in range(0, m // 2, 1):
                result_matrix_[i][j] += (matrix_1[i][2 * u + 1] + matrix_2[2 * u    ][j]) * \
                                  (matrix_1[i][2 * u] + matrix_2[2 * u + 1][j])

    if m % 2 == 1:
        for i in range(n):
            for j in range(k):
                result_matrix_[i][j] += matrix_1[i][m - 1] * matrix_2[m - 1][j]
    return result_matrix_


def optimized_vinograd_alg(matrix_1, matrix_2):
    n = len(matrix_1)
    m = len(matrix_1[0])
    k = len(matrix_2[0])

    result_matrix_ = [[0] * k for _ in range(n)]
    row_factor = [0] * n

    for i in range(n):
        for j in range(1, m, 2):
            row_factor[i] += matrix_1[i][j] * matrix_1[i][j - 1]

    column_factor = [0] * k

    for i in range(k):
        for j in range(1, m, 2):
            column_factor[i] += matrix_2[j][i] * matrix_2[j - 1][i]
    flag = n % 2

    for i in range(n):
        for j in range(k):
            result_matrix_[i][j] = -(row_factor[i] + column_factor[j])

            for u in range(1, m, 2):
                result_matrix_[i][j] += (matrix_1[i][u - 1] + matrix_2[u    ][j]) * \
                                  (matrix_1[i][u    ] + matrix_2[u - 1][j])

            if flag:
                result_matrix_[i][j] += matrix_1[i][m - 1] * matrix_2[m - 1][j]

    return result_matrix_

def func_run(function):
    print("\nМатрица 1\n")
    matrix_1 = input_matrix()

    if matrix_1 == []:
        return

    print("\nМатрица 2\n")
    matrix_2 = input_matrix()

    if matrix_2 == []:
        return

    if len(matrix_2) != len(matrix_1[0]):
        print("\n\tОшибка: количество строк одной матрицы должно быть равно количеству столбцов второй матрицы\n")
        return

    result= function(matrix_1, matrix_2)
    print("\nРезультат перемножения матриц:\n")

    output_matrix(result)

def time_count(function, nIter, size):
    matrix_1 = [[0] * size for _ in range(size)]
    matrix_2 = [[0] * size for _ in range(size)]

    t1 = process_time()

    for i in range(nIter):
        function(matrix_1, matrix_2)

    t2 = process_time()

    return (t2 - t1) / nIter

def menu():
    flag = True
    while(flag):
        command = input("Меню:\n \
\t1. Классическое перемножение матриц\n \
\t2. Алгоритм Винограда\n \
\t3. Оптимизированный алгоритм Винограда\n \
\t4. Замеры времени\n\n \
\t0. Выход\n")
        if (command == "1"):
            func_run(classic_alg)
        elif (command == "2"):
            func_run(vinograd_alg)
        elif (command == "3"):
            func_run(optimized_vinograd_alg)
        elif (command == "4"):
            if COMPARE_TYPE:
                sizes = [9, 19, 29, 39, 49, 59]
            else:
                sizes = [10, 20, 30, 40, 50, 60]
            for n in sizes:
                print("\n")
                print("Размер матрицы: ", n)  
                print("   Классическое перемножение            : ", "{0:.6f}".format(time_count(classic_alg, RUNS_NUM, n)))
                print("   Алгоритм Винограда                   : ", "{0:.6f}".format(time_count(vinograd_alg, RUNS_NUM, n)))
                print("   Оптимизированный алгоритм Винограда  : ", "{0:.6f}".format(time_count(optimized_vinograd_alg, RUNS_NUM, n)))
                print("\n")
        elif (command == "0"):
            return 0
        else:
            flag = False

if __name__ == "__main__": 
    menu()