# Sorts

def insertion_sort(arr, n):
    
    for i in range(1, n):
        j = i - 1
        tmp = arr[i]

        while (j >= 0 and arr[j] > tmp):
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = tmp

    return arr


def shaker_sort(arr, n):

    left = 0
    right = n - 1

    swapped = True

    while(swapped):
        swapped = False

        for i in range(left, right):
            if (arr[i] > arr[i + 1]):
                tmp = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = tmp

                swapped = True

        if (swapped == False):
            break

        swapped = False
        right -= 1

        for i in range(right - 1, left - 1, -1):
            if (arr[i] > arr[i + 1]):
                tmp = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = tmp

                swapped = True

        left += 1

    return arr


def gnomme_sort(arr, n):
    
    i = 1

    while (i < n):
        if (arr[i] < arr[i - 1]):
            tmp = arr[i]
            arr[i] = arr[i - 1]
            arr[i - 1] = tmp

            if (i > 1):
                i -= 1
        else:
            i += 1

    return arr