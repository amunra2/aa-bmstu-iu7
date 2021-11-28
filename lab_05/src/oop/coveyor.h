#ifndef CONVEYOR_H
#define CONVEYOR_H


#include <thread>
#include <queue>
#include <vector>
#include <memory>

#include "spec_matrix.h"


#define THREADS 4 // change

class Conveyor
{
public:
    Conveyor() = default;
    ~Conveyor() = default;

    void exec_parallel(int count);
    void exec_no_parallel(int count);

    void exec_stage1();
    void exec_stage2();
    void exec_stage3();

private:
    std::thread threads[THREADS];

    std::vector<std::shared_ptr<SpecMatrix>> spec_matrixes;

    std::queue<std::shared_ptr<SpecMatrix>> queue1;
    std::queue<std::shared_ptr<SpecMatrix>> queue2;
    std::queue<std::shared_ptr<SpecMatrix>> queue3;
};


#endif