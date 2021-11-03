# Libs
import matplotlib.pyplot as plt 

# Text
MSG = "\n\n      Меню \n\n \
    Программа для построения графиков к распараллеливанию\n \
    пучка отрезков Брезенхема. \n\n \
    1. График зависимости времени от кол-ва потоков \n \
    2. График зависмости времени от длины пучка \n \
    0. Выход \n\n \
    \
    Выбор: \
    "

# Define
EXIT = 0
DIF_THREADS = 1
DIF_DIAMS = 2

NUM = 0
TIME = 1

MAX_THREADS = 32

FILE_THREADS = "data/time_different_threads.csv"
FILE_DIF_DIAM_4THREADS = "data/time_dif_diams_4threads.csv"
FILE_DIF_DIAM_NOPARALLEL = "data/time_dif_diams_noparallel.csv"
FILE_NOPARALLEL = "data/time_noparallel.csv"


def get_time_from_file(filename):

    try:
        f = open(filename, "r")

        time_file = []

        for line in (f.readlines()):
            time_file.append([float(num) for num in (line.split("|"))])

        f.close()

        lengths = []
        time = []

        for arr in time_file:
            lengths.append(int(arr[NUM]))
            time.append(arr[TIME])

        print("\n\033[32mSuccess\033[37m: File \"", filename, "\" parsed")

        return lengths, time
    except:
        print("\n\033[31mFailed\033[37m: Mistake occured while parsing \"", filename, "\"\n")

        return [], []


def graph_different_threads():

    threads, time_threads = get_time_from_file(FILE_THREADS)
    noparallel_arr, time_noparallel = get_time_from_file(FILE_NOPARALLEL)

    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(threads, time_threads, label = "Разное количество потоков")
    plot.plot(threads, time_noparallel * MAX_THREADS, label="Без распараллеливания")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Кол-во потоков")
    
    plt.show()


def graph_different_diams():

    diams_4thread, time_4threads = get_time_from_file(FILE_DIF_DIAM_4THREADS)
    diams_noparallel, time_noparallel = get_time_from_file(FILE_DIF_DIAM_NOPARALLEL)

    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(diams_4thread, time_4threads, label = "Распараллеивание на 4 потока")
    plot.plot(diams_noparallel, time_noparallel, label="Без распараллеливания")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (с)")
    plt.xlabel("Кол-во пучков")
    
    plt.show()


def main():
    option = -1

    while (option != EXIT):
        option = int(input(MSG))

        if (option == DIF_THREADS):

            graph_different_threads()

        elif (option == DIF_DIAMS):
            
            graph_different_diams()

        else:
            print("\nПовторите ввод\n")


if __name__ == "__main__":
    main()
    