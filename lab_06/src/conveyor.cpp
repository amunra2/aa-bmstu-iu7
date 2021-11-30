#include "conveyor.h"

double time_now = 0;

std::vector<double> t1;
std::vector<double> t2;
std::vector<double> t3;


void log_linear(matrix_t &matrix, int task_num, int stage_num, void (*func)(matrix_t &), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double start_res_time = time_now, res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(matrix);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count()) / 1e9;

     // here or after print?

    time_now = start_res_time + res_time;

    if (is_print)
        printf("Task: %3d, Tape: %3d, Start: %.6f, End: %.6f\n", 
                    task_num, stage_num, start_res_time, start_res_time + res_time);
}



void log_conveyor(matrix_t &matrix, int task_num, int stage_num, void (*func)(matrix_t &), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(matrix);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count()) / 1e9;

     // here or after print?

    double start_res_time;

    if (stage_num == 1)
    {
        start_res_time = t1[task_num - 1];

        t1[task_num] = start_res_time + res_time;
        t2[task_num - 1] = t1[task_num];
    }
    else if (stage_num == 2)
    {
        start_res_time = t2[task_num - 1];

        t2[task_num] = start_res_time + res_time;
        t3[task_num - 1] = t2[task_num];
    }
    else if (stage_num == 3)
    {
        start_res_time = t3[task_num - 1];
    }

    if (is_print)
        printf("Task: %3d, Tape: %3d, Start: %.6f, End: %.6f\n", 
                    task_num, stage_num, start_res_time, start_res_time + res_time);
}


void stage1_linear(matrix_t &matrix, int task_num, bool is_print)
{
    log_linear(matrix, task_num, 1, get_avg, is_print);
}



void stage2_linear(matrix_t &matrix, int task_num, bool is_print)
{   
    log_linear(matrix, task_num, 2, get_max, is_print);
}


void stage3_linear(matrix_t &matrix, int task_num, bool is_print)
{   
    log_linear(matrix, task_num, 3, fill_matrix, is_print);
}


void parse_linear(int count, size_t size, bool is_print)
{

    time_now = 0;

    std::queue<matrix_t> q1;
    std::queue<matrix_t> q2;
    std::queue<matrix_t> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    for (int i = 0; i < count; i++)
    {
        matrix_t res = generate_matrix(size);
        
        queues.q1.push(res);
    }

    for (int i = 0; i < count; i++)
    {
        matrix_t matrix = queues.q1.front();
        stage1_linear(matrix, i + 1, is_print);
        queues.q1.pop();
        queues.q2.push(matrix);

        matrix = queues.q2.front();
        stage2_linear(matrix, i + 1, is_print); // Stage 2
        queues.q2.pop();
        queues.q3.push(matrix);

        matrix = queues.q3.front();
        stage3_linear(matrix, i + 1, is_print); // Stage 3
        queues.q3.pop();

        // if (is_print)
        //     print_matrix(matrix);
    }
}



void stage1_parallel(std::queue<matrix_t> &q1, std::queue<matrix_t> &q2, std::queue<matrix_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    while(!q1.empty())
    {      
        m.lock();
        matrix_t matrix = q1.front();
        m.unlock();

        log_conveyor(matrix, task_num++, 1, get_avg, is_print);

        m.lock();
        q2.push(matrix);
        q1.pop();
        m.unlock();
    }
}


void stage2_parallel(std::queue<matrix_t> &q1, std::queue<matrix_t> &q2, std::queue<matrix_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    do
    {   
        m.lock();
        bool is_q2empty = q2.empty();
        m.unlock();

        if (!is_q2empty)
        {   
            m.lock();
            matrix_t matrix = q2.front();
            m.unlock();

            log_conveyor(matrix, task_num++, 2, get_max, is_print);

            m.lock();
            q3.push(matrix);
            q2.pop();
            m.unlock();
        }
    } while (!q1.empty() || !q2.empty());
}


