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


def print_matrix_answer(matrix):
    # n = len(matrix[0])
    n = 10
    for i in range(len(matrix)):
        for j in range(n):
            print(f"{matrix[i][j]:.3f}", end=" ")
        print()

def implicit_scheme(matrix, nx, nt):
    tmp = (h)/(1**2)
    A = [0 for i in range(nx)]
    B = [0 for i in range(nx)]
    C = [0 for i in range(nx)]
    
    # T = [[0 for i in range(nx)] for i in range(nx)]
    for i in range(nx):
        if(i != nx-1):
            B[i] = 2*tmp + 1

        if(i < nx-1):
            C[i] = -tmp
        else: 
            C[i] = 0

        if(i > 0):
            A[i] = -tmp
        else: 
            A[i] = 0
    B[0] = 1
    B[nx-1] = 1
    C,A = A,C

    for k in range (1,nt):
        # d = [matrix[k-1][i] + tau*f(x[i],t[k-1]) for i in range(nx)]
        # d = [matrix[k-1][i] for i in range(nx)]
        # Прямой ход метода прогонки
        flag=1
        if (k != 9999):
            for item in tau_switch:
                if (tau_list[k] < item and tau_list[k + 1] > item or tau_list[k] == item):
                    flag += 1

        alpha_list = ([0 for _ in range(nx)])
        beta_list = [0 for _ in range(nx)]

        alpha_list[0] = (2*1*h*lamb)/(lamb*1**2 + 2*1*h*(lamb + alpha*1))
        beta_list[0] = (lamb*1**2*matrix[k-1][1] + 2*1*h*1*alpha*u(tau_list[i], flag))/(lamb*1**2 + 2*1*h*(lamb + alpha*1))

        for i in range(1, nx-1):
            alpha_list[i] = (2*1*h*lamb)/(lamb*1**2 + 2*1*h*(lamb + alpha*1))
            beta_list[i] = (lamb*1**2*matrix[k-1][i] + 2*1*h*1*alpha*u(tau_list[i], flag))/(lamb*1**2 + 2*1*h*(lamb + alpha*1))

        # Обратный ход метода прогонки
        U = [0 for i in range(nx)]
        U[nx-1] = (lamb*1**2*matrix[k][nx-1] + 2*1*h*(lamb*beta_list[nx-2] + 1*alpha*get_u(tau_list[k])))/\
            (lamb*1**2 + 2*1*h*(1*alpha + lamb*(1 - alpha_list[nx-2])))
        for i in range(nx-2,-1,-1):
            U[i] = alpha_list[i]*U[i+1] + beta_list[i]

        for i in range (1,nx-1):
            matrix[k][i] = U[i]

    print_matrix(matrix, "Неявная схема")
    return matrix

def get_u(x):
    for i in range(len(tau_switch) - 1):
        if (tau_switch[i] <= x < tau_switch[i+1]):
            u = u_list[i]
            return u

def print_matrix(A, name):
    nx = len(A)
    m = len(A[0])
    print(f'\t\t\t{name}')
    for i in range(nx-1, -1, -1):
        for j in range (m):
            print(f"{A[i][j]:5.3f}", end=' ')
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
    u_list = [39 + (40/7)*i for i in range(8)]

    tau_list = [i * h for i in range(m)]
    tau_switch = [i/7 for i in range(0, 8)]
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
    print_matrix_answer(answer)
    plt.legend()
    plt.show()

    bi = alpha * R / lamb
    
    tetta_list = [0]
    for i in range(m-1):
        tetta_list.append(tetta(0, i, phi))
    t_list = []
    for i in range(m):
        t_list.append(20*tetta_list[i] + 20)
    plt.plot(tau_list, t_list, label=f'l = 0')
    t_list_l0 = t_list

    tetta_list = [0]
    for i in range(m-1):
        tetta_list.append(tetta(1, i, phi))
    t_list = []
    for i in range(m):
        t_list.append(20*tetta_list[i] + 20)
    plt.plot(tau_list, t_list, label=f'l = 1')
    t_list_l1 = t_list

    plt.legend()
    plt.show()

    nx = len(answer)
    nt = len(tau_list)

    flag=0
    A = [[0 for _ in range(nx)] for _ in range(nt)]
    for i in range (nt):
        if (i != 9999):
            for item in tau_switch:
                if (tau_list[i] < item and tau_list[i + 1] > item or tau_list[i] == item):
                    flag += 1
        for j in range (nx):
            if(j == nx-1):
                A[i][j] = 50/23*(u(tau_list[j], flag) - t_list[j])
            elif(i == 0):
                A[i][j] = 0
            else: A[i][j] = 3

    answer = implicit_scheme(A, nx, nt)

    # Построение графика для каждого столбца
    for col_index in range(len(answer[0])):
        y_values = [row[col_index] for row in answer]
        plt.plot(tau_list, y_values, label=f'Column {col_index + 1}')

    # Настройка графика
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.title('Графики столбцов')

    # Отображение графика
    plt.show()