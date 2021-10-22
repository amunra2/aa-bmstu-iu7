def levenstein_recursive(str1, str2, output = True):
    n = len(str1)
    m = len(str2)

    if ((n == 0) or (m == 0)):
        return abs(n - m)

    flag = 0

    if (str1[-1] != str2[-1]):
        flag = 1

    min_distance = min(levenstein_recursive(str1[:-1], str2) + 1,
                    levenstein_recursive(str1, str2[:-1]) + 1,
                    levenstein_recursive(str1[:-1], str2[:-1]) + flag)

    return min_distance


def create_lev_matrix(n, m):
    matrix = [[0] * m for _ in range(n)]

    for i in range(n):
        matrix[i][0] = i
    
    for j in range(m):
        matrix[0][j] = j

    return matrix
    

def print_lev_matrix(matrix, str1, str2):
    print("\n0  0  " + "  ".join([let for let in str2]))

    for i in range(len(str1) + 1):
        
        print(str1[i - 1] if (i != 0) else "0", end = "")

        for j in range(len(str2) + 1):

            print("  " + str(matrix[i][j]), end = "")

        print("")


def levenstein_matrix(str1, str2, output = True):
    n = len(str1)
    m = len(str2)

    matrix = create_lev_matrix(n + 1, m + 1)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            add = matrix[i - 1][j] + 1
            delete = matrix[i][j - 1] + 1
            change = matrix[i - 1][j - 1]
            
            if (str1[i - 1] != str2[j - 1]):
                change += 1

            matrix[i][j] = min(add, delete, change)

    if (output):
        print("\nМатрица, с помощью которой происходило вычисление расстояния Левенштейна:")
        print_lev_matrix(matrix, str1, str2)

    return matrix[n][m]


def recursive_for_levenstein_cache(str1, str2, n, m, matrix):
    if (matrix[n][m] != -1):
        return matrix[n][m]

    if (n == 0):
        matrix[n][m] = m
        return matrix[n][m]

    if ((n > 0) and (m == 0)):
        matrix[n][m] = n
        return matrix[n][m]

    add = recursive_for_levenstein_cache(str1, str2, n - 1, m, matrix) + 1
    delete = recursive_for_levenstein_cache(str1, str2, n, m - 1, matrix) + 1
    change = recursive_for_levenstein_cache(str1, str2, n - 1, m - 1, matrix)

    if (str1[n - 1] != str2[m - 1]):
        change += 1 # flag

    matrix[n][m] = min(add, delete, change)

    return matrix[n][m]


def levenstein_cache_matrix(str1, str2, output = True):
    n = len(str1)
    m = len(str2)

    matrix = create_lev_matrix(n + 1, m + 1)


    for i in range(n + 1):
        for j in range(m + 1):
            matrix[i][j] = -1

    recursive_for_levenstein_cache(str1, str2, n, m, matrix)

    if (output):
        print("\nМатрица для кеша рекурсивного нахождения расстояния Левенштейна:")
        print_lev_matrix(matrix, str1, str2)

    return matrix[n][m]


def damerau_levenstein_recursive(str1, str2, output = True):
    n = len(str1)
    m = len(str2)

    if ((n == 0) or (m == 0)):
        if (n != 0):
            return n
        
        if (m != 0):
            return m

        return 0

    flag = 0 if (str1[-1] == str2[-1]) else 1

    add = damerau_levenstein_recursive(str1[:n - 1], str2) + 1
    delete = damerau_levenstein_recursive(str1, str2[:m - 1]) + 1
    change = damerau_levenstein_recursive(str1[:n - 1], str2[:m - 1]) + flag
    extra_change = damerau_levenstein_recursive(str1[:n - 2], str2[:m - 2]) + 1

    if ((n > 1) and (m > 1) and (str1[-1] == str2[-2]) and (str1[-2] == str2[-1])):
        minimum  = min(add, delete, change, extra_change)

    else:
        minimum = min(add, delete, change)

    return minimum