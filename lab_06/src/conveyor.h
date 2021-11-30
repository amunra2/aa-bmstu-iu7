#ifndef CONVEYOR_H
#define CONVEYOR_H

#include <random>
#include <vector>
#include <iostream>
#include <queue>
#include <thread>
#include <chrono>
#include <ctime>
#include <mutex>

#include "matrix.h"


#define THREADS 3
#define STEP_SIZE 100
#define STEP_COUNT 5


struct queues_s
{
    std::queue<matrix_t> q1;
    std::queue<matrix_t> q2;
    std::queue<matrix_t> q3;
};

using queues_t = struct queues_s;


// Funcs

void parse_linear(int count, size_t size, bool is_print);
void parse_parallel(int count, size_t size, bool is_print);
void time_mes(void);
void info_stages(void);

#endif