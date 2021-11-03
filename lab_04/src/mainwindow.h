#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "building.h"
#include "timer.h"

#define WIN_X 709
#define WIN_Y 709

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_clean_clicked();

    void on_beam_clicked();

    void read_parallel(int &type_parallel);

    request_t init(void);

    void on_time_mes_btn_clicked();

    void on_time_mes_btn_dif_d_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
