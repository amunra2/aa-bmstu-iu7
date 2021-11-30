#ifndef MATRIX_H
#define MATRIX_H

#include <random>
#include <vector>
#include <iostream>
#include <queue>
#include <thread>
#include <math.h>
#include <string>



struct matrix_s
{
    std::vector<std::vector<double>> data;

    size_t size;

    double avg;
    double max;
};

using matrix_t = struct matrix_s;


// Funcs
matrix_t generate_matrix(size_t size);
matrix_t copy_matrix(matrix_t matrix);
void print_matrix(matrix_t matrix);

void get_avg(matrix_t &matrix);
void get_max(matrix_t &matrix);
void get_determinate(matrix_t &matrix);
void fill_matrix(matrix_t &matrix);

#endif