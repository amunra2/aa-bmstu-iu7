#include "mainwindow.h"

#include <QApplication>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;

    w.setMinimumHeight(800);
    w.setMaximumHeight(800);
    w.setMinimumWidth(1100);
    w.setMaximumWidth(1100);
    w.show();

    return a.exec();
}
