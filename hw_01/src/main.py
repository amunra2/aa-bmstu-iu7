def levenstein_matrix():
    str1 = input("Input 1 string:")                     # 1
    str2 = input("Input 2 string:")                     # 2

    n = len(str1)                                       # 3
    m = len(str2)                                       # 4

    matrix = [[0] * m for _ in range(n)]                # 5

    for i in range(n):                                  # 6
        matrix[i][0] = i                                # 7
    
    for j in range(m):                                  # 8
        matrix[0][j] = j                                # 9

    for i in range(1, n + 1):                           # 10
        for j in range(1, m + 1):                       # 11
            add = matrix[i - 1][j] + 1                  # 12
            delete = matrix[i][j - 1] + 1               # 13
            change = matrix[i - 1][j - 1]               # 14
            
            if (str1[i - 1] != str2[j - 1]):            # 15
                change += 1                             # 16

            matrix[i][j] = min(add, delete, change)     # 17

    return matrix[n][m]