#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>
#include "gnuplot-iostream.h"  // Подключаем библиотеку Gnuplot

const long double initial_u = (1600 - 20) / 20;

long double u(long double tau) {
    return initial_u;
}

long double f(long double x, long double tau, long double phi) {
    return -std::pow(phi, 2) * x + phi * 79;
}

long double newSum(long double phi, long double tau) {
    return 79.0 / phi * (1 - std::exp(-tau * std::pow(phi, 2)));
}

long double solve(long double x, long double phi, long double tau, long double h) {
    long double k1 = h * f(x, tau, phi);
    long double k2 = h * f(x + h * k1 / 2, tau + h / 2, phi);
    long double k3 = h * f(x + h * k2 / 2, tau + h / 2, phi);
    long double k4 = h * f(x + h * k3, tau + h, phi);
    return x + 1.0 / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4);
}

void print_matrix(const std::vector<std::vector<long double>>& matrix) {
    int n = 10; // Assuming a fixed size for better formatting
    for (const auto& row : matrix) {
        for (int j = 0; j < n; ++j) {
            std::cout << std::fixed << std::setprecision(8) << row[j] << " ";
        }
        std::cout << std::endl;
    }
}

void plot_graph(const std::vector<long double>& x, const std::vector<long double>& y, const std::string& title) {
    Gnuplot gp;

    gp << "set terminal wxt size 600,400" << std::endl;  // Устанавливаем тип терминала и размер окна
    gp << "set title '" << title << "'" << std::endl;     // Устанавливаем заголовок графика
    gp << "plot '-' with lines title '" << title << "'" << std::endl;

    for (size_t i = 0; i < x.size(); ++i) {
        gp << x[i] << " " << y[i] << std::endl;
    }

    gp << "e" << std::endl;  // Завершаем ввод данных
}

int main() {
    int t = 4;
    long double R = 0.25;
    long double a = 0.0153;
    long double tau = a * t / std::pow(R, 2);
    int m = 10000;
    long double h = tau / m;

    std::vector<long double> tau_list(m);
    for (int i = 0; i < m; ++i) {
        tau_list[i] = i * h;
    }

    std::vector<long double> phi = {1.1597, 13.2758, 43.2740, 92.729};
    std::vector<std::vector<long double>> answer;

    for (const auto& current_phi : phi) {
        std::vector<long double> tmp;
        for (int i = 0; i < m; ++i) {
            tmp.push_back(newSum(current_phi, i * h));
        }
        answer.push_back(tmp);
    }

    print_matrix(answer);

    // Построение графиков
    for (size_t i = 0; i < phi.size(); ++i) {
        plot_graph(tau_list, answer[i], "NewSum for phi = " + std::to_string(phi[i]));
    }

    std::vector<std::vector<long double>> solution(t, std::vector<long double>(m, 0.0));

    for (int i = 0; i < t; ++i) {
        for (int j = 1; j < m; ++j) {
            if (tau_list[j] > 0.5) {
                // Some condition, adjust as needed
            }
            long double tmp = solve(solution[i][j - 1], phi[i], tau_list[j], h);
            solution[i][j] = tmp;
        }
    }

    print_matrix(solution);

    // Построение графиков
    for (int i = 0; i < t; ++i) {
        plot_graph(tau_list, solution[i], "Solution for phi = " + std::to_string(phi[i]));
    }

    return 0;
}
