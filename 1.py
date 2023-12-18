import math
import matplotlib.pyplot as plt

def u(tau):
    return (1600 - 20) / 20


def f(x, tau, phi):
    return -pow(phi, 2) * x + phi * 79


def newSum(phi, tau):
    return 79.0 / phi * (1 - pow(math.e, -tau * pow(phi, 2)))


def solve(x, phi, tau, h):
    k1 = h * f(x, tau, phi)
    k2 = h * f(x + h * k1 / 2, tau + h / 2, phi)
    k3 = h * f(x + h * k2 / 2, tau + h / 2, phi)
    k4 = h * f(x + h * k3, tau + h, phi)
    return x + 1/ 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def print_matrix(matrix):
    # n = len(matrix[0])
    n = 10
    for i in range(len(matrix)):
        for j in range(n):
            print(f"{matrix[i][j]:.8f}", end=" ")
        print()


if __name__ == '__main__':
    t = 4
    R = 0.25
    a = 0.0153
    tau = a * t / R**2
    m = 10_000
    h = tau / m

    tau_list = [i * h for i in range(m)]
    phi = [1.1597, 13.2758, 43.2740, 92.729]
    answer = []

    for j in range(len(phi)):
        tmp = []
        for i in range(m):
            tmp.append(newSum(phi[j], i * h))
        answer.append(tmp)
        plt.plot(tau_list, tmp, label=phi[j])
    print_matrix(answer)
    plt.legend()
    plt.show()
    print()


    answer = [[0.0] for i in range(t)]
    for i in range(len(answer)):
        for j in range(1, m):
            if (tau_list[j] > 0.5):
                pass
            tmp = solve(answer[i][j - 1], phi[i], tau_list[j], h)
            answer[i].append(tmp)
        # if(i==1):
        plt.plot(tau_list, answer[i], label=phi[i])    
    print_matrix(answer)

    plt.legend()
    plt.show()