void stage3_parallel(std::queue<matrix_t> &q1, std::queue<matrix_t> &q2, std::queue<matrix_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    do
    {
        m.lock();
        bool is_q3empty = q3.empty();
        m.unlock();

        if (!is_q3empty)
        {
            m.lock();
            matrix_t matrix = q3.front(); 
            m.unlock();

            log_conveyor(matrix, task_num++, 3, fill_matrix, is_print);

            m.lock();
            q3.pop();
            m.unlock();
        }
    } while (!q1.empty() || !q2.empty() || !q3.empty());
}


void parse_parallel(int count, size_t size, bool is_print)
{
    t1.resize(count + 1);
    t2.resize(count + 1);
    t3.resize(count + 1);

    for (int i = 0; i < count + 1; i++)
    {
        t1[i] = 0;
        t2[i] = 0;
        t3[i] = 0;
    }

    std::queue<matrix_t> q1;
    std::queue<matrix_t> q2;
    std::queue<matrix_t> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    
    for (int i = 0; i < count; i++)
    {
        matrix_t res = generate_matrix(size);
        
        q1.push(res);
    }

    std::thread threads[THREADS];

    threads[0] = std::thread(stage1_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[1] = std::thread(stage2_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[2] = std::thread(stage3_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);

    for (int i = 0; i < THREADS; i++)
    {
        threads[i].join();
    }
}


void time_mes(void)
{
    int option, alg_option;

    std::cout << "\n\nВыбор алгоритма: \
                    \n\t1) Линейный \
                    \n\t2) Параллельный\n\n";

    std::cin >> alg_option;

    std::cout << "\n\nЗамер времени: \
                    \n\t1) Разный размер матриц \
                    \n\t2) Разное кол-во матриц\n\n";

    std::cin >> option;

    if (option == 1)
    {
        int count = 0;
        size_t size_b, size_e;

        std::cout << "\nКоличество: ";
        std::cin >> count;

        std::cout << "\nНачальный размер: ";
        std::cin >> size_b;

        std::cout << "\nКонечный размер: ";
        std::cin >> size_e;

        if ((alg_option < 3) && (alg_option > 0))
            printf("\n\n Размер   |   Время \
                \n----------------------\n");
        else
        {
            printf("Ошибка: Алгоритм выбран неверно\n");
            return;
        }


        for (size_t i_size = size_b; i_size <= size_e; i_size += STEP_SIZE)
        {   
            time_now = 0;

            if (alg_option == 1)
            {
                parse_linear(count, i_size, false);

                printf("  %3ld     |   %3.4f\n", i_size, time_now);
            }
            else if (alg_option == 2)
            {
                parse_parallel(count, i_size, false);

                printf("  %3ld     |   %3.4f\n", i_size, time_now);
            }
        }
    }
    else if (option == 2)
    {
        int count_b, count_e;
        size_t size;

        std::cout << "\nНачальное количество: ";
        std::cin >> count_b;

        std::cout << "\nКонечное количество: ";
        std::cin >> count_e;

        std::cout << "\nРазмер: ";
        std::cin >> size;

        if ((alg_option < 3) && (alg_option > 0))
            printf("\n\n Кол-во   |   Время \
                \n----------------------\n");
        else
        {
            printf("Ошибка: Алгоритм выбран неверно\n");
            return;
        }


        for (int i_count = count_b; i_count <= count_e; i_count += STEP_COUNT)
        {   
            time_now = 0;

            if (alg_option == 1)
            {
                parse_linear(i_count, size, false);

                printf("  %4d    |   %3.4f\n", i_count, time_now);
            }
            else if (alg_option == 2)
            {
                parse_parallel(i_count, size, false);

                printf("  %4d    |   %3.4f\n", i_count, time_now);
            }
        }
    }
    else
    {
        printf("Ошибка: Тип замера выбран неварно\n");
    }
}


void info_stages(void)
{
    printf("\n\nПоследовательная обработка матриц: \
            \n\tЭтап 1. Среднее арифметическое элементов матрицы \
            \n\tЭтап 2. Максимальный элемент в матрице \
            \n\tЭтап 3. На нечетную позицию в матрице ставится среднее \
            \n\t        арифметическое, а на четную - максимальный элемент");
}