def standart_alg(mat_a, mat_b):
    if (len(mat_a[0]) != len(mat_b)):
        print("Ошибка: Размеры не совпадают - умножение таких матриц невозможно")

        return []

    n = len(mat_a)
    m = len(mat_a[0])
    t = len(mat_b[0])

    res_matrix = [[0] * t for _ in range(n)]

    for i in range(n):
        for j in range(m):
            for k in range(t):
                res_matrix[i][j] += mat_a[i][k] * mat_b[k][j]

    return res_matrix


def vinograd_alg(mat_a, mat_b):
    if (len(mat_a[0]) != len(mat_b)):
        print("Ошибка: Размеры не совпадают - умножение таких матриц невозможно")

        return []

    n = len(mat_a)
    m = len(mat_a[0])
    t = len(mat_b[0])

    res_matrix = [[0] * t for _ in range(n)]

    tmp_row = [0] * n
    tmp_col = [0] * t

    for i in range(n):
        for j in range(0, m // 2):
            tmp_row[i] = tmp_row[i] + mat_a[i][2 * j] * mat_a[i][2 * j + 1]

    for i in range(t):
        for j in range(0, m // 2):
            tmp_col[i] = tmp_col[i] + mat_b[2 * j][i] * mat_b[2 * j + 1][i] 


    for i in range(n):
        for j in range(t):

            res_matrix[i][j] = -tmp_row[i] - tmp_col[i]   

            for k in range(0, m // 2):

                res_matrix[i][j] = res_matrix[i][j] + (mat_a[i][2 * k + 1] + mat_b[2 * k][j]) * (mat_a[i][2 * k] + mat_b[2 * k + 1][j])

    if (m % 2 == 1):
        for i in range(n):
            for j in range(t):
                res_matrix[i][j] = res_matrix[i][j] + mat_a[i][m - 1] * mat_b[m - 1][j]

    return res_matrix


def optimized_vinograd_alg(mat_a, mat_b):
    if (len(mat_a[0]) != len(mat_b)):
        print("Ошибка: Размеры не совпадают - умножение таких матриц невозможно")

        return []

    n = len(mat_a)
    m = len(mat_a[0])
    t = len(mat_b[0])

    res_matrix = [[0] * t for _ in range(n)]

    tmp_row = [0] * n
    tmp_col = [0] * t

    for i in range(n):
        for j in range(0, m // 2):
            tmp_row[i] = tmp_row[i] + mat_a[i][2 * j] * mat_a[i][2 * j + 1]

    for i in range(t):
        for j in range(0, m // 2):
            tmp_col[i] = tmp_col[i] + mat_b[2 * j][i] * mat_b[2 * j + 1][i]


    flag = m % 2

    for i in range(n):
        for j in range(t):

            res_matrix[i][j] -= (tmp_row[i] + tmp_col[i])

            for k in range(1, m, 2):

                res_matrix[i][j] += (mat_a[i][k - 1] + mat_b[k][j]) * (mat_a[i][k] + mat_b[k - 1][j])

            if (flag):
                res_matrix[i][j] += mat_a[i][m - 1] * mat_b[m - 1][j]

    return res_matrix
