#include <iostream>

#include "conveyor.h"



void print_menu()
{
    printf("\n\nСтупенчатая обработка матрицы \
        \n\t1. Линейная обработка \
        \n\t2. Конвейерная обработка \
        \n\t3. Замерить время \
        \n\t4. Вывести информацию об этапах обработки \
      \n\n\t0. Выход\n\n");
}


void run()
{
    int option = -1;

    while (option != 0)
    {
        print_menu();

        std::cout << "Выбор: ";
        std::cin >> option;

        if (option == 1)
        {   
            int size = 0, count = 0;

            std::cout << "\n\nРазмер: ";
            std::cin >> size;

            std::cout << "Количество: ";
            std::cin >> count;

            parse_linear(count, size, true);
        }
        else if (option == 2)
        {
            int size = 0, count = 0;

            std::cout << "\n\nРазмер: ";
            std::cin >> size;

            std::cout << "Количество: ";
            std::cin >> count;

            parse_parallel(count, size, true);
        }
        else if (option == 3)
        {
            time_mes();
        }
        else if (option == 4)
        {
            info_stages();
        }
        else
        {
            printf("\nОшибка: Неверно введен пункт меню. Повторите\n");
        }
    }
}



int main(void)
{
    run();

    return 0;
}
