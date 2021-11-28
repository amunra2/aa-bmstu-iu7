#ifndef SPEC_MATRIX_H
#define SPEC_MATRIX_H

#include <memory>

class Stage1
{
public:
    Stage1();
    ~Stage1() = default;
};


class Stage2
{
public:
    Stage2();
    ~Stage2() = default;
};


class Stage3
{
public:
    Stage3();
    ~Stage3() = default;
};



class SpecMatrix
{
public:
    SpecMatrix() = default;
    ~SpecMatrix() = default;


    void exec_stage1();
    void exec_stage2();
    void exec_stage3();

private:

    double 

    std::unique_ptr<Stage1> stage1;
    std::unique_ptr<Stage2> stage2;
    std::unique_ptr<Stage3> stage3;
};

#endif