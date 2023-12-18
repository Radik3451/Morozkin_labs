import math
import matplotlib.pyplot as plt


def u(tau, flag):
    return u_list[flag]


def dn(bi,phi):
    return(2*pow(bi,2))/((pow(phi, 2) + pow(bi, 2) + bi)*math.sin(phi))


def tetta(l, tau, phi):
    tetta = 0
    for i in range(t):
        tetta += dn(bi, phi[i]) * answer[i][tau] * math.cos(phi[i] * l)
    return tetta


def f(x, tau, phi, flag):
    return -pow(phi, 2) * x + phi * u(tau, flag)


def newSum(phi, tau):
    return 79.0 / phi * (1 - pow(math.e, -tau * pow(phi, 2)))


def solve(x, phi, tau, flag):
    k1 = f(x, tau, phi, flag)
    k2 = f(x + h / 2, tau + h / 2 * k1, phi, flag)
    k3 = f(x + h / 2, tau + h / 2 * k2, phi, flag)
    k4 = f(x + h, tau + h * k3, phi, flag)
    return x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def print_matrix(matrix):
    # n = len(matrix[0])
    n = 10
    for i in range(len(matrix)):
        for j in range(n):
            print(f"{matrix[i][j]:.3f}", end=" ")
        print()


if __name__ == '__main__':
    t = 4
    R = 0.25
    alpha = 200
    lamb = 23
    T0=20
    tau = 1
    m = 10_000
    h = tau / m
    u_list = [39 + (40/12)*i for i in range(13)]

    tau_list = [i * h for i in range(m)]
    tau_switch = [i/12 for i in range(0, 13)]
    phi = [1.1597, 13.2758, 43.2740, 92.729]
    answer = []

    answer = [[0.0] for i in range(t)]
    for i in range(len(answer)):
        flag = 1
        for j in range(1, m-1):
            switch = False
            for item in tau_switch:
                if (tau_list[j] < item and tau_list[j + 1] > item or tau_list[j] == item):
                    switch = True
                    flag += 1
            answer[i].append(solve(answer[i][j - 1], phi[i], tau_list[j], flag))
        plt.plot(tau_list[:9999], answer[i], label=phi[i])  
    print_matrix(answer)
    plt.legend()
    plt.show()

    bi = alpha * R / lamb
    
    tetta_list = [0]
    for i in range(m-1):
        tetta_list.append(tetta(0, i, phi))
    t_list = []
    for i in range(m):
        t_list.append(20*tetta_list[i] + 20)
    plt.plot(tau_list, t_list)

    tetta_list = [0]
    for i in range(m-1):
        tetta_list.append(tetta(1, i, phi))
    t_list = []
    for i in range(m):
        t_list.append(20*tetta_list[i] + 20)
    plt.plot(tau_list, t_list)

    plt.show()