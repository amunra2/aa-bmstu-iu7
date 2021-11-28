#include "matrix.h"


void get_avg(matrix_t &matrix)
{
    double sum = 0;

    for (size_t i = 0; i < matrix.size; i++)
    {
        for (size_t j = 0; j < matrix.size; j++)
        {
            sum += matrix.data[i][j];
        }
    }

    matrix.avg = sum / (matrix.size * matrix.size);
}


void get_max(matrix_t &matrix)
{
    double maximum = matrix.data[0][0];

    for (size_t i = 0; i < matrix.size; i++)
    {
        for (size_t j = 0; j < matrix.size; j++)
        {
            if (matrix.data[i][j] >= maximum) 
                maximum = matrix.data[i][j];
        }
    }

    matrix.max = maximum;
}


void fill_matrix(matrix_t &matrix)
{
    for (size_t i = 0; i < matrix.size; i++)
    {
        for (size_t j = 0; j < matrix.size; j++)
        {
            if ((i + j + 1) % 2 == 0)
            {
                matrix.data[i][j] = matrix.max;
            }
            else
            {
                matrix.data[i][j] = matrix.avg;
            }
        }
    }
}


int get_max_in_column(matrix_t matrix, int col_place)
{
    double max_elem = matrix.data[col_place][col_place];
    size_t max_place = col_place;

    for (size_t i = col_place + 1; i < matrix.size; i++)
    {
        if (matrix.data[i][col_place] >= max_elem)
        {
            max_elem = matrix.data[i][col_place];
            max_place = i;
        }
    }

    return max_place;
}


int triangulation(matrix_t &matrix) // приведение к верхнетреугольной матрице
{
    int swaps = 0;

    for (size_t i = 0; i < matrix.size - 1; i++)
    {
        size_t max_col_place = get_max_in_column(matrix, i);

        if (max_col_place != i)
        {
            std::swap(matrix.data[i], matrix.data[max_col_place]);

            swaps++;
        }

        for (size_t j = i + 1; j < matrix.size; j++)
        {
            double mult = -matrix.data[j][i] / matrix.data[i][i]; 

            for (size_t k = i; k < matrix.size; k++)
            {
                matrix.data[j][k] += matrix.data[i][k] * mult;
            }
        }
    }

    return swaps;
}


void get_determinate(matrix_t &matrix) // метод Гаусса
{
    int swaps = triangulation(matrix);

    double det = 1;

    if (swaps % 2 == 1)
    {
        det *= -1;
    }

    for (size_t i = 0; i < matrix.size; i++)
    {
        det *= matrix.data[i][i];
    }

    // matrix.det = det;
}


matrix_t generate_matrix(size_t size)
{
    std::vector<std::vector<double>> tmp_data;

    tmp_data.resize(size);

    for (size_t i = 0; i < size; i++)
    {
        tmp_data[i].resize(size);
    }

    matrix_t matrix;
    matrix.size = size;
    matrix.data = tmp_data;

    for (size_t i = 0; i < matrix.size; i++)
    {
        for (size_t j = 0; j < matrix.size; j++)
        {
            matrix.data[i][j] = rand() % 10 + 1;
        }
    }

    return matrix;
}


void print_matrix(matrix_t matrix)
{
    printf("\n\n");

    for (size_t i = 0; i < matrix.size; i++)
    {
        for (size_t j = 0; j < matrix.size; j++)
        {
            printf("%-15.1f ", matrix.data[i][j]);
        }

        printf("\n");
    }
}
