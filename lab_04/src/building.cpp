#include "building.h"


extern QImage image;


int sign(const int &number)
{
    if (number > 0)
    {
        return 1;
    }
    else if (number < 0)
    {
        return -1;
    }

    return 0;
}


static void draw_pixel(const request_t &request, int x, int y)
{
    image.setPixel(x, y, request.color.rgb());
}


void breshenham_float(const request_t &request, const point_t &pt1, const point_t &pt2)
{
    int dx = abs(pt2.x - pt1.x);
    int dy = abs(pt2.y - pt1.y);

    int sx = sign(pt2.x - pt1.x);
    int sy = sign(pt2.y - pt1.y);

    int change = 0;

    if (dy > dx)
    {
        SWAP(int, dx, dy);
        change = 1;
    }

    double m = (double)dy / (double)dx;
    double e = m - 0.5;

    int x = pt1.x;
    int y = pt1.y;

    std::mutex mut;

    for (int i = 0; i < dx; i++)
    {
        if (request.is_draw)
        {
            mut.lock();
            draw_pixel(request, x, y);
            mut.unlock();
        }

        if (e >= 0)
        {
            if (change == 0)
            {
                y += sy;
            }
            else
            {
                x += sx;
            }

            e -= 1;
        }

        if (e < 0)
        {
            if (change == 0)
            {
                x += sx;
            }
            else
            {
                y += sy;
            }

            e += m;
        }
    }

}


void calculate_beam_no_parallel(const request_t &request, const beam_stgs_t &settings)
{
    int spektr = 360;

    point_t pt1, pt2;
    pt1.x = WIN_X / 2;
    pt1.y = WIN_Y / 2;

    for (int i = 0; i < spektr; i += 1)
    {
        pt2.x = cos(i * PI / 180) * settings.d + WIN_X / 2;
        pt2.y = sin(i * PI / 180) * settings.d + WIN_Y / 2;

        // Round for Bresenham float
        pt1.x = round(pt1.x);
        pt1.y = round(pt1.y);
        pt2.x = round(pt2.x);
        pt2.y = round(pt2.y);


        calculate_line(request, pt1, pt2);
    }
}


void calculate_part_beam(const request_t &request, const beam_stgs_t &settings, int thread_ind)
{   
    // std::cout << "\n======== Started: calculate_part_beam " << thread_ind + 1 << " ========\n" << std::endl;

    int spektr = 360;

    // For parallel
    int sector_in_thread = spektr / settings.threads_count;
    int part_ind = thread_ind * sector_in_thread;

    if (thread_ind + 1 == settings.threads_count)
    {
        sector_in_thread += (spektr - sector_in_thread * settings.threads_count);
    }
    // End 

    point_t pt1, pt2;
    pt1.x = WIN_X / 2;
    pt1.y = WIN_Y / 2;

    for (int i = part_ind; i < part_ind + sector_in_thread; i += 1)
    {

        pt2.x = cos(i * PI / 180) * settings.d + WIN_X / 2;
        pt2.y = sin(i * PI / 180) * settings.d + WIN_Y / 2;

        // Round for Bresenham float
        pt1.x = round(pt1.x);
        pt1.y = round(pt1.y);
        pt2.x = round(pt2.x);
        pt2.y = round(pt2.y); 

        calculate_line(request, pt1, pt2);
    }

    // std::cout << "\n======== Ended: calculate_part_beam " << thread_ind + 1 << " ========\n" << std::endl;
}


void calculate_beam_parallel(const request_t &request, const beam_stgs_t &settings)
{
    std::vector<std::thread> threads(settings.threads_count);

    for (int i = 0; i < settings.threads_count; i++)
    {
        threads[i] = std::thread(calculate_part_beam, request, settings, i);
    }

    for (int i = 0; i < settings.threads_count; i++)
    {
        threads[i].join();
    }
}


void calculate_line(const request_t &request, const point_t &pt1, const point_t &pt2)
{
    breshenham_float(request, pt1, pt2);
}


double time_mes_no_parallel(const request_t &request, const beam_stgs_t &settings)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double res_time = 0;

    for (int i = 0; i < ITERATIONS; i++)
    {
        time_start = std::chrono::system_clock::now();
        calculate_beam_no_parallel(request, settings);
        time_end = std::chrono::system_clock::now();

        res_time += (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count());
    }

    res_time /= ITERATIONS; 

    return res_time / 1e9;
}


double time_mes_parallel(const request_t &request, const beam_stgs_t &settings)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double res_time = 0;

    for (int i = 0; i < ITERATIONS; i++)
    {
        time_start = std::chrono::system_clock::now();
        calculate_beam_parallel(request, settings);
        time_end = std::chrono::system_clock::now();

        res_time += (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count());
    }

    res_time /= ITERATIONS;

    return res_time / 1e9;
}
