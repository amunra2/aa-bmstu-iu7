#ifndef BUILDING_H
#define BUILDING_H

#include <ui_mainwindow.h>
#include <math.h>

#include <thread>
#include <mutex>
#include <vector>
#include <chrono>
#include <ctime>

#include <iostream>

#include "timer.h"


#define WIN_X 709
#define WIN_Y 709
#define PI 3.1415
#define PT_SIZE 0.1

#define MAX_THREADS 32

#define MAX_DIAM 10000
#define MIN_DIAM 500
#define DIAM_STEP 500
 
#define ITERATIONS 300


#define SWAP(t, a, b) do { t temp = a; a = b; b = temp; } while(0);

struct request
{
    int algorithm;
    QColor color;
    QGraphicsScene *scene;

    bool is_draw;
};

struct beam_settings
{
    int d;
    int threads_count;
};

struct point
{
    double x;
    double y;
};


enum types
{
    PARALLEL,
    NO_PARALLEL
};

using point_t = struct point;

using request_t = struct request;

using beam_stgs_t = struct beam_settings;

int sign(const int &number);

void calculate_beam_no_parallel(const request_t &request, const beam_stgs_t &settings);
void calculate_beam_parallel(const request_t &request, const beam_stgs_t &settings);

void calculate_line(const request_t &request, const point_t &pt1, const point_t &pt2);

void breshenham_float(const request_t &request, const point_t &pt1, const point_t &pt2);

double time_mes_no_parallel(const request_t &request, const beam_stgs_t &settings);
double time_mes_parallel(const request_t &request, const beam_stgs_t &settings);

#endif
